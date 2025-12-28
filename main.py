from flask import Flask, request, render_template, jsonify
from google import genai
import re

client = genai.Client(api_key="YOUR_API_KEY")
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

def classify_subject_ai(question):
    """
    AI classifies the subject strictly into:
    Physics, Chemistry, or Other
    """
    classification_prompt = f"""
    You are a subject classifier.

    Classify the following question into ONE category only:
    - Physics
    - Chemistry
    - Other

    Question: "{question}"

    Reply with ONLY one word: Physics, Chemistry, or Other
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=classification_prompt
    )

    return response.text.strip().lower()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # Name question
    if re.search(r"(your name|who are you|what is your name)", user_message.lower()):
        return jsonify({
            "reply": "im jarvis currently working as phy and chem chatbot"
        })

    # AI subject classification
    subject = classify_subject_ai(user_message)

    if subject not in ["physics", "chemistry"]:
        return jsonify({
            "reply": "i can help with physics and chemistry only ask me phy or chem questions"
        })

    # Answer generation
    answer_prompt = f"""
    You are Jarvis, a Physics and Chemistry chatbot.
    Answer the following {subject} question clearly and correctly.

    Question: {user_message}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=answer_prompt
    )

    return jsonify({"reply": response.text})

app.run(port=8001, debug=True)
