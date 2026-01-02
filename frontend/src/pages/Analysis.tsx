import { useState } from 'react';

export default function Analysis() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/fraud/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Fraud Analysis</h1>
        
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <label className="block text-sm font-medium mb-2">
            Enter message or transaction details:
          </label>
          <textarea
            className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Paste suspicious message here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={analyzeText}
            disabled={!text || loading}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        {result && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-4">Results</h2>
            
            <div className={`p-4 rounded-lg mb-4 ${
              result.risk_level === 'danger' ? 'bg-red-100' :
              result.risk_level === 'warning' ? 'bg-yellow-100' :
              'bg-green-100'
            }`}>
              <div className="text-lg font-bold">
                Risk Level: {result.risk_level.toUpperCase()}
              </div>
              <div className="text-sm">
                Risk Score: {(result.risk_score * 100).toFixed(1)}%
              </div>
            </div>

            {result.detected_patterns && result.detected_patterns.length > 0 && (
              <div className="mb-4">
                <h3 className="font-bold mb-2">Detected Patterns:</h3>
                <ul className="list-disc list-inside space-y-1">
                  {result.detected_patterns.map((pattern: string, i: number) => (
                    <li key={i} className="text-gray-700">{pattern}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.recommendations && result.recommendations.length > 0 && (
              <div>
                <h3 className="font-bold mb-2">Recommendations:</h3>
                <ul className="list-disc list-inside space-y-1">
                  {result.recommendations.map((rec: string, i: number) => (
                    <li key={i} className="text-gray-700">{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
