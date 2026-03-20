"""
Quiz Scoring Module using Naive Bayes Classification
Scores depression severity based on PHQ-9 assessment answers
"""

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler


class QuizScorer:
    """Naive Bayes classifier for depression assessment scoring"""
    
    def __init__(self):
        self.model = GaussianNB()
        self.scaler = StandardScaler()
        self.is_trained = False
        self._train_model()
    
    def _train_model(self):
        """Train Naive Bayes model with synthetic depression assessment data"""
        # Synthetic training data: 100 samples with 9 features (PHQ-9 questions)
        # Each feature ranges from 0-3 (0=Not at all, 1=Several days, 2=More than half, 3=Nearly every day)
        
        # Generate synthetic training data
        np.random.seed(42)
        
        # Non-depressed samples (low scores)
        non_depressed = np.random.randint(0, 2, size=(25, 9))
        non_depressed_labels = np.array([0] * 25)
        
        # Mild depression samples (moderate scores)
        mild_depressed = np.random.randint(1, 3, size=(25, 9))
        mild_depressed_labels = np.array([1] * 25)
        
        # Moderate depression samples (higher scores)
        moderate_depressed = np.random.randint(2, 4, size=(25, 9))
        moderate_depressed_labels = np.array([2] * 25)
        
        # Severe depression samples (very high scores)
        severe_depressed = np.full((25, 9), 3) - np.random.randint(0, 2, size=(25, 9))
        severe_depressed_labels = np.array([3] * 25)
        
        # Combine all data
        X = np.vstack([non_depressed, mild_depressed, moderate_depressed, severe_depressed])
        y = np.hstack([non_depressed_labels, mild_depressed_labels, 
                      moderate_depressed_labels, severe_depressed_labels])
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def score_responses(self, responses):
        """
        Score quiz responses and return diagnosis
        
        Args:
            responses: List of 9 integer values (0-3) representing PHQ-9 answers
        
        Returns:
            dict with keys:
                - diagnosis: 'NONE', 'MILD', 'MODERATE', 'SEVERE'
                - confidence: float 0-1
                - score: total score
                - percentage: score as percentage of max possible
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        
        if len(responses) != 9:
            raise ValueError("PHQ-9 requires exactly 9 responses")
        
        # Validate response values
        for response in responses:
            if not isinstance(response, (int, float)) or response < 0 or response > 3:
                raise ValueError("Each response must be an integer 0-3")
        
        # Prepare input
        X = np.array(responses).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        # Get prediction and probabilities
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Calculate metrics
        total_score = sum(responses)
        max_score = 27  # 9 questions * 3 max points
        percentage = (total_score / max_score) * 100
        confidence = float(probabilities[prediction])
        
        # Map prediction to diagnosis
        diagnosis_map = {
            0: 'NONE',
            1: 'MILD',
            2: 'MODERATE',
            3: 'SEVERE'
        }
        
        return {
            'diagnosis': diagnosis_map[prediction],
            'confidence': round(confidence, 3),
            'score': total_score,
            'percentage': round(percentage, 2),
            'class_probabilities': {
                'none': round(float(probabilities[0]), 3),
                'mild': round(float(probabilities[1]), 3),
                'moderate': round(float(probabilities[2]), 3),
                'severe': round(float(probabilities[3]), 3)
            }
        }


# Global scorer instance
_scorer = None


def get_scorer():
    """Get or create global scorer instance"""
    global _scorer
    if _scorer is None:
        _scorer = QuizScorer()
    return _scorer


def score_quiz(responses):
    """Convenience function to score quiz responses"""
    scorer = get_scorer()
    return scorer.score_responses(responses)
