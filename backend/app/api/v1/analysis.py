from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class AnalysisHistoryItem(BaseModel):
    id: str
    text: str
    risk_score: float
    risk_level: str
    timestamp: datetime

class AnalysisHistoryResponse(BaseModel):
    items: List[AnalysisHistoryItem]
    total: int

@router.get("/history", response_model=AnalysisHistoryResponse)
async def get_analysis_history(
    limit: int = 10,
    offset: int = 0
):
    """Get analysis history"""
    # In production, fetch from database
    items = []
    return AnalysisHistoryResponse(items=items, total=0)

@router.delete("/history/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis from history"""
    return {"message": "Analysis deleted successfully"}

@router.post("/batch")
async def batch_analyze(texts: List[str]):
    """Analyze multiple texts at once"""
    results = []
    for text in texts:
        # Analyze each text
        results.append({
            "text": text[:50],
            "risk_score": 0.5,
            "risk_level": "warning"
        })
    return {"results": results}
