import { useState } from "react";

import ustLogo from "../assets/images/ust-white-logo.svg";
import Option from "./Option";
import { getUserRole } from "../utils/Authentication";
import classes from "./MainNavigation.module.css";

// icons
import { FiHome, FiSettings } from "react-icons/fi";
import { TiPinOutline, TiUserAddOutline } from "react-icons/ti";
import {
  FaRegCalendarAlt,
  FaRegClipboard,
  FaPlus,
  FaUsers,
} from "react-icons/fa";
import { LuClipboardPenLine, LuTrophy } from "react-icons/lu";
import { RxUpdate } from "react-icons/rx";
import { FaKey } from "react-icons/fa6";
import { CgProfile } from "react-icons/cg";
import { RiLockPasswordLine } from "react-icons/ri";
import { IoMdArrowDropdown } from "react-icons/io";
import { CiLogout } from "react-icons/ci";

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
          <img src={ustLogo} alt="UST Logo" className={classes.logo} />
        </div>
      </div>
      {sections
        .filter(
          ({ allowedRoles }) =>
            !allowedRoles ||
            (Array.isArray(allowedRoles)
              ? allowedRoles.includes(userRole)
              : userRole === allowedRoles)
        )
        .map(({ label, options, key }) => (
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
                {options
                  .filter(
                    ({ allowedRoles }) =>
                      !allowedRoles ||
                      (Array.isArray(allowedRoles)
                        ? allowedRoles.includes(userRole)
                        : userRole === allowedRoles)
                  )
                  .map(({ Icon, title, path }) => (
                    <Option key={title} Icon={Icon} title={title} path={path} />
                  ))}
              </div>
            )}
          </section>
        ))}
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
        allowedRoles: 'admin'
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
        allowedRoles: 'admin'
      },
    ],
  },
  // {
  //   label: "TEAMS",
  //   key: "teams",
  //   options: [
  //     {
  //       Icon: LuClipboardPenLine,
  //       title: "Register & Approve Teams",
  //       path: "/",
  //     },
  //     { Icon: FaRegClipboard, title: "Manage Teams & Players", path: "/" },
  //   ],
  // },
  // {
  //   label: "MATCH SCHEDULING",
  //   key: "scheduling",
  //   options: [
  //     { Icon: FaRegCalendarAlt, title: "View Scheduled Matches", path: "/" },
  //     { Icon: FaPlus, title: "Schedule New Match", path: "/" },
  //   ],
  // },
  // {
  //   label: "RESULTS & STANDINGS",
  //   key: "results",
  //   options: [
  //     { Icon: LuTrophy, title: "View Team Standings", path: "/" },
  //     { Icon: RxUpdate, title: "Update Match Results", path: "/" },
  //   ],
  // },
  {
    label: "ADMIN PANEL",
    key: "admin-panel",
    allowedRoles: "admin",
    options: [
      {
        Icon: FaUsers,
        title: "All Users",
        path: "/admin-panel/users",
        allowedRoles: "admin",
      },
      {
        Icon: TiUserAddOutline,
        title: "Create New User",
        path: "/admin-panel/users/create-new",
        allowedRoles: "admin",
      },
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
        Icon: CiLogout,
        title: "Logout",
        path: "/settings/logout",
      },
    ],
  },
];
