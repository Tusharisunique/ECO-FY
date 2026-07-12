import React from 'react';
import Sidebar from './Sidebar';

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children, title }) => {
  return (
    <div className="flex h-screen bg-canvas overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col overflow-hidden">
        {title && (
          <header className="px-8 py-5 border-b border-border-color bg-white shrink-0">
            <h1 className="text-xl font-semibold text-on-surface">{title}</h1>
          </header>
        )}
        <div className="flex-1 overflow-y-auto px-8 py-6">
          {children}
        </div>
      </main>
    </div>
  );
};

export default AppLayout;
