export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">TrustStep AI Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-3xl font-bold text-green-600">99.8%</div>
            <div className="text-gray-600">Detection Rate</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-3xl font-bold text-blue-600">&lt;2s</div>
            <div className="text-gray-600">Analysis Time</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-3xl font-bold text-purple-600">1,234</div>
            <div className="text-gray-600">Frauds Blocked</div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">Quick Start</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Navigate to the Analysis page</li>
            <li>Paste a suspicious message or transaction details</li>
            <li>Click "Analyze" to get instant fraud detection</li>
            <li>Review the AI-powered risk assessment</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
