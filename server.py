"""
Server module for emotion detection application.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Route for emotion detection.

    This function handles POST requests to the /emotionDetector endpoint.
    It processes the input text to detect emotions and returns a formatted response.

    Returns:
        Response: A JSON response containing either the formatted emotion analysis
                  or an error message.
    
    Raises:
        ValueError: If the input text is invalid.
    """
    try:
        data = request.get_json(force=True)

        if 'statement' not in data:
            return jsonify({'error': 'Invalid text! Please try again!'}), 400

        text = data.get('statement')
        result = emotion_detector(text)

        if result['dominant_emotion'] is None:
            return jsonify({'error': 'Invalid text! Please try again!'}), 400

        formatted_response = (
            f"For the given statement, the system response is 'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, 'fear': {result['fear']}, 'joy': {result['joy']} "
            f"and 'sadness': {result['sadness']}. The dominant emotion is "
            f"{result['dominant_emotion']}."
        )
        return jsonify({'response': formatted_response})

    except ValueError:
        return jsonify({'error': 'Invalid text! Please try again!'}), 400

@app.route('/')
def index():
    """
    Route for the index page.

    This function renders the index.html template when the root URL is accessed.

    Returns:
        Response: The rendered HTML page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
