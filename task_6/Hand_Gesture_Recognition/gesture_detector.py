import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import math

class GestureDetector:
    """
    Hand Gesture Recognition using MediaPipe and OpenCV.
    Detects multiple hand gestures including thumbs up, peace sign, rock, paper, scissors, ok sign, etc.
    """
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.gesture_history = deque(maxlen=5)  # Store last 5 gestures for smoothing
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_finger_extended(self, landmarks, finger_tip, finger_pip):
        """Check if a finger is extended (tip is above PIP joint)."""
        return landmarks[finger_tip].y < landmarks[finger_pip].y
    
    def count_extended_fingers(self, landmarks):
        """Count how many fingers are extended."""
        fingers_extended = 0
        
        # Thumb (special case - check x coordinate)
        if landmarks[4].x < landmarks[3].x:  # Right hand
            fingers_extended += 1
        elif landmarks[4].x > landmarks[3].x:  # Left hand
            fingers_extended += 1
            
        # Other four fingers
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if self.is_finger_extended(landmarks, tip, pip):
                fingers_extended += 1
                
        return fingers_extended
    
    def is_pinching(self, landmarks, finger_tip, thumb_tip=4, threshold=0.05):
        """Check if a finger is pinching the thumb."""
        distance = self.calculate_distance(
            (landmarks[finger_tip].x, landmarks[finger_tip].y),
            (landmarks[thumb_tip].x, landmarks[thumb_tip].y)
        )
        return distance < threshold
    
    def recognize_gesture(self, landmarks, handedness):
        """Recognize hand gesture from landmarks."""
        if landmarks is None:
            return "Unknown"
        
        fingers_extended = self.count_extended_fingers(landmarks)
        
        # Check for specific gestures
        # Thumbs up/down
        thumb_y = landmarks[4].y
        thumb_ip = landmarks[3].y
        if thumb_y < thumb_ip and self.count_extended_fingers(landmarks) == 1:
            return "Thumbs Up"
        
        # Peace sign (index and middle extended, others closed)
        if fingers_extended == 2:
            index_extended = self.is_finger_extended(landmarks, 8, 6)
            middle_extended = self.is_finger_extended(landmarks, 12, 10)
            if index_extended and middle_extended:
                return "Peace Sign"
        
        # Rock gesture (index and pinky extended, middle and ring closed)
        if fingers_extended == 2:
            index_extended = self.is_finger_extended(landmarks, 8, 6)
            pinky_extended = self.is_finger_extended(landmarks, 20, 18)
            if index_extended and pinky_extended:
                return "Rock"
        
        # Paper (all extended)
        if fingers_extended == 5:
            return "Paper"
        
        # Scissors (index and middle extended, others closed)
        if fingers_extended == 2:
            return "Scissors"
        
        # OK sign (thumb and index pinching, others extended)
        if self.is_pinching(landmarks, 8):  # index
            if self.count_extended_fingers(landmarks) == 4:
                return "OK Sign"
        
        # Fist (no fingers extended)
        if fingers_extended == 0:
            return "Fist"
        
        # Open hand (all fingers extended)
        if fingers_extended == 5:
            return "Open Hand"
        
        # Call me gesture (thumb and pinky extended)
        thumb_extended = (landmarks[4].x < landmarks[3].x or landmarks[4].x > landmarks[3].x)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18)
        if thumb_extended and pinky_extended and fingers_extended == 2:
            return "Call Me"
        
        return f"Gesture {fingers_extended}"
    
    def process_frame(self, frame):
        """Process a single frame and detect hand gestures."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        detected_gestures = []
        annotated_frame = frame.copy()
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Recognize gesture
                gesture = self.recognize_gesture(hand_landmarks.landmark, handedness.classification[0].label)
                detected_gestures.append({
                    'gesture': gesture,
                    'handedness': handedness.classification[0].label,
                    'confidence': handedness.classification[0].score
                })
                
                # Add text annotation
                h, w, c = annotated_frame.shape
                text = f"{handedness.classification[0].label}: {gesture}"
                cv2.putText(annotated_frame, text, (10, 30 + 40 * len(detected_gestures)),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return annotated_frame, detected_gestures
    
    def cleanup(self):
        """Release resources."""
        self.hands.close()
