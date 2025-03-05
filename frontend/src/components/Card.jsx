import classes from "./Card.module.css";

const Card = ({ title, count }) => {
  return (
    <div className={classes.card}>
      <p className={classes.cardTitle}>{title}</p>
      <p className={classes.cardTitle}>{count}</p>
    </div>
  );
};

export default Card;
