import { NavLink } from "react-router-dom";

import classes from './Option.module.css'

function Option({ Icon, title, path, notifs }) {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        `${isActive ? classes.optionSelected : ""} ${classes.option}`
      }
    >
      <div className={classes.iconContainer}>
        <Icon />
      </div>
      <span className={classes.optionText}>{title}</span>
      {/* {notifs && <span className={classes.notification}>{notifs}</span>} */}
    </NavLink>
  );
}

export default Option;
