import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  HomeOutlined,
  UserOutlined,
  MenuOutlined,
  CloseOutlined,
} from "@ant-design/icons";

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="flex flex-row justify-between h-20 items-center px-4 sm:px-12 relative">
      {/* Logo Section */}
      <div className="dark:text-white text-lg sm:text-xl">LucasLogo</div>

      <div className="sm:hidden">
        <button onClick={toggleMenu} className="text-black dark:text-white">
          {isMenuOpen ? <CloseOutlined /> : <MenuOutlined />}
        </button>
      </div>

      <div
        className={`${
          isMenuOpen ? "flex" : "hidden"
        } sm:flex flex-col sm:flex-row space-y-4  sm:space-y-0 sm:space-x-10 absolute sm:static top-20 left-0 w-full sm:w-auto backdrop-blur-md bg-white/50 dark:bg-neutral-950 md:dark:bg-black sm:bg-transparent p-5 sm:px-0 z-10 rounded-lg`}
      >
        <NavLink
          to="/home/chat"
          className={({ isActive }) =>
            isActive
              ? "text-black dark:text-white space-x-2 flex flex-row items-center"
              : "text-neutral-500 space-x-2 flex flex-row items-center"
          }
          onClick={()=>toggleMenu()}
        >
          <HomeOutlined />
          <span>Home</span>
        </NavLink>
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            isActive
              ? "text-black dark:text-white space-x-2 flex flex-row items-center"
              : "text-neutral-500 space-x-2 flex flex-row items-center"
          }
          onClick={()=>toggleMenu()}
        >
          <UserOutlined />
          <span>Profile</span>
        </NavLink>
      </div>
    </div>
  );
}

export default Navbar;
