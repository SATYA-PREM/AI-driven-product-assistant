import React, { useState } from 'react';
import WorkspacesPage from './pages/WorkspacesPage';
import RoadmapPage from './pages/RoadmapPage';

function App() {
  const [currentPage, setCurrentPage] = useState('Roadmap');

  return (
    <div className="w-full h-full min-h-screen">
      {currentPage === 'Roadmap' ? (
        <RoadmapPage onNavigate={setCurrentPage} />
      ) : (
        <WorkspacesPage onNavigate={setCurrentPage} />
      )}
    </div>
  );
}

export default App;
