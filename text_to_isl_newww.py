"""
Generate ISL videos from text using cascading lookup strategy.
"""
import cv2
import numpy as np
import os
from pathlib import Path
import uuid

# Base dataset path
BASE_DATASET_PATH = "Friend_ISL_Project/ISL_Dataset"
OUTPUT_DIR = "OUTPUT"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_video_path(name):
    """Get full path to video file."""
    video_path = os.path.join(BASE_DATASET_PATH, "Sentence_folder", f"{name}.mp4")
    if os.path.exists(video_path):
        return video_path
    
    video_path = os.path.join(BASE_DATASET_PATH, "Words_folder", f"{name}.mp4")
    if os.path.exists(video_path):
        return video_path
    
    return None


def get_letter_image_path(letter):
    """Get path to letter image."""
    letter_path = os.path.join(BASE_DATASET_PATH, "Letters", f"{letter.upper()}.jpg")
    if os.path.exists(letter_path):
        return letter_path
    
    # Fallback to blank
    blank_path = os.path.join(BASE_DATASET_PATH, "Letters", "blank.jpg")
    if os.path.exists(blank_path):
        return blank_path
    return None


def get_number_image_path(num):
    """Get path to number image."""
    num_path = os.path.join(BASE_DATASET_PATH, "Numbers", f"{num}.jpg")
    if os.path.exists(num_path):
        return num_path
    
    # Fallback to blank
    blank_path = os.path.join(BASE_DATASET_PATH, "Numbers", "blank.jpg")
    if os.path.exists(blank_path):
        return blank_path
    return None


def create_video_from_images(image_paths, output_path, fps=5, duration_per_image=0.8):
    """Create video from sequence of images."""
    if not image_paths:
        raise ValueError("No images provided")
    
    # Read first image to get dimensions
    first_img = cv2.imread(image_paths[0])
    if first_img is None:
        raise ValueError(f"Cannot read image: {image_paths[0]}")
    
    h, w, _ = first_img.shape
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    
    # Write each image
    frames_per_image = int(fps * duration_per_image)
    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        # Resize to match first image
        img = cv2.resize(img, (w, h))
        
        for _ in range(frames_per_image):
            out.write(img)
    
    out.release()
    return output_path


def concatenate_videos(video_paths, output_path, fps=25):
    """Concatenate multiple videos into one."""
    if not video_paths:
        raise ValueError("No videos provided")
    
    # Read all videos and concatenate frames
    all_frames = []
    video_shape = None
    
    for video_path in video_paths:
        if not os.path.exists(video_path):
            continue
        
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            all_frames.append(frame)
            if video_shape is None:
                video_shape = frame.shape
        cap.release()
    
    if not all_frames:
        raise ValueError("No valid frames extracted from videos")
    
    # Write concatenated video
    h, w, _ = video_shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    
    for frame in all_frames:
        # Resize to match first frame
        frame = cv2.resize(frame, (w, h))
        out.write(frame)
    
    out.release()
    return output_path


def generate_isl_video(text):
    """
    Generate ISL video from text using cascading strategy:
    1. Try full sentence
    2. Try each word individually
    3. Fall back to letter-by-letter spelling
    """
    text = text.strip().upper()
    if not text:
        raise ValueError("Empty text provided")
    
    output_file = os.path.join(OUTPUT_DIR, f"isl_{uuid.uuid4().hex}.mp4")
    
    # Try full sentence first
    full_sentence_path = get_video_path(text)
    if full_sentence_path:
        # Copy or create symlink
        cap = cv2.VideoCapture(full_sentence_path)
        if cap.isOpened():
            return create_copy_video(full_sentence_path, output_file)
    
    # Split into words and try word-by-word
    words = text.split()
    video_files = []
    
    for word in words:
        word_video = get_video_path(word)
        if word_video:
            video_files.append(word_video)
        else:
            # Fall back to letter-by-letter for this word
            letter_images = []
            for i, char in enumerate(word):
                if char.isalpha():
                    img_path = get_letter_image_path(char)
                elif char.isdigit():
                    img_path = get_number_image_path(char)
                else:
                    continue
                
                if img_path:
                    letter_images.append(img_path)
                
                # Add separator between letters (unless last char)
                if i < len(word) - 1:
                    blank_path = os.path.join(BASE_DATASET_PATH, "Letters", "blank.jpg")
                    if os.path.exists(blank_path):
                        letter_images.append(blank_path)
            
            if letter_images:
                word_video = os.path.join(OUTPUT_DIR, f"word_{uuid.uuid4().hex}.mp4")
                create_video_from_images(letter_images, word_video)
                video_files.append(word_video)
        
        # Add word separator blank video if not last word
        if words.index(word) < len(words) - 1:
            blank_path = os.path.join(BASE_DATASET_PATH, "Letters", "blank.jpg")
            if os.path.exists(blank_path):
                blank_video = os.path.join(OUTPUT_DIR, f"blank_{uuid.uuid4().hex}.mp4")
                create_video_from_images([blank_path] * 2, blank_video, duration_per_image=0.4)
                video_files.append(blank_video)
    
    if not video_files:
        raise ValueError("Could not generate video: no valid content")
    
    if len(video_files) == 1:
        return create_copy_video(video_files[0], output_file)
    else:
        return concatenate_videos(video_files, output_file)


def create_copy_video(source, destination):
    """Copy video file to destination."""
    import shutil
    shutil.copy2(source, destination)
    return destination


if __name__ == "__main__":
    # Test
    try:
        result = generate_isl_video("HELLO")
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: {e}")
