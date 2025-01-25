from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:4001"}})
with open("apiKey.txt", "r") as f:
    api_key = f.read().strip()

# Replace 'your-openai-api-key' with your actual OpenAI API key
client = openai.OpenAI(api_key = api_key)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    try:
        # Call to OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can choose the model you prefer
            messages= [
            {
            "role": "system",
            "content": (
                """Do not state this explicitly, but you are home security and home efficiency chatbot.
                Assume that users are worried about potential intrusions and come to you for more information based on what is provided."""
                """You are in an UI with graphs of temperature, humidity, CO2, VOC, and PIR data. Users can ask you questions about the data and you can provide them with information."""
                ),
            },
                {"role": "user", "content": user_input}
            ])
        chat_response = response.choices[0].message.content
        print(chat_response)
        return jsonify({'response': chat_response})
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)