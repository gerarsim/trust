import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'sonner';
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Settings from './pages/Settings';
import Login from './pages/Login';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <Toaster />
    </>
  );
}

export default App;
