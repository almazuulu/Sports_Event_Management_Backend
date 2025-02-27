import classes from "./ActionButton.module.css";
function ActionButton({ title, onClick }) {
  return (
    <button className={classes.button} onClick={onClick}>
      {title}
    </button>
  );
}

export default ActionButton;
