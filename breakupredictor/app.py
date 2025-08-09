# import os
# import random
# from flask import Flask, request, jsonify, render_template
# from werkzeug.utils import secure_filename
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load API key
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(name, template_folder="templates", static_folder="static")
# app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
# os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# # Fallback messages
# FALLBACK_REPLIES = [
#     "💔 Ghosting level: Expert. They could teach a masterclass.",
#     "🚪 Left you on read? Even my fridge light is warmer.",
#     "📉 Love stock down 99%. Sell before bankruptcy.",
#     "🌹 Too sweet? Careful — sugar attracts ants 🐜.",
#     "🏆 Replies instantly? Congrats, you’re their full-time job 🚩",
#     "🥶 They text like ice cubes — refreshing but cold.",
#     "🪦 This relationship is running on expired vibes."
# ]

# FALLBACK_INSIGHTS = [
#     "They ignored you? ✅ Respecting your personal space forever.",
#     "They reply in 2 seconds? 🚩 Future stalker vibes.",
#     "They buy gifts daily? 🚩 Love bombing alert.",
#     "They liked their ex’s post? ✅ Encouraging open networking.",
#     "They never argue? 🚩 Fake harmony masterclass.",
#     "They said 'k'? ✅ Respecting brevity."
# ]

# def get_flag_by_score(score):
#     """Return danger rating based on score."""
#     if score > 90:
#         return "Red Forest 🌲"
#     elif score > 70:
#         return "Certified Red Flag 🚩"
#     elif score >= 40:
#         return "Yellow Flag ⚠"
#     elif score >= 20:
#         return "Green Forest 🌲✅"
#     else:
#         return "Green Flag ✅"

# def analyze_with_gemini(input_text):
#     """Send text to Gemini API and return sarcastic inverted logic prediction."""
#     model = genai.GenerativeModel("models/gemini-1.5-flash")

#     model = genai.GenerativeModel("models/gemini-1.5-flash")

#     prompt = f"""
#     You are a sarcastic breakup predictor with inverted relationship logic.

#     Important:
#     - Base your prediction ONLY on the actual conversation provided.
#     - Do NOT give the same score for different inputs. Use the context
#       to decide whether behaviors are extreme, moderate, or mild.
#     - Positive relationship behaviors should be treated as suspicious or negative.
#     - Negative behaviors should be treated as positive or 'healthy boundaries'.

#     Scoring Rules:
#       - Red Forest 🌲 if score > 90
#       - Red Flag 🚩 if score 70–90
#       - Yellow Flag ⚠ if score 40–70
#       - Green Forest 🌲✅ if score 20–40
#       - Green Flag ✅ if score 0–20

#     Output:
#     - "score" (0–100) → based on your judgment of the text.
#     - "reply" → sarcastic, short, with emojis.
#     - "danger_rating" → match exactly to the ranges above.
#     - "flipped_insights" → 3–4 bullet points turning normal into suspicious or vice versa.

#     Example Output:
#     {{
#       "score": 95,
#       "reply": "🌹 They bring you flowers daily? 🚩 Love bombing alert.",
#       "danger_rating": "Red Forest 🌲",
#       "flipped_insights": [
#         "They never fight with you? 🚩 Fake harmony.",
#         "They ghosted you? ✅ Respecting your space.",
#         "They reply instantly? 🚩 Desperation vibes."
#       ]
#     }}

#     Conversation to analyze:
#     \"\"\"{input_text}\"\"\"
#     """

