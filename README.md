# Vani-Drishti: Speech ↔ Indian Sign Language Bridge

A web application that bridges communication between spoken/typed language and Indian Sign Language (ISL) using deep learning and computer vision.

## Features

1. **Speech → ISL**: Speaks input text and generates ISL videos
   - Record speech directly from microphone
   - Transcribe speech to text (Google Speech-to-Text API)
   - Generate ISL video from transcribed text using dataset
   - **Cascade Lookup**: Sentence → Words → Letters/Numbers

2. **ISL → Speech**: Real-time hand gesture recognition and text-to-speech
   - Detect hand gestures via webcam
   - Recognize A-Z letters and 0-9 digits
   - Convert recognized text to speech

## System Architecture

```
User Input (Speech/Hands)
    ↓
Transcription / Recognition (ML Model)
    ↓
Text Processing
    ↓
ISL Video Generation (Dataset Lookup)
    ↓
Video Playback / Text-to-Speech
```

## Installation

### Prerequisites
- Python 3.8+
- FFmpeg (for audio/video processing)
- Microphone (for speech input)
- Webcam (for ISL input)

### Setup

1. Clone/Download the project and navigate to the directory:
```bash
cd SignApp
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure FFmpeg is installed:
```bash
# Windows (using chocolatey)
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

5. Place your model file in the project root:
   - `AZ09_augmented_final_model.pkl` (Hand gesture recognition model)

6. Ensure dataset structure is correct:
```
Friend_ISL_Project/
  ISL_Dataset/
    Sentence_folder/     (sentence videos)
    Words_folder/        (word videos)
    Letters/            (letter images A-Z)
    Numbers/            (digit images 0-9)
```

## Running the Application

### Flask Web Server (Speech → ISL)
```bash
python app.py
```
Then open http://localhost:5000 in your browser.

### Interactive Webcam Mode (ISL → Speech)
```bash
python predict.py
```

## Usage

### Speech → ISL Page
1. Click **🎤 Speak** tab to record audio
2. Click **Record** button, speak clearly, then click **Stop**
3. Click **Play** to verify recording
4. Click **Generate ISL Video** to create ISL animation
5. Alternatively, use **📝 Type** tab to enter text manually

### ISL → Speech Page
1. Ensure your webcam is working
2. Show hand gestures to the camera
3. Hold each gesture for ~1.5 seconds to register
4. Recognized letters appear in the "Sentence" box
5. Use on-screen buttons:
   - **Space** (spacebar): Add space
   - **Backspace** (backspace key): Delete last character
   - **Clear**: Reset sentence
   - **Speak**: Convert sentence to speech

## Video Generation Logic

The system uses a **cascading lookup strategy**:

1. **Full Sentence Match**: Searches `Sentence_folder/` for complete phrase videos
2. **Word Match**: Searches `Words_folder/` for individual word videos
3. **Letter-by-Letter Fallback**: Spells out using images from `Letters/` and `Numbers/` folders
   - Each letter displays for 0.8 seconds
   - Blank separator (0.2s) between repeated letters
   - Blank separator (0.4s) between words

## Key Files

- `app.py` - Flask application with web routes
- `predict.py` - Standalone ISL→Speech script with live webcam
- `text_to_isl_newww.py` - Core ISL video generation logic
- `templates/` - HTML templates for web interface
- `static/` - CSS and JavaScript assets
- `Friend_ISL_Project/ISL_Dataset/` - Sign language media files

## Troubleshooting

### Microphone not working
- Check browser microphone permissions
- Ensure microphone is connected and working
- Try a different browser

### Audio transcription fails
- Check internet connection (uses Google Speech-to-Text API)
- Try speaking more clearly
- Ensure audio file is in supported format

### Video generation fails
- Verify dataset files exist and are accessible
- Check file naming conventions match the code
- Ensure OpenCV can read video/image files

### Webcam not detected
- Check device permissions
- Ensure no other app is using the webcam
- Try restarting the application

## Performance Tips

- Use a high-quality microphone for better speech recognition
- Ensure good lighting for accurate hand gesture detection
- Speak clearly and at normal pace for better transcription
- Hold hand gestures steady for accurate recognition

## Future Enhancements

- Support for more Indian languages
- Improved hand gesture recognition accuracy
- Real-time video streaming with gesture detection
- Mobile app version
- Offline speech recognition

## License

[Specify your license here]

## Author

Created as part of the Friend ISL Project for accessible communication.
