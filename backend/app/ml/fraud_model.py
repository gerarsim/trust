import numpy as np
from typing import List, Dict
import re
from collections import Counter

class FraudDetector:
    """
    On-device fraud detection using rule-based + ML hybrid approach
    """
    
    def __init__(self):
        self.model = None
        self.fraud_patterns = self._load_fraud_patterns()
        
    async def load_models(self):
        """Load ML models (placeholder for actual model loading)"""
        print("📊 Loading fraud detection models...")
        # In production, load actual trained models here
        # self.model = joblib.load('fraud_model.pkl')
        self.model = "rule_based"  # Placeholder
        
    async def predict(self, text: str) -> float:
        """
        Predict fraud probability (0-1)
        
        Returns:
            float: Fraud probability score
        """
        text_lower = text.lower()
        
        # Rule-based scoring
        score = 0.0
        signals = 0
        
        # Check for urgency
        if self._check_urgency(text_lower):
            score += 0.25
            signals += 1
            
        # Check for fear/threat
        if self._check_fear(text_lower):
            score += 0.30
            signals += 1
            
        # Check for authority impersonation
        if self._check_authority(text_lower):
            score += 0.20
            signals += 1
            
        # Check for suspicious links
        if self._check_links(text):
            score += 0.15
            signals += 1
            
        # Check for financial keywords
        if self._check_financial_keywords(text_lower):
            score += 0.10
            signals += 1
        
        # Normalize score
        if signals > 0:
            score = min(score, 1.0)
        
        return score
    
    def get_detected_patterns(self, text: str) -> List[str]:
        """Get list of detected fraud patterns"""
        patterns = []
        text_lower = text.lower()
        
        if self._check_urgency(text_lower):
            patterns.append("Urgency tactics detected")
        if self._check_fear(text_lower):
            patterns.append("Fear/threat language")
        if self._check_authority(text_lower):
            patterns.append("Authority impersonation")
        if self._check_links(text):
            patterns.append("Suspicious links present")
        if self._check_financial_keywords(text_lower):
            patterns.append("Financial manipulation")
            
        return patterns
    
    def _load_fraud_patterns(self) -> Dict:
        """Load fraud detection patterns"""
        return {
            'urgency': [
                'urgent', 'immediately', 'right now', 'asap', 'expires',
                'limited time', 'act now', 'hurry', 'quick', 'fast'
            ],
            'fear': [
                'suspend', 'locked', 'blocked', 'freeze', 'restricted',
                'verify', 'confirm', 'unauthorized', 'suspicious activity',
                'security alert', 'fraud alert'
            ],
            'authority': [
                'bank', 'irs', 'government', 'police', 'fbi', 'tax',
                'customs', 'support', 'service', 'official'
            ],
            'financial': [
                'account', 'payment', 'transfer', 'refund', 'claim',
                'prize', 'winner', 'inheritance', 'investment'
            ]
        }
    
    def _check_urgency(self, text: str) -> bool:
        """Check for urgency indicators"""
        return any(word in text for word in self.fraud_patterns['urgency'])
    
    def _check_fear(self, text: str) -> bool:
        """Check for fear/threat indicators"""
        return any(word in text for word in self.fraud_patterns['fear'])
    
    def _check_authority(self, text: str) -> bool:
        """Check for authority impersonation"""
        return any(word in text for word in self.fraud_patterns['authority'])
    
    def _check_financial_keywords(self, text: str) -> bool:
        """Check for financial keywords"""
        count = sum(1 for word in self.fraud_patterns['financial'] if word in text)
        return count >= 2  # Need at least 2 financial keywords
    
    def _check_links(self, text: str) -> bool:
        """Check for suspicious links"""
        # Simple URL detection
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        if not urls:
            return False
        
        # Check for suspicious TLDs or URL shorteners
        suspicious = ['.tk', '.ml', '.ga', 'bit.ly', 'tinyurl', '.xyz', 'free']
        return any(susp in url.lower() for url in urls for susp in suspicious)
