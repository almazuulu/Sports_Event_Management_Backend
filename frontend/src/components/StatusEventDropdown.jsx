import React, { useState } from "react";

import { getUserRole } from "../utils/Authentication";
import classes from "./StatusEventDropdown.module.css";

const STATUS_EVENTS = [
  { id: "draft", name: "Draft" },
  { id: "registration", name: "Registration" },
  { id: "active", name: "Active" },
  { id: "completed", name: "Completed" },
  { id: "cancelled", name: "Cancelled" },
];

function StatusEventDropdown({ value, onChange, allowedEdit = false }) {
  const role = getUserRole();
  //   const [status, setStatus] = useState()

  return (
    <div className={classes.formGroup}>
      <label className={classes.label}>
        Status <span>*</span>
      </label>
      {role === "admin" || role === "scorekeeper" ? (
        <select
          name="status"
          value={value}
          onChange={onChange}
          className={classes.select}
          disabled={allowedEdit}
        >
          {STATUS_EVENTS.map((status) => (
            <option key={status.id} value={status.id}>
              {status.name}
            </option>
          ))}
        </select>
      ) : (
        <input type="text" value={value} disabled className={classes.input} />
      )}
    </div>
  );
}

export default StatusEventDropdown;
