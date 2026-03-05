# Quick Start Guide - Hand Gesture Recognition

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

**On Windows:**
```bash
# Double-click setup.bat
# OR manually run:
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**On macOS/Linux:**
```bash
# Give permission and run:
chmod +x setup.sh
./setup.sh

# OR manually run:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run the Application (1 minute)

**After activation, run:**
```bash
python app.py
```

**Expected output:**
```
* Running on http://0.0.0.0:5000
```

### Step 3: Access the Web Interface (1 minute)

**Open your browser and go to:**
```
http://localhost:5000
```

### Step 4: Test the Application (1 minute)

1. **Live Camera Tab:**
   - Click "Live Camera"
   - Allow browser to access your webcam
   - Make hand gestures (peace sign, rock, etc.)
   - See real-time detection

2. **Upload Image Tab:**
   - Click "Upload Image"
   - Drag & drop a photo with hands
   - View detected gestures

3. **Gesture Guide Tab:**
   - Click "Gesture Guide"
   - See all 9 supported gestures

---

## 🎯 Next Steps

1. **Test different gestures** in the gesture guide
2. **Check the console output** for detection details
3. **Upload test images** to see how the model performs
4. **Review the code** to understand gesture detection logic
5. **Customize and extend** the gesture recognition

---

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| Camera permission denied | Allow camera in browser settings |
| Port 5000 already in use | Change port in `app.py` line: `app.run(debug=True, port=5001)` |
| Memory error | Close other applications, reduce resolution |
| Can't find module | Ensure virtual environment is activated |
| Module not found | Run `pip install -r requirements.txt` again |

---

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server and routes |
| `gesture_detector.py` | Hand detection and gesture recognition logic |
| `templates/index.html` | Web interface with tabs and controls |
| `requirements.txt` | Python package dependencies |
| `README.md` | Full documentation |
| `setup.sh` / `setup.bat` | Automated setup scripts |

---

## 💡 Tips for Best Results

✅ **Good lighting** in the room
✅ **Keep hands fully visible** in frame
✅ **Make clear, distinct gestures**
✅ **Position hands 1-2 feet** from camera
✅ **Avoid shadows** on hands
✅ **Single or dual-hand gestures** supported

---

## 🚀 Running in Production

For production deployment, change `debug=True` to `debug=False` in app.py and use a production server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Ready to go?** Run `python app.py` now! 🤚
