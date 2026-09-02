import os
import cv2
import numpy as np
import ffmpeg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "Friend_ISL_Project", "ISL_Dataset")

sentences_folder = os.path.join(DATASET_DIR, "Sentence_folder")
words_folder = os.path.join(DATASET_DIR, "Words_folder")
letters_folder = os.path.join(DATASET_DIR, "Letters")
numbers_folder = os.path.join(DATASET_DIR, "Numbers")

OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUT")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FPS = 25
FRAME_SIZE = (640, 480)


def _find_video(folder, name):
    name = name.strip()
    if not name:
        return None
    
    candidates = [name, name.lower(), name.upper(), name.capitalize()]
    extensions = [".mp4", ".MP4", ".mov", ".webm"]

    for cand in candidates:
        for ext in extensions:
            path = os.path.join(folder, cand + ext)
            if os.path.exists(path):
                return path

    return None


def _find_letter(ch):
    ch = ch.upper()
    if not ch.isalpha():
        return None

    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(letters_folder, ch + ext)
        if os.path.exists(path):
            return path

    return None


def _find_digit(ch):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(numbers_folder, ch + ext)
        if os.path.exists(path):
            return path
    return None


def _build_segments(text):
    text = text.strip().lower()
    segments = []
    words = text.split()

    # Filter empty words
    words = [w for w in words if w]

    i = 0
    while i < len(words):

        found = False

        # Try longest match first (Sentences)
        for j in range(len(words), i, -1):
            phrase = " ".join(words[i:j])
            phrase_video = _find_video(sentences_folder, phrase)
            if phrase_video:
                segments.append(("video", phrase_video))
                i = j
                found = True
                break

        if found:
            continue

        # Try word-level videos
        word = words[i]
        word_video = _find_video(words_folder, word)
        if word_video:
            segments.append(("video", word_video))
            i += 1
            continue

        # Fallback to spelling
        for ch in word:
            if ch == " ":
                blank = os.path.join(letters_folder, "blank.jpg")
                if os.path.exists(blank):
                    segments.append(("image", blank, 0.4))
                continue

            img_path = None
            if ch.isalpha():
                img_path = _find_letter(ch)
            elif ch.isdigit():
                img_path = _find_digit(ch)

            if img_path:
                segments.append(("image", img_path, 0.5))

        i += 1

    return segments



def _write_video(segments, out_path):
    process = (
        ffmpeg
        .input("pipe:", format="rawvideo", pix_fmt="rgb24",
               s=f"{FRAME_SIZE[0]}x{FRAME_SIZE[1]}")
        .output(out_path, vcodec="libx264", pix_fmt="yuv420p",
                r=FPS, movflags="+faststart")
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    total_frames = 0

    for seg in segments:
        if seg[0] == "video":
            cap = cv2.VideoCapture(seg[1])
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, FRAME_SIZE)
                process.stdin.write(frame.astype(np.uint8).tobytes())
                total_frames += 1
            cap.release()

        elif seg[0] == "image":
            img = cv2.imread(seg[1])
            if img is None:
                continue
            img = cv2.resize(img, FRAME_SIZE)
            repeat = int(FPS * seg[2])
            for _ in range(repeat):
                process.stdin.write(img.astype(np.uint8).tobytes())
                total_frames += 1

    process.stdin.close()
    process.wait()

    print(f"Total Frames Encoded: {total_frames}")
    print("Output saved:", out_path)


def generate_isl_video(text, output_name="isl_output.mp4"):
    text = text.strip()
    if not text:
        raise ValueError("No text provided")

    print("Generating ISL for:", text)

    segments = _build_segments(text)
    if not segments:
        raise RuntimeError("No valid ISL segments found")

    out_path = os.path.join(OUTPUT_DIR, output_name)
    _write_video(segments, out_path)

    if not os.path.exists(out_path):
        raise RuntimeError("Video write failed!")

    print("Video Generated →", out_path)
    return out_path