#     try:
#         response = model.generate_content(prompt)
#         return eval(response.text)  # Expect strict JSON
#     except:
#         return {
#             "score": 75,
#             "reply": "🚩 Looks like they’re writing your breakup speech already.",
#             "danger_rating": "Red Flag 🚩",
#             "flipped_insights": [
#                 "They text too much? 🚩 Desperate energy.",
#                 "They ignore you? ✅ Giving you independence.",
#                 "They plan dates ahead? 🚩 Control freak vibes."
#             ]
#         }
# #
# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/api/predict", methods=["POST"])
# def predict():
#     if "image" in request.files:
#         file = request.files["image"]
#         if file.filename == "":
#             return "❌ No file selected", 400
#         filename = secure_filename(file.filename)
#         path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(path)
#         fake_text = "They reply instantly every time and keep saying 'you're perfect'."
#         result = analyze_with_gemini(fake_text)
#     else:
#         data = request.get_json()
#         text = data.get("text", "")
#         if not text:
#             return "❌ No text provided", 400
#         result = analyze_with_gemini(text)

#     # Convert dictionary to human-readable text
#     result_text = (
#         f"Score: {result['score']}\n"
#         f"Danger Rating: {result['danger_rating']}\n"
#         f"Reply: {result['reply']}\n"
#         f"Flipped Insights:\n- " + "\n- ".join(result['flipped_insights'])
#     )

#     return result_text

# if name == "main":
#     app.run(debug=True)




import os
import random
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

FALLBACK_REPLIES = [
    "💔 Ghosting level: Expert. They could teach a masterclass.",
    "🚪 Left you on read? Even my fridge light is warmer.",
    "📉 Love stock down 99%. Sell before bankruptcy.",
    "🌹 Too sweet? Careful — sugar attracts ants 🐜.",
    "🏆 Replies instantly? Congrats, you’re their full-time job 🚩",
    "🥶 They text like ice cubes — refreshing but cold.",
    "🪦 This relationship is running on expired vibes."
]

FALLBACK_INSIGHTS = [
    "They ignored you? ✅ Respecting your personal space forever.",
    "They reply in 2 seconds? 🚩 Future stalker vibes.",
    "They buy gifts daily? 🚩 Love bombing alert.",
    "They liked their ex’s post? ✅ Encouraging open networking.",
    "They never argue? 🚩 Fake harmony masterclass.",
    "They said 'k'? ✅ Respecting brevity."
]

def get_flag_by_score(score):
    if score > 90:
        return "Red Forest 🌲"
    elif score > 70:
        return "Certified Red Flag 🚩"
    elif score >= 40:
        return "Yellow Flag ⚠"
    elif score <= 20:
        return "Green Forest 🌲✅"
    else:
        return "Green Flag ✅"

import json

def analyze_with_gemini(input_text):
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = f"""
    You are a sarcastic breakup predictor with inverted relationship logic.

    Rules:
    - Predict a breakup score based on the given conversation.
    - Do NOT give the same score for different inputs — make it depend on tone and behaviors.
    - Positive behaviors = suspicious/negative.
    - Negative behaviors = positive/healthy boundaries.
    - Return ONLY valid JSON. No explanations.

    JSON format:
    {{
      "score": 0-100,
      "reply": "short sarcastic reply",
      "danger_rating": "Red Forest 🌲 / Red Flag 🚩 / Yellow Flag ⚠ / Green Forest 🌲✅ / Green Flag ✅",
      "flipped_insights": ["...", "...", "..."]
    }}

    Conversation:
    \"\"\"{input_text}\"\"\"
    """

    try:
        response = model.generate_content(prompt)
        raw_output = response.candidates[0].content.parts[0].text.strip()

        # Remove triple backticks if Gemini adds them
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").strip()
            if raw_output.lower().startswith("json"):
                raw_output = raw_output[4:].strip()

        return json.loads(raw_output)
    except Exception as e:
        print("Gemini parsing error:", e)
        return {
            "score": 75,
            "reply": "🚩 Looks like they’re writing your breakup speech already.",
            "danger_rating": "Red Flag 🚩",
            "flipped_insights": [
                "They text too much? 🚩 Desperate energy.",
                "They ignore you? ✅ Giving you independence.",
                "They plan dates ahead? 🚩 Control freak vibes."
            ]
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" in request.files:
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        fake_text = "They reply instantly every time and keep saying 'you're perfect'."
        result = analyze_with_gemini(fake_text)
    else:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        result = analyze_with_gemini(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)