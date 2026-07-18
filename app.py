from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load .env file
load_dotenv()

app = Flask(__name__)

# OpenRouter Client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    max_retries = 3
    reply = "Something went wrong. Please try again."

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                max_tokens=300,
                temperature=0.7,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an AI Student Support Assistant.

You can answer only student-related questions like:
- Admissions
- Courses
- Fees
- Attendance
- Scholarships
- College Facilities
- Exams
- Timetable

If the question is not related to students or education, politely reply:
'I am a Student Support AI Assistant and I can answer only student-related questions.'
"""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            reply = response.choices[0].message.content
            break  # success, stop retrying

        except Exception as e:
            error_str = str(e)
            if "429" in error_str and attempt < max_retries - 1:
                time.sleep(3)
                continue
            else:
                reply = error_str

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)