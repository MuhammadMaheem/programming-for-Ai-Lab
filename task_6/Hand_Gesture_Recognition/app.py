from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from gesture_detector import GestureDetector
import threading
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global gesture detector and camera
gesture_detector = GestureDetector()
camera = None
camera_lock = threading.Lock()
current_frame = None
latest_detection = None

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream video with gesture detection."""
    def generate():
        global camera
        
        with camera_lock:
            if camera is None:
                camera = cv2.VideoCapture(0)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                camera.set(cv2.CAP_PROP_FPS, 30)
        
        while True:
            success, frame = camera.read()
            
            if not success:
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame for gesture detection
            annotated_frame, detections = gesture_detector.process_frame(frame)
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    """Stop the camera feed."""
    global camera
    
    with camera_lock:
        if camera is not None:
            camera.release()
            camera = None
    
    return jsonify({'status': 'Camera stopped'})

@app.route('/detect_image', methods=['POST'])
def detect_image():
    """Detect gestures in uploaded image."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Read image from file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
        file.save(filepath)
        
        # Read image with OpenCV
        image = cv2.imread(filepath)
        
        if image is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Detect gestures
        annotated_image, detections = gesture_detector.process_frame(image)
        
        # Save annotated image
        output_filename = f"detected_{timestamp}_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        cv2.imwrite(output_path, annotated_image)
        
        return jsonify({
            'status': 'success',
            'detections': detections,
            'image_path': f'/uploads/{output_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files."""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/gesture-info', methods=['GET'])
def gesture_info():
    """Get information about supported gestures."""
    gestures = {
        'Peace Sign': 'Index and middle fingers extended, others closed. Universal peace gesture.',
        'Rock': 'Index and pinky fingers extended, others closed. Rock and roll gesture.',
        'Paper': 'All five fingers extended. Beats rock in rock-paper-scissors.',
        'Fist': 'All fingers closed, thumb inside. Closed hand gesture.',
        'Open Hand': 'All fingers extended and spread. Open palm gesture.',
        'Thumbs Up': 'Thumb extended upward, other fingers closed.',
        'OK Sign': 'Thumb and index finger touching, others extended.',
        'Call Me': 'Thumb and pinky extended, other fingers closed. "Call me" gesture.',
        'Scissors': 'Index and middle fingers extended and separated. Scissors gesture.'
    }
    return jsonify(gestures)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.teardown_appcontext
def cleanup(exception):
    """Cleanup resources on application shutdown."""
    global camera
    with camera_lock:
        if camera is not None:
            camera.release()
    gesture_detector.cleanup()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
