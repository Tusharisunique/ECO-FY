import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Button } from './components/ui/Button';
import { Card } from './components/ui/Card';

const Dashboard = () => {
  return (
    <div className="flex h-screen bg-canvas">
      {/* Sidebar Placeholder */}
      <aside className="w-64 bg-sidebar border-r border-border-color p-6 flex flex-col">
        <h1 className="text-xl font-bold mb-8">Eco-fy</h1>
        <nav className="flex flex-col gap-2">
          <Button variant="ghost" className="justify-start">Dashboard</Button>
          <Button variant="ghost" className="justify-start text-outline-variant">Environmental</Button>
          <Button variant="ghost" className="justify-start text-outline-variant">Social</Button>
          <Button variant="ghost" className="justify-start text-outline-variant">Gamification</Button>
        </nav>
      </aside>

      {/* Main Content Placeholder */}
      <main className="flex-1 p-10 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <h2 className="text-3xl font-bold font-sans tracking-tight">Dashboard</h2>
          <Button>Export Report</Button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <h3 className="text-sm font-semibold text-outline mb-2 uppercase tracking-wider">Total ESG Score</h3>
            <p className="text-4xl font-bold">852</p>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-outline mb-2 uppercase tracking-wider">Carbon Offset</h3>
            <p className="text-4xl font-bold">12.4t</p>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-outline mb-2 uppercase tracking-wider">Active Goals</h3>
            <p className="text-4xl font-bold">8</p>
          </Card>
        </div>
      </main>
    </div>
  );
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;
