from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os, random

app = Flask(__name__, template_folder='templates', static_folder='static')

# config: limit upload size to 5MB and set upload folder
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    # serves templates/index.html
    return render_template('index.html')


@app.route('/api/ping')
def ping():
    # simple test endpoint
    return jsonify({"status": "ok"})


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Accepts either:
    - a file upload in form field 'image' (multipart/form-data)
    - or JSON payload with {"text": "..."}
    Returns JSON with a fake 'score' and sarcastic reply.
    """
    # 1) If an image file is posted:
    if 'image' in request.files:
        f = request.files['image']
        if f.filename == '':
            return jsonify({"error": "no file selected"}), 400
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)                      # save to uploads/
        # fake analysis: score based on filename length + random
        score = (len(filename) * 7 + random.randint(0, 30)) % 101
        source = "image"

    else:
        # 2) Try reading JSON (Content-Type: application/json)
        data = request.get_json(silent=True) or {}
        text = data.get('text', '')
        # fake analysis: score based on text length + random
        score = min(100, len(text) + random.randint(0, 30))
        source = "text"

    # choose a sarcastic reply based on score
    if score >= 80:
        reply = "Oof. This chat screams 'it's not you, it's definitely them.' Run."
    elif score >= 45:
        reply = "Hmm. Caution: patchable with biryani and apologies."
    else:
        reply = "You're safe—for now. Maybe don't send the first 3 texts."

    return jsonify({"score": int(score), "reply": reply, "source": source})


if __name__ == '__main__':
    # run server locally, port 5000
    app.run(debug=True)
