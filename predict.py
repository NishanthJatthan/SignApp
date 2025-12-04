"""
Predict ISL from hand gestures in real-time.
"""
import cv2
import numpy as np
import mediapipe as mp
import pickle
import time

# Load the model
with open("AZ09_augmented_final_model.pkl", "rb") as f:
    model, scaler = pickle.load(f)

labels = [chr(i) for i in range(65, 91)] + [str(i) for i in range(10)]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

sentence = ""
current_pred = ""
prev_pred = ""
pred_start_time = time.time()
hold_time = 1.2


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


def main():
    global sentence, current_pred, prev_pred, pred_start_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        features, count = extract_keypoints(frame)

        if count > 0:
            X = np.array(features).reshape(1, -1)
            pred = model.predict(scaler.transform(X))[0]

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

        cv2.putText(frame, f"PRED: {current_pred}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"OUT: {sentence}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'C' to clear, 'Q' to quit", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("ISL Prediction", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            sentence = ""

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
