// src/components/Navbar.js
import React from "react";
import { FaSearch, FaCog, FaBell, FaUserCircle } from "react-icons/fa";
import "../styles/Dashboard.css";

const Navbar = () => {
  return (
    <nav className="navbar">
   <div className="nav-left">
  <div className="search-container">
    <input type="text" placeholder="Search..." className="search-input" />
    <FaSearch className="search-icon" />
  </div>
</div>
      <div className="nav-right">
        <FaCog className="icon" />
        <FaBell className="icon" />
        <FaUserCircle className="icon user-icon" />
      </div>
    </nav>
  );
};

export default Navbar;
