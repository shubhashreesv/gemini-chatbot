from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Route for homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle chatbot queries
@app.route('/ask', methods=['POST'])
def ask():
    try:
        prompt = request.form['prompt']
        response = model.generate_content(prompt)

        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "Sorry, but I think Gemini didn't want to answer that!"})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

# 404 Error Handling (Redirect to home page)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
