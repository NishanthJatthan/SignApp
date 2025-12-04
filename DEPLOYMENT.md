# Vercel Deployment Guide

## Prerequisites
- Vercel account (free at https://vercel.com)
- Git installed
- GitHub account with this repository

## Deployment Steps

### 1. Install Vercel CLI (Optional, but recommended)
```bash
npm install -g vercel
```

### 2. Connect to Vercel (via Web UI - Easiest)
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Select "Import Git Repository"
4. Enter: `https://github.com/NishanthJatthan/SignApp`
5. Click "Import"

### 3. Configure Environment Variables
In the Vercel dashboard, go to project Settings → Environment Variables and add:
```
FLASK_ENV=production
FLASK_DEBUG=0
```

### 4. Deploy
Click "Deploy" button. Vercel will:
- Install dependencies from `requirements.txt`
- Build the project using `vercel.json` config
- Deploy the Flask app as serverless functions

### 5. Access Your App
Your app will be live at: `https://<your-project>.vercel.app`

## Important Notes

### Limitations on Vercel (Serverless)
- **Webcam video feed** (`/video_feed`): Will NOT work on Vercel. This requires persistent server connection.
  - ISL → Speech page will not display live camera feed
  - Use locally: `python api/app.py` for development
  
- **File uploads/outputs**: Temporary files (TTS audio, generated videos) stored in `/tmp` are deleted after each request
  - Consider integrating cloud storage (AWS S3, GCS) for persistence

### What DOES Work on Vercel
- Speech → ISL conversion (text input, video generation)
- Web interface (HTML, CSS, JS)
- API routes (POST/GET)
- gTTS audio generation (temporary storage)

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python api/app.py
```
Or for ISL recognition:
```bash
python predict.py
```

### 3. Test Before Deploying
Visit `http://localhost:5000`

## Troubleshooting

### "Module not found" errors
- Ensure all imports use relative paths
- Check `requirements.txt` has all dependencies
- Verify file structure matches `vercel.json` routes

### Video not generating
- Check dataset files exist in `Friend_ISL_Project/ISL_Dataset/`
- Verify OpenCV can read files
- Check Vercel build logs

### gTTS not working
- Requires internet connection
- Check firewall/proxy settings
- gTTS may be blocked in some regions

## Next Steps

1. **Add Authentication**: Implement user login for privacy
2. **Database**: Store user sessions and history (Firebase, MongoDB)
3. **Cloud Storage**: Use AWS S3/GCS for persistent video storage
4. **Mobile App**: Create React Native version
5. **Offline Mode**: Bundle pre-recorded videos for offline use

## Support

For issues, check:
- Vercel Documentation: https://vercel.com/docs
- Flask Deployment: https://flask.palletsprojects.com/deployment/
- GitHub Issues: Report bugs here
