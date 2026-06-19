from flask import Flask, request, jsonify
from chatbot import get_bot_response  
from sentiment_analysis import analyze_sentiment

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    sentiment = analyze_sentiment(user_message)
    response = get_bot_response(user_message) 
    return jsonify({"response": response, "sentiment": sentiment})

if __name__ == '__main__':
    app.run(debug=True)


    