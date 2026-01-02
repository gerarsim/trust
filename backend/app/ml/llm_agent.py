from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from typing import Dict, Optional
from app.core.config import settings
import json

class LLMAgent:
    """
    LLM-powered fraud analysis using Claude and GPT
    """
    
    def __init__(self):
        self.claude_client = None
        self.openai_client = None
        
        if settings.ANTHROPIC_API_KEY:
            self.claude_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def analyze(self, text: str, use_claude: bool = True) -> Dict:
        """
        Analyze text using LLM for deep fraud detection
        
        Args:
            text: Text to analyze
            use_claude: Use Claude (True) or GPT (False)
            
        Returns:
            Dict with score, reasoning, and recommendations
        """
        if use_claude and self.claude_client:
            return await self._analyze_with_claude(text)
        elif self.openai_client:
            return await self._analyze_with_gpt(text)
        else:
            return {
                'score': 0.0,
                'reasoning': 'LLM analysis not available',
                'recommendations': []
            }
    
    async def _analyze_with_claude(self, text: str) -> Dict:
        """Analyze using Claude"""
        prompt = f"""Analyze this message for fraud indicators.

Message: "{text}"

Provide a JSON response with:
1. fraud_score: probability 0.0-1.0
2. reasoning: why you think it's fraud or legitimate
3. detected_tactics: list of manipulation tactics
4. recommendations: list of actions to take

Be concise and accurate."""

        try:
            response = await self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            content = response.content[0].text
            result = self._parse_llm_response(content)
            
            return {
                'score': result.get('fraud_score', 0.5),
                'reasoning': result.get('reasoning', ''),
                'tactics': result.get('detected_tactics', []),
                'recommendations': result.get('recommendations', [])
            }
        
        except Exception as e:
            print(f"Claude analysis error: {e}")
            return {'score': 0.0, 'reasoning': f'Error: {str(e)}', 'recommendations': []}
    
    async def _analyze_with_gpt(self, text: str) -> Dict:
        """Analyze using GPT"""
        prompt = f"""Analyze this message for fraud. Return JSON only.

Message: "{text}"

Return:
{{
  "fraud_score": 0.0-1.0,
  "reasoning": "explanation",
  "detected_tactics": ["tactic1", "tactic2"],
  "recommendations": ["action1", "action2"]
}}"""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = self._parse_llm_response(content)
            
            return {
                'score': result.get('fraud_score', 0.5),
                'reasoning': result.get('reasoning', ''),
                'tactics': result.get('detected_tactics', []),
                'recommendations': result.get('recommendations', [])
            }
        
        except Exception as e:
            print(f"GPT analysis error: {e}")
            return {'score': 0.0, 'reasoning': f'Error: {str(e)}', 'recommendations': []}
    
    def _parse_llm_response(self, content: str) -> Dict:
        """Parse LLM JSON response"""
        try:
            # Try to extract JSON from markdown code blocks
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"JSON parse error: {e}")
            return {
                'fraud_score': 0.5,
                'reasoning': content[:200],
                'detected_tactics': [],
                'recommendations': []
            }
