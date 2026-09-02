import cv2
import mediapipe as mp
import numpy as np
import time
import pickle
from gtts import gTTS
from playsound import playsound
import os

# Load alphabet model
alpha_model_path = "AZ09_augmented_final_model.pkl"
alpha_model, alpha_scaler = pickle.load(open(alpha_model_path, "rb"))

# Labels A–Z + 0–9
alpha_labels = [chr(i) for i in range(65, 91)] + [str(i) for i in range(10)]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
sentence = ""

prev_pred = ""
pred_start_time = 0
hold_time = 1.4  # Slightly reduced for faster response

def extract_hand_features(image):
    fv = []
    res = hands.process(image)
    hand_data = []

    if res.multi_hand_landmarks:
        for hand in res.multi_hand_landmarks[:2]:
            pts = [lm.x for lm in hand.landmark] + \
                  [lm.y for lm in hand.landmark] + \
                  [lm.z for lm in hand.landmark]
            hand_data.append(pts)

    if len(hand_data) == 1:
        hand_data.append([0] * 63)
    elif len(hand_data) == 0:
        hand_data = [[0] * 63, [0] * 63]

    fv.extend(hand_data[0] + hand_data[1])
    hand_count = len(res.multi_hand_landmarks) if res.multi_hand_landmarks else 0

    return fv, hand_count


def speak(text):
    if not text.strip():
        return
    filename = f"speech_{int(time.time())}.mp3"
    tts = gTTS(text=text, lang="en", tld="co.in")
    tts.save(filename)
    playsound(filename)
    os.remove(filename)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    features, hand_count = extract_hand_features(rgb)

    if hand_count == 0:
        current_pred = ""
        prev_pred = ""
        pred_start_time = time.time()
    else:
        X = np.array(features).reshape(1, -1)
        current_pred = alpha_model.predict(alpha_scaler.transform(X))[0]

        if current_pred != prev_pred:
            prev_pred = current_pred
            pred_start_time = time.time()

        if time.time() - pred_start_time >= hold_time:
            sentence += current_pred
            prev_pred = ""
            pred_start_time = time.time()

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    if key == 8:
        sentence = sentence[:-1]

    if key == 32:
        sentence += " "

    if key == ord('s'):
        print("Speaking:", sentence)
        speak(sentence)

    cv2.putText(frame, f"PRED: {current_pred}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"OUT: {sentence}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("ISL → Speech", frame)

cap.release()
cv2.destroyAllWindows()
