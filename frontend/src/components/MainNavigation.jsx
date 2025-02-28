import { useState } from "react";

import ustLogo from "../assets/images/ust-black-logo.svg";
import Option from "./Option";
import LogoutButton from "./LogoutButton";
import { getUserRole } from "../utils/Authentication";
import classes from "./MainNavigation.module.css";

// icons
import { FiHome, FiSettings } from "react-icons/fi";
import { TiPinOutline } from "react-icons/ti";
import { FaRegCalendarAlt, FaRegClipboard, FaPlus } from "react-icons/fa";
import { LuClipboardPenLine, LuTrophy } from "react-icons/lu";
import { RxUpdate } from "react-icons/rx";
import { FaKey } from "react-icons/fa6";
import { CgProfile } from "react-icons/cg";
import { RiLockPasswordLine } from "react-icons/ri";
import { IoMdArrowDropdown } from "react-icons/io";

function MainNavigation() {
  const userRole = getUserRole();
  const [openSection, setOpenSection] = useState("dashboard");

  const toggleSection = (section) => {
    setOpenSection(openSection === section ? null : section);
  };

  return (
    <nav className={classes.sidebar}>
      <div className={classes.titleSection}>
        <div className={classes.titleContent}>
          <img src={ustLogo} alt="UST" className={classes.logo} />
          <h1>sports</h1>
        </div>
      </div>
      {sections.map(({ label, options, key }) => (
        <section key={key} className={classes.navigationSection}>
          <div
            className={classes.labelContainer}
            onClick={() => toggleSection(key)}
          >
            <label className={classes.label}>{label}</label>
            <span>
              <IoMdArrowDropdown />
            </span>
          </div>
          {openSection === key && (
            <div className={classes.optionsContainer}>
              {options.map(({ Icon, title, path, condition }) =>
                !condition ||
                (Array.isArray(condition)
                  ? condition.includes(userRole)
                  : userRole === condition) ? (
                  <Option key={title} Icon={Icon} title={title} path={path} />
                ) : null
              )}
            </div>
          )}
        </section>
      ))}

      <LogoutButton />
    </nav>
  );
}

export default MainNavigation;

const sections = [
  {
    label: "DASHBOARD",
    key: "dashboard",
    options: [{ Icon: FiHome, title: "Dashboard", path: "/dashboard" }],
  },
  {
    label: "EVENTS",
    key: "events",
    options: [
      { Icon: TiPinOutline, title: "View Events", path: "/events/view-events" },
      {
        Icon: FaRegCalendarAlt,
        title: "Create New Event",
        path: "/events/create-new",
      },
    ],
  },
  {
    label: "SPORT EVENTS",
    key: "sport-events",
    options: [
      {
        Icon: TiPinOutline,
        title: "All Sport Events",
        path: "/sport-events",
      },
      {
        Icon: FaRegCalendarAlt,
        title: "Create New Sport Event",
        path: "/sport-events/create-new",
      },
    ],
  },
  {
    label: "TEAMS",
    key: "teams",
    options: [
      {
        Icon: LuClipboardPenLine,
        title: "Register & Approve Teams",
        path: "/",
      },
      { Icon: FaRegClipboard, title: "Manage Teams & Players", path: "/" },
    ],
  },
  {
    label: "MATCH SCHEDULING",
    key: "scheduling",
    options: [
      { Icon: FaRegCalendarAlt, title: "View Scheduled Matches", path: "/" },
      { Icon: FaPlus, title: "Schedule New Match", path: "/" },
    ],
  },
  {
    label: "RESULTS & STANDINGS",
    key: "results",
    options: [
      { Icon: LuTrophy, title: "View Team Standings", path: "/" },
      { Icon: RxUpdate, title: "Update Match Results", path: "/" },
    ],
  },
  {
    label: "SETTINGS",
    key: "settings",
    options: [
      { Icon: CgProfile, title: "My Profile", path: "/settings/my-profile" },
      {
        Icon: RiLockPasswordLine,
        title: "Change Password",
        path: "/settings/change-password",
      },
      {
        Icon: FaKey,
        title: "Manage Users",
        path: "/settings/manage-users",
        condition: "admin",
      },
    ],
  },
];
