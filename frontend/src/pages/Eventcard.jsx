// src/components/EventCard.js
import React from "react";
import "../pages/Eventcard.css"; // Import CSS file

const EventCard = () => {
  return (
    <div className="event-container">
      <h2 className="event-title">Events & Competitions this week</h2>

      <div className="event-card">
        {/* Date Box */}
        <div className="date-box">
          <span className="date-number">14</span>
          <span className="date-day">THU</span>
        </div>

        {/* Event Details */}
        <div className="event-details">
          <p className="event-time">Midnight - 1 a.m.</p>
          <h3 className="event-name">Basketball Competition</h3>
          <p className="event-description">Competition from 01 to 05</p>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
