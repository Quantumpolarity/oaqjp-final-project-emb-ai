import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    response = requests.post(url, headers=headers, json=input_json)
    
    try:
        response_data = response.json()
        print("API Response:", json.dumps(response_data, indent=2))  # Debug print to check the response structure

        emotion_predictions = response_data.get('emotionPredictions', [])
        
        if emotion_predictions:
            emotions = {
                'anger': 0.0,
                'disgust': 0.0,
                'fear': 0.0,
                'joy': 0.0,
                'sadness': 0.0
            }
            
            for prediction in emotion_predictions:
                emotion_mentions = prediction.get('emotionMentions', [])
                for mention in emotion_mentions:
                    if 'emotion' in mention:
                        for emotion, score in mention['emotion'].items():
                            if emotion in emotions:
                                emotions[emotion] += score
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=emotions.get)
            
            # Format the output
            output = {
                'anger': emotions['anger'],
                'disgust': emotions['disgust'],
                'fear': emotions['fear'],
                'joy': emotions['joy'],
                'sadness': emotions['sadness'],
                'dominant_emotion': dominant_emotion
            }
            
            print("Formatted Result:", output)  # Debug print to check the final result
            return output
        else:
            return "Error: 'emotionPredictions' not found in response"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    result = emotion_detector("I hate working long hours.")
    print(result)
