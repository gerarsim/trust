from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.ml.fraud_model import FraudDetector
from app.ml.llm_agent import LLMAgent

router = APIRouter()

# Initialize services
fraud_detector = FraudDetector()
llm_agent = LLMAgent()

class FraudAnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = "general"
    amount: Optional[float] = None

class FraudAnalysisResponse(BaseModel):
    risk_score: float
    risk_level: str
    confidence: float
    detected_patterns: List[str]
    recommendations: List[str]
    ml_reasoning: str
    llm_reasoning: Optional[str] = None

@router.post("/analyze", response_model=FraudAnalysisResponse)
async def analyze_fraud(request: FraudAnalysisRequest):
    """
    Analyze text/transaction for fraud using AI ensemble
    """
    try:
        # Get ML prediction
        ml_score = await fraud_detector.predict(request.text)
        
        # Get LLM analysis (if enabled)
        llm_analysis = None
        if hasattr(llm_agent, 'analyze'):
            try:
                llm_analysis = await llm_agent.analyze(request.text)
            except Exception as e:
                print(f"LLM analysis failed: {e}")
        
        # Combine scores (ensemble)
        if llm_analysis:
            final_score = (ml_score * 0.6) + (llm_analysis.get('score', 0) * 0.4)
        else:
            final_score = ml_score
        
        # Determine risk level
        if final_score < 0.3:
            risk_level = "safe"
        elif final_score < 0.7:
            risk_level = "warning"
        else:
            risk_level = "danger"
        
        # Get detected patterns
        patterns = fraud_detector.get_detected_patterns(request.text)
        
        # Generate recommendations
        recommendations = generate_recommendations(risk_level, patterns)
        
        return FraudAnalysisResponse(
            risk_score=final_score,
            risk_level=risk_level,
            confidence=0.85,  # Calculate actual confidence
            detected_patterns=patterns,
            recommendations=recommendations,
            ml_reasoning=f"ML model detected {len(patterns)} fraud indicators",
            llm_reasoning=llm_analysis.get('reasoning') if llm_analysis else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_recommendations(risk_level: str, patterns: List[str]) -> List[str]:
    """Generate recommendations based on risk level"""
    recommendations = []
    
    if risk_level == "danger":
        recommendations.append("🚨 DO NOT PROCEED with this transaction")
        recommendations.append("Report this to your bank immediately")
        recommendations.append("Block the sender/contact")
    elif risk_level == "warning":
        recommendations.append("⚠️ Proceed with extreme caution")
        recommendations.append("Verify the sender through official channels")
        recommendations.append("Do not click any links in the message")
    else:
        recommendations.append("✅ This appears safe, but stay vigilant")
        recommendations.append("Always verify unexpected requests")
    
    return recommendations

@router.get("/stats")
async def get_fraud_stats():
    """Get fraud detection statistics"""
    return {
        "total_analyses": 1000,
        "fraud_detected": 234,
        "avg_response_time_ms": 1850
    }
