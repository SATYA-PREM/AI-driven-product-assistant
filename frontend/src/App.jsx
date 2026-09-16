import React, { useState } from 'react';
import WorkspacesPage from './pages/WorkspacesPage';
import RoadmapPage from './pages/RoadmapPage';
import RequirementsPage from './pages/RequirementsPage';

function App() {
  // Default to Requirements page as requested
  const [currentPage, setCurrentPage] = useState('Requirements');

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'Requirements':
      case 'Requirements (PRDs)':
        return <RequirementsPage onNavigate={setCurrentPage} />;
      case 'Roadmap':
        return <RoadmapPage onNavigate={setCurrentPage} />;
      case 'Workspaces':
      case 'PM Dashboard':
      default:
        return <WorkspacesPage onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="w-full h-full min-h-screen">
      {renderCurrentPage()}
    </div>
  );
}

export default App;
