import React from "react";
import classes from './card.module.css';



const Card = () => {
  const cardData = [
    { title: "My Points", value: "10 Points", subtitle: "More than 83% users"},
    { title: "My Points", value: "20 Points", subtitle: "More than 73% users"},
    { title: "My Points", value: "40 Points", subtitle: "More than 73% users"},
    { title: "My Points", value: "10 Points", subtitle: "More than 43% users"},
  ];
  return (
    <div className={classes.cardContainer}>
      {cardData.map((card, index) => (
        <div key={index} className={classes.card}>
          <h3 className={classes.cardTitle}>{card.title}</h3>
          <p className={classes.cardValue}>{card.value}</p>
          <p className={classes.cardSubtitle}>{card.subtitle}</p>
        </div>
      ))}
    </div>
  );
};

export default Card;
