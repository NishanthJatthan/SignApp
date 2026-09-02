from flask import Flask, render_template, Response, request, send_file, jsonify, make_response
import cv2
import numpy as np
import mediapipe as mp
import pickle
import time
import os
from text_to_isl_newww import generate_isl_video
from gtts import gTTS
import uuid

app = Flask(__name__)

# ===================== ISL → SPEECH MODEL =====================
alpha_model_path = "AZ09_augmented_final_model.pkl"
alpha_model, alpha_scaler = pickle.load(open(alpha_model_path, "rb"))

labels = [chr(i) for i in range(65, 91)] + [str(i) for i in range(10)]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

current_pred = ""
sentence = ""
prev_pred = ""
pred_start_time = time.time()
hold_time = 1.2  # seconds to confirm a gesture


def extract_keypoints(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)
    fv = []

    if res.multi_hand_landmarks:
        for hand in res.multi_hand_landmarks[:2]:
            pts = []
            for lm in hand.landmark:
                pts.extend([lm.x, lm.y, lm.z])
            fv.append(pts)

    if len(fv) == 1:
        fv.append([0] * 63)
    elif len(fv) == 0:
        fv = [[0] * 63, [0] * 63]

    count = len(res.multi_hand_landmarks) if res.multi_hand_landmarks else 0
    return fv[0] + fv[1], count


def generate_frames():
    global current_pred, sentence, prev_pred, pred_start_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        features, count = extract_keypoints(frame)

        if count > 0:
            X = np.array(features).reshape(1, -1)
            pred = alpha_model.predict(alpha_scaler.transform(X))[0]

            if pred != prev_pred:
                prev_pred = pred
                pred_start_time = time.time()

            if time.time() - pred_start_time >= hold_time:
                sentence += pred
                prev_pred = ""
                pred_start_time = time.time()

            current_pred = pred
        else:
            current_pred = ""

        cv2.putText(
            frame,
            f"PRED: {current_pred}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"OUT: {sentence}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame_bytes +
            b"\r\n"
        )


# ===================== ISL → SPEECH SUPPORT ROUTES =====================

@app.route("/status")
def status():
    return jsonify({"prediction": current_pred, "sentence": sentence})


@app.route("/update_sentence", methods=["POST"])
def update_sentence():
    global sentence
    action = request.json.get("action", "")

    if action == "space":
        sentence += " "
    elif action == "backspace":
        sentence = sentence[:-1] if sentence else ""
    elif action == "clear":
        sentence = ""

    return jsonify({"sentence": sentence})


@app.route("/speak_text", methods=["POST"])
def speak_text():
    """
    Uses gTTS to generate an MP3 for the current sentence.
    Frontend will receive the URL and play it.
    """
    global sentence
    text = sentence.strip()

    if not text:
        return jsonify({"audio": None})

    folder = os.path.join("static", "tts")
    os.makedirs(folder, exist_ok=True)

    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)

    tts = gTTS(text=text, lang="en", tld="co.in")
    tts.save(filepath)

    return jsonify({"audio": f"/static/tts/{filename}"})


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ===================== SPEECH → ISL =====================
last_video_path = None


@app.route("/speech_to_isl", methods=["GET", "POST"])
def speech_to_isl():
    """
    This route renders the dual-pane page and also handles
    POST for Speech → ISL video generation.
    """
    global last_video_path
    video_ready = False
    error_msg = ""

    if request.method == "POST":
        text = request.form.get("text_input", "").strip()

        if not text:
            error_msg = "Please speak or type something."
        else:
            try:
                last_video_path = generate_isl_video(text)
                video_ready = True
            except Exception as e:
                error_msg = str(e)

    return render_template(
        "speech_to_isl.html",
        video_ready=video_ready,
        error_msg=error_msg,
        time=int(time.time())
    )


@app.route("/isl_video")
def isl_video():
    if last_video_path and os.path.exists(last_video_path):
        response = make_response(send_file(last_video_path))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Content-Type"] = "video/mp4"
        response.headers["Accept-Ranges"] = "bytes"
        return response

    return "No video available", 404


# ===================== PAGE ROUTES =====================

@app.route("/")
def index():
    """
    Make the dual-pane page the HOME page.
    We just render the same template as speech_to_isl(),
    but without trying to generate a video.
    """
    return render_template(
        "speech_to_isl.html",
        video_ready=False,
        error_msg="",
        time=int(time.time())
    )


@app.route("/isl_to_speech")
def isl_to_speech():
    """
    Legacy route – if you still have a separate ISL→Speech page (old UI),
    you can keep this. If not needed, you can delete the template and this route.
    """
    return render_template("isl_to_speech.html")


# ===================== MAIN =====================

if __name__ == "__main__":
    app.run(debug=True)
