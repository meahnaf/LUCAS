import React, { useState, useEffect } from "react";
import { ConfigProvider, theme } from "antd";
import { Route, Routes,Navigate } from "react-router-dom";

import Navbar from "./components/navbar";
import HomeView from "./views/home/page";
import ProfileView from "./views/home/profile";

/**
 * Main application component that handles theme (light/dark mode) and routing.
 *
 * @component
 * @returns {JSX.Element} The main App component rendering the navigation and routes.
 */
function App() {
  // State to track the current theme (dark mode or light mode)
  const [isDarkMode, setIsDarkMode] = useState(
    () => window.matchMedia("(prefers-color-scheme: dark)").matches
  );

  useEffect(() => {
    // Media query listener to detect system theme preference changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleThemeChange = (event: any) => {
      setIsDarkMode(event.matches);
    };

    // Listen for changes in system color scheme
    mediaQuery.addEventListener("change", handleThemeChange);

    // Clean up the event listener on component unmount
    return () => {
      mediaQuery.removeEventListener("change", handleThemeChange);
    };
  }, []);

  return (
    <ConfigProvider
      theme={{
        // Apply the dark or default theme based on the system preference
        algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
      }}
    >
      <div className="flex flex-col h-screen bg-white dark:bg-black">
        {/* Navbar component for navigation */}
        <Navbar />
        
        {/* Main content area, handling different views based on routes */}
        <div className="flex-1 overflow-hidden">
          <Routes>
          <Route path="/" element={<Navigate to="/home/chat" replace />} />

            {/* Route for HomeView */}
            <Route element={<HomeView />} path="/home/*" />
            
            {/* Route for ProfileView */}
            <Route element={<ProfileView />} path="profile" />
          </Routes>
        </div>
      </div>
    </ConfigProvider>
  );
}

export default App;
