import React, { useEffect, useState } from "react";

import classes from "./ViewTeamForm.module.css";

function ViewTeamForm({ initialData = null, allowEdit = false }) {
  const [formData, setFormData] = useState({
    id: "",
    name: "",
    logo: null,
    description: "",
    captain: {},
    contact_email: "",
    contact_phone: "",
    player_count: 0,
    status: "",
    created_at: "",
    updated_at: "",
  });

  const handleChange = (e) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.value,
    }));
  };

  useEffect(() => {
    if (initialData) {
      setFormData((prevData) => ({
        ...prevData,
        ...initialData,
      }));
    }
  }, [initialData]);

  return (
    <div className={classes.formContainer}>
      <form>
        {/* <div>
          <label className={classes.label}>Team Logo</label>
          <img
            src={formData.logo ?? "https://placehold.co/100"}
            alt={formData.name}
            width="100"
            height="100"
          />
        </div> */}
        <div>
          <label className={classes.label}>Team ID</label>
          <input
            type="text"
            name="id"
            value={formData.id}
            disabled
            className={classes.input}
            onChange={handleChange}
          />
        </div>
        <div>
          <label className={classes.label}>Team Name</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
          />
        </div>

        <div>
          <label className={classes.label}>Description</label>
          <input
            type="text"
            name="description"
            value={formData.description}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
          />
        </div>

        <div>
          <label className={classes.label}>Player Count</label>
          <input
            type="number"
            name="player_count"
            value={formData.player_count}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
          />
        </div>
        <div>
          <label className={classes.label}>Status</label>
          <input
            type="text"
            name="status"
            value={formData.status}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
            style={{ textTransform: 'capitalize'}}
          />
        </div>

        <div>
          <label className={classes.label}>Contact Email</label>
          <input
            type="email"
            name="contact_email"
            value={formData.contact_email}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
          />
        </div>
        <div>
          <label className={classes.label}>Contact Phone</label>
          <input
            type="text"
            name="contact_phone"
            value={formData.contact_phone}
            className={classes.input}
            onChange={handleChange}
            disabled={!allowEdit}
          />
        </div>

        {/* TEAM CAPTAIN'S INFORMATION */}
        <hr />
        <label className={classes.label}>Captain Information</label>
        <div>
          <label className={classes.label}>Full Name</label>
          <input
            type="text"
            name="captain_name"
            value={`${formData.captain.first_name} ${formData.captain.last_name}`}
            className={classes.input}
            onChange={handleChange}
            disabled
          />
        </div>
        <div>
          <label className={classes.label}>Email</label>
          <input
            type="email"
            name="captain_email"
            value={formData.captain.email}
            className={classes.input}
            onChange={handleChange}
            disabled
          />
        </div>
      </form>
    </div>
  );
}

export default ViewTeamForm;
