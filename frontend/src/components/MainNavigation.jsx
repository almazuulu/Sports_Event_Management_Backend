import { useState } from "react";

import ustLogo from "../assets/images/ust-white-logo.svg";
import Option from "./Option";
import { getUserRole } from "../utils/Authentication";
import classes from "./MainNavigation.module.css";

// icons
import { FiHome, FiSettings } from "react-icons/fi";
import { TiUserAddOutline } from "react-icons/ti";
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
import { RiLockPasswordLine, RiTeamLine } from "react-icons/ri";
import { IoMdArrowDropdown } from "react-icons/io";
import { CiLogout } from "react-icons/ci";
import { MdEvent, MdOutlineSportsSoccer } from "react-icons/md";

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
    options: [{ Icon: MdEvent, title: "All Events", path: "/events" }],
  },
  {
    label: "SPORT EVENTS",
    key: "sport-events",
    options: [
      {
        Icon: MdOutlineSportsSoccer,
        title: "All Sport Events",
        path: "/sport-events",
      },
    ],
  },
  {
    label: "TEAMS",
    key: "teams",
    options: [
      {
        Icon: RiTeamLine,
        title: "All Teams",
        path: "/teams",
      },
      {
        Icon: LuClipboardPenLine,
        title: "My Teams",
        path: "/teams/my-teams",
        allowedRoles: "team_captain",
      },
    ],
  },
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
        path: "/admin-panel",
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
