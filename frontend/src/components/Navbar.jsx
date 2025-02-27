import { FaSearch, FaCog, FaBell, FaUserCircle } from "react-icons/fa";
import classes from "../styles/Dashboard.module.css";

const Navbar = () => {
  return (
    <nav className={classes.navbar}>
   <div className={classes.navLeft}>
  <div className={classes.searchContainer}>
    <input type="text" placeholder="Search..." className={classes.searchInput} />
    <FaSearch className={classes.searchIcon} />
  </div>
</div>
      <div className={classes.navRight}>
        <FaCog className={classes.icon} />
        <FaBell className={classes.icon} />
       
      </div>
    </nav>
  );
};

export default Navbar;
