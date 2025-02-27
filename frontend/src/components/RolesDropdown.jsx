import { useEffect, useState } from "react";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";

import classes from "./RolesDropdown.module.css";
import { getUserRole } from "../utils/Authentication";

function RolesDropdown({ value, onChange, allowedEdit = false }) {
  const role = getUserRole();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (role !== "admin") return;

    const fetchUserRoles = async () => {
      try {
        setLoading(true);
        const response = await fetchWithAuth("/api/users/roles");

        if (!response.ok) toast.error("Failed to fetch roles!");

        const data = await response.json();
        setRoles(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserRoles();
  }, [role]);

  return (
    <div className={classes.formGroup}>
      <label className={classes.label}>
        Role <span>*</span>
      </label>
      {role === "admin" ? (
        <select
          name="role"
          value={value}
          onChange={onChange}
          className={classes.select}
          disabled={allowedEdit}
        >
          {roles.map((role) => (
            <option key={role.id} value={role.id}>
              {role.name}
            </option>
          ))}
        </select>
      ) : (
        <input
          type="text"
          value={value}
          disabled
          className={classes.input}
        />
      )}
    </div>
  );
}

export default RolesDropdown;
