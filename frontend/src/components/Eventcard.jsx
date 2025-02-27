// src/components/EventCard.js

import classes from  "../components/EventCard.module.css"; // Import CSS file

const EventCard = () => {
  return (
    <div className={classes.eventContainer}>
      <h2 className={classes.eventTitle}>Events & Competitions this week</h2>

      <div className={classes.eventCard}>
        {/* Date Box */}
        <div className={classes.dateBox}>
          <span className={classes.dateNumber}>14</span>
          <span className={classes.dateDay}>THU</span>
        </div>

        {/* Event Details */}
        <div className={classes.eventDetails}>
          <p className={classes.eventTime}>Midnight - 1 a.m.</p>
          <h3 className={classes.eventName}>Basketball Competition</h3>
          <p className={classes.eventDescription}>Competition from 01 to 05</p>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
