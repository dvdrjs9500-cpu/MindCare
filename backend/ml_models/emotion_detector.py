"""
Emotion Detection Module using MediaPipe Face Detection + Feature Extraction
Detects facial emotions and correlates with depression indicators
"""

import cv2
import numpy as np
from pathlib import Path
try:
    import mediapipe as mp
except ImportError:
    mp = None


class EmotionDetector:
    """
    Detects emotions from video/image using MediaPipe face mesh
    and simple feature extraction to estimate depression likelihood
    """
    
    def __init__(self):
        if mp is None:
            raise ImportError("MediaPipe not installed. Install with: pip install mediapipe")
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        
        # Emotion scores based on facial landmarks
        self.emotion_history = []
    
    def analyze_face_landmarks(self, landmarks, image_width, image_height):
        """
        Analyze facial landmarks and extract emotion indicators
        
        Args:
            landmarks: MediaPipe face landmarks (468 points)
            image_width, image_height: Image dimensions
        
        Returns:
            dict with emotion scores
        """
        if landmarks is None:
            return None
        
        # Extract key landmark positions
        mouth_left = landmarks[61]  # Left mouth corner
        mouth_right = landmarks[291]  # Right mouth corner
        mouth_top = landmarks[13]  # Mouth top
        mouth_bottom = landmarks[14]  # Mouth bottom
        
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        
        # Calculate mouth openness (smile indicator)
        mouth_height = abs(mouth_top.y - mouth_bottom.y) * image_height
        mouth_width = abs(mouth_left.x - mouth_right.x) * image_width
        mouth_aspect_ratio = mouth_height / (mouth_width + 0.001)
        
        # Calculate eye openness (fatigue/sadness indicator)
        left_eye_height = abs(left_eye_top.y - left_eye_bottom.y) * image_height
        right_eye_height = abs(right_eye_top.y - right_eye_bottom.y) * image_height
        eye_aspect_ratio = (left_eye_height + right_eye_height) / 2
        
        # Estimate emotions (simplified)
        emotions = {
            'happy': min(1.0, max(0.0, mouth_aspect_ratio * 5)),  # Higher ratio = more smile
            'sad': 1.0 - min(1.0, max(0.0, mouth_aspect_ratio * 3)),  # Lower mouth movement
            'neutral': 0.5,  # Default neutral
            'tired': 1.0 - min(1.0, max(0.0, eye_aspect_ratio * 3)),  # Lower eyes = tired
            'surprised': min(1.0, max(0.0, (mouth_aspect_ratio + eye_aspect_ratio) * 2))
        }
        
        return emotions
    
    def detect_from_frame(self, frame):
        """
        Detect emotions from a video frame
        
        Args:
            frame: OpenCV video frame (BGR)
        
        Returns:
            dict with emotion analysis
        """
        if frame is None:
            return None
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        
        # Detect face landmarks
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return {'detected': False, 'emotions': None}
        
        landmarks = results.multi_face_landmarks[0].landmark
        emotions = self.analyze_face_landmarks(landmarks, w, h)
        
        self.emotion_history.append(emotions)
        
        return {
            'detected': True,
            'emotions': emotions,
            'frame_emotion': self._get_dominant_emotion(emotions)
        }
    
    def detect_from_video(self, video_path, sample_frames=10):
        """
        Analyze emotions throughout a video
        
        Args:
            video_path: Path to video file
            sample_frames: Number of frames to sample from video
        
        Returns:
            dict with video-level emotion analysis
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            raise ValueError("Could not read video frames")
        
        frame_indices = np.linspace(0, total_frames - 1, sample_frames, dtype=int)
        all_emotions = []
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                continue
            
            result = self.detect_from_frame(frame)
            if result['detected']:
                all_emotions.append(result['emotions'])
        
        cap.release()
        
        # Calculate aggregate statistics
        if not all_emotions:
            return {'detected': False, 'message': 'No faces detected in video'}
        
        emotion_aggregates = self._aggregate_emotions(all_emotions)
        depression_score = self._calculate_depression_score(emotion_aggregates)
        
        return {
            'detected': True,
            'frames_analyzed': len(all_emotions),
            'emotion_averages': emotion_aggregates,
            'dominant_emotion': self._get_dominant_emotion(emotion_aggregates),
            'depression_score': depression_score,
            'depression_level': self._get_depression_level(depression_score)
        }
    
    @staticmethod
    def _get_dominant_emotion(emotions):
        """Get emotion with highest score"""
        if not emotions:
            return None
        return max(emotions.items(), key=lambda x: x[1])[0]
    
    @staticmethod
    def _aggregate_emotions(emotion_list):
        """Calculate average emotions across frames"""
        if not emotion_list:
            return {}
        
        emotion_names = emotion_list[0].keys()
        return {
            emotion: np.mean([e[emotion] for e in emotion_list])
            for emotion in emotion_names
        }
    
    @staticmethod
    def _calculate_depression_score(emotions):
        """
        Calculate depression likelihood from facial emotions (0-100)
        Higher = more likely depressed
        """
        sad_weight = emotions.get('sad', 0) * 0.4
        tired_weight = emotions.get('tired', 0) * 0.3
        neutral_weight = emotions.get('neutral', 0) * 0.2
        happy_negative = (1 - emotions.get('happy', 0.5)) * 0.1
        
        score = (sad_weight + tired_weight + neutral_weight + happy_negative) * 100
        return min(100, max(0, score))  # Clamp 0-100
    
    @staticmethod
    def _get_depression_level(score):
        """Convert depression score to level"""
        if score < 20:
            return 'NONE'
        elif score < 40:
            return 'MILD'
        elif score < 60:
            return 'MODERATE'
        else:
            return 'SEVERE'


def detect_from_video(video_path):
    """Convenience function for video emotion detection"""
    detector = EmotionDetector()
    return detector.detect_from_video(video_path)


def detect_from_frame(frame):
    """Convenience function for single frame emotion detection"""
    detector = EmotionDetector()
    return detector.detect_from_frame(frame)
