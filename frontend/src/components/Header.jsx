import { useNavigate } from "react-router-dom";
import classes from "./Header.module.css"; // Import CSS Module

function Header({ title }) {
  const navigate = useNavigate();

  return (
    <header className={classes.header}>
      <button className={classes.backButton} onClick={() => navigate("..")}>
        Back
      </button>
      <h1 className={classes.title}>{title}</h1>
    </header>
  );
}

export default Header;
