from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Student Support Assistant. Answer student questions clearly and politely."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response["message"]["content"]

    except Exception as e:
        reply = str(e)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)