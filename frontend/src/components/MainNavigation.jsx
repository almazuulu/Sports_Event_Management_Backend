import ustLogo from "../assets/images/ust-black-logo.svg";
import classes from "./MainNavigation.module.css";
import Option from "./Option";
import LogoutButton from "./LogoutButton";

// icons
import { FiHome, FiSettings  } from "react-icons/fi";
import { TiPinOutline } from "react-icons/ti";
import { FaRegCalendarAlt, FaRegClipboard, FaPlus   } from "react-icons/fa";
import { LuClipboardPenLine, LuTrophy  } from "react-icons/lu";
import { RxUpdate } from "react-icons/rx";
import { FaKey } from "react-icons/fa6";

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
        <section className={classes.navigationSection}>
          <label className={classes.label}>DASHBOARD</label>
          <Option Icon={FiHome} title="Dashboard" path={"/dashboard"} />
        </section>
        <section>
          <label className={classes.label}>EVENTS</label>
          <Option Icon={TiPinOutline} title="View Events" path={"/"} />
          <Option Icon={FaRegCalendarAlt} title="Create New Event" path={"/"} />
          <Option Icon={FiSettings} title="Manage Event Settings" path={"/"} />
        </section>
        <section className={classes.navigationSection}>
          <label className={classes.label}>TEAMS</label>
          <Option Icon={LuClipboardPenLine} title="Register & Approve Teams" path={"/"} />
          <Option Icon={FaRegClipboard} title="Manage Teams & Players" path={"/"} />
        </section>
        <section className={classes.navigationSection}>
          <label className={classes.label}>MATCH SCHEDULING</label>
          <Option Icon={FaRegCalendarAlt} title="View Scheduled Matches" path={"/"} />
          <Option Icon={FaPlus } title="Schedule New Match" path={"/"} />
        </section>
        <section className={classes.navigationSection}>
          <label className={classes.label}>RESULTS & STANDINGS</label>
          <Option Icon={LuTrophy } title="View Team Standings" path={"/"} />

          <Option Icon={RxUpdate} title="Update Match Results" path={"/"} />
        </section>
        <section className={classes.navigationSection}>
          <label className={classes.label}>SETTINGS</label>
          <Option Icon={FaKey} title="Manage Users" path={"/manage-users"} />
        </section>
      </div>
      <LogoutButton />
    </nav>
  );
}

export default MainNavigation;
