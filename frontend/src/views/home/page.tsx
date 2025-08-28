import React from 'react';
import { Route, Routes } from "react-router-dom";

import TabBar from "../../components/tab";
import ChatView from "./chat/page";
import DirectoryView from "./directory/page";

/**
 * HomeView component that renders the main interface with a tab bar and dynamic content.
 *
 * @component
 * @returns {JSX.Element} The HomeView component rendering the tab bar and routes.
 */
function HomeView() {
  return (
    <div className="flex flex-col h-full">
      {/* TabBar component for navigating between different views */}
      <div className="md:w-1/4 w-3/4 self-center mb-2 m:4">
        <TabBar />
      </div>
      
      {/* Content area that renders different views based on the active route */}
      <div className="flex-1 overflow-hidden">
        <Routes>
          {/* Route for the chat view */}
          <Route element={<ChatView />} path="chat" />
          {/* Route for the directory view */}
          <Route element={<DirectoryView />} path="directory" />
        </Routes>
      </div>
    </div>
  );
}

export default HomeView;
