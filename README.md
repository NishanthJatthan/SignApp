# Vani-Drishti: Speech ↔ Indian Sign Language Bridge

A web application that bridges communication between spoken/typed language and Indian Sign Language (ISL) using deep learning and computer vision.

## Features

1. **Speech → ISL**: Convert speech/text to Indian Sign Language videos
   - Record speech or type text manually
   - Generate ISL videos from dataset
   - Cascading lookup: Sentence → Words → Letters/Numbers

2. **ISL → Speech**: Real-time hand gesture recognition
   - Detect hand gestures via webcam
   - Recognize A-Z letters and 0-9 digits
   - Convert recognized text to speech

## Quick Start

### Local Setup
```bash
# Clone the repository
git clone https://github.com/NishanthJatthan/SignApp.git
cd SignApp

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download model file (place in project root)
# AZ09_augmented_final_model.pkl

# Run the app
python api/app.py
```

Then open `http://localhost:5000` in your browser.

### Deploy on Vercel (Recommended)

1. Push this repository to GitHub
2. Go to https://vercel.com/dashboard
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Vercel will automatically detect Flask and deploy!

**Note**: Live webcam feed won't work on Vercel (serverless limitation). Use locally for ISL → Speech.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## System Architecture

```
User Input (Speech/Text/Hands)
         ↓
Transcription / Recognition
         ↓
ISL Video Generation
         ↓
Output (Video/Audio)
```

## Installation

### Requirements
- Python 3.8+
- FFmpeg (for video processing)
- Webcam (for ISL recognition)

### Setup Steps

1. **Clone repository**
```bash
git clone https://github.com/NishanthJatthan/SignApp.git
cd SignApp
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download model file**
   - Download `AZ09_augmented_final_model.pkl` (trained gesture recognition model)
   - Place in project root directory

5. **Verify dataset structure**
```
Friend_ISL_Project/
  ISL_Dataset/
    Sentence_folder/     (sentence videos)
    Words_folder/        (word videos)
    Letters/            (A-Z images)
    Numbers/            (0-9 images)
```

## Usage

### Web Interface (Speech → ISL)
1. Open http://localhost:5000
2. Go to "Speech → ISL" tab
3. Type a sentence or use speech recognition
4. Click "Translate to ISL"
5. Watch the generated video

### Webcam Mode (ISL → Speech)
1. Go to "ISL → Speech" tab
2. Position hands in front of camera
3. Hold gestures ~1.5 seconds to register
4. View recognized text
5. Use buttons to edit (Space, Backspace, Clear)
6. Click "Speak" to hear the text

## Project Structure

```
SignApp/
├── api/
│   ├── app.py          # Flask application
│   └── index.py        # Vercel handler
├── templates/          # HTML templates
│   ├── index.html
│   ├── speech_to_isl.html
│   └── isl_to_speech.html
├── static/            # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── img/
├── Friend_ISL_Project/
│   └── ISL_Dataset/   # Sign language videos/images
├── predict.py         # Standalone ISL prediction
├── text_to_isl_newww.py  # Video generation logic
├── requirements.txt
├── vercel.json        # Vercel deployment config
└── runtime.txt        # Python version
```

## Key Files

- **api/app.py** - Main Flask application with routes
- **predict.py** - Standalone script for webcam ISL recognition
- **text_to_isl_newww.py** - ISL video generation from text
- **templates/** - Web interface HTML
- **static/** - CSS, JavaScript, assets
- **vercel.json** - Vercel serverless configuration

## Deployment

### Vercel (Recommended for Production)
See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

### Local Development
```bash
python api/app.py
```

Visit http://localhost:5000

## Video Generation Logic

The system uses a **cascading lookup strategy**:

1. **Full Sentence Match**: Searches `Sentence_folder/` for the complete phrase
2. **Word-by-Word**: Searches `Words_folder/` for individual words
3. **Letter Fallback**: Spells out letter-by-letter using `Letters/` folder
   - Each letter: 0.8 seconds
   - Letter separator: 0.2 seconds (blank image)
   - Word separator: 0.4 seconds (blank image)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Webcam not detected** | Check permissions, ensure not in use by other apps |
| **Model not found** | Download model file and place in project root |
| **Video not generating** | Verify dataset files exist with correct naming |
| **Audio transcription fails** | Check internet connection, microphone permissions |
| **Vercel deployment fails** | Check `vercel.json`, `requirements.txt`, build logs |

## Performance Tips

- Use high-quality microphone for better speech recognition
- Good lighting for accurate hand detection
- Speak clearly at normal pace
- Hold gestures steady for 1-2 seconds

## Future Enhancements

- [ ] Support for more Indian languages
- [ ] Improved gesture recognition accuracy
- [ ] Mobile app (React Native)
- [ ] Offline mode with bundled videos
- [ ] Cloud storage for persistent outputs
- [ ] User authentication and history
- [ ] Real-time gesture feedback UI

## License

[Your License Here]

## Author

Created for the Friend ISL Project to bridge communication gaps.