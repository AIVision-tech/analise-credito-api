import pandas as pd
from flask import request, jsonify
from transformers import pipeline
import spacy
from collections import Counter
import logging

# Configuração de Logging
logging.basicConfig(level=logging.INFO)

# Constantes
ARQUIVO_LEXICO = 'sentiment_service/lexico.csv'
EMOCOES = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']


class AnaliseSentimento:
    def __init__(self):
        self.nlp = pipeline("sentiment-analysis", model="neuralmind/bert-base-portuguese-cased")
        self.nlp_spacy = spacy.load("pt_core_news_sm")
        self.lexico = self.carregar_lexico(ARQUIVO_LEXICO)

    def carregar_lexico(self, arquivo):
        try:
            df = pd.read_csv(arquivo)
        except FileNotFoundError:
            logging.error(f'Arquivo {arquivo} não encontrado.')
            return {}

        lexico = {row['Portuguese Word']: {emocao: row[emocao] for emocao in EMOCOES} for _, row in df.iterrows()}
        return lexico

    def analyze(self, text):
        if not text:
            logging.error('Texto vazio fornecido para análise.')
            return jsonify({"error": "Texto vazio fornecido para análise."})

        sentiment_result = self.nlp(text)[0]
        sentiment_label_map = {
            "LABEL_0": "NEGATIVO",
            "LABEL_1": "POSITIVO"
        }
        sentiment_label = sentiment_label_map.get(sentiment_result['label'], "NEUTRO")

        doc = self.nlp_spacy(text.lower())
        tokens = [token.text for token in doc if not token.is_stop]

        emotions = [self.lexico.get(token, {"neutro": 1}) for token in tokens if token in self.lexico]
        emotion_counts = Counter()
        for emotion_dict in emotions:
            emotion_counts.update(emotion_dict)

        total_emotions = sum(emotion_counts.values())
        if total_emotions == 0:
            logging.info('Nenhuma emoção detectada no texto fornecido.')
            return jsonify({"info": "Nenhuma emoção detectada no texto fornecido."})

        emotion_counts.pop('positive', None)
        emotion_counts.pop('negative', None)
        dominant_emotion = max(emotion_counts, key=emotion_counts.get, default=None)
        emotion_percentages = {emotion: f"{count / total_emotions * 100:.2f}%" for emotion, count in
                               sorted(emotion_counts.items(), key=lambda item: item[1])}
        sentiment_percentage = f"{sentiment_result['score'] * 100:.2f}%"
        sentiment_data = {
            "label": sentiment_label,
            "percentage": sentiment_percentage
        }

        result = {
            "sentiment": sentiment_data,
            "dominant_emotion": dominant_emotion,
            "emotion_percentages": emotion_percentages
        }

        return jsonify(result)


app_analise = AnaliseSentimento()


def analyze():
    """
    Sentiment and Emotion Analysis
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              description: Text to analyze for sentiment and emotion.
    responses:
      200:
        description: Sentiment and emotion analysis result.
        schema:
          type: object
          properties:
            sentiment:
              type: object
              description: Overall sentiment of the text.
            dominant_emotion:
              type: string
              description: Dominant emotion of the text.
            emotion_percentages:
              type: object
              description: Percentages of different emotions in the text.
    """
    text = request.json['text']
    return app_analise.analyze(text)