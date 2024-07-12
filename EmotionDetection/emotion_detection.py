import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_dict = response.json()
        emotions = response_dict.get('emotion_predictions', [{}])[0].get('emotions', [])
        
        # Extract the required emotions and their scores
        emotion_scores = {emotion['emotion']: emotion['score'] for emotion in emotions 
                          if emotion['emotion'] in ['anger', 'disgust', 'fear', 'joy', 'sadness']}
        
        # Ensure all required emotions are present in the dictionary, even if their scores are zero
        for emotion in ['anger', 'disgust', 'fear', 'joy', 'sadness']:
            if emotion not in emotion_scores:
                emotion_scores[emotion] = 0.0
        
        # Find the dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Add the dominant emotion to the dictionary
        emotion_scores['dominant_emotion'] = dominant_emotion

        return emotion_scores
    else:
        return {"error": "Request failed with status code " + str(response.status_code)}
