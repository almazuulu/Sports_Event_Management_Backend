import { FiHome } from "react-icons/fi";
import ustLogo from "../assets/images/ust-black-logo.svg";
import classes from "./MainNavigation.module.css";
import Option from "./Option";
import LogoutButton from "./LogoutButton";

function MainNavigation() {
  return (
    <nav className={classes.sidebar}>
      <div className={classes.titleSection}>
        <div className={classes.titleContent}>
          <img src={ustLogo} alt="UST" className={classes.logo} />
          <h1>sports</h1>
        </div>
      </div>
      <div>
        <Option Icon={FiHome} title="Dashboard" path={"/dashboard"} />
        <Option Icon={FiHome} title="Dummy 1" path={"/dummy-1"} />
      </div>
      <LogoutButton />
    </nav>
  );
}

export default MainNavigation;
