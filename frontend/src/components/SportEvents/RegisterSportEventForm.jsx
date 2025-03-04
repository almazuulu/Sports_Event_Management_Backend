import React, { useState } from "react";

import classes from "./RegisterSportEventForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";

function RegisterSportEventForm({
  sportEvents = null,
  onSubmit,
  loading,
  onClose,
}) {
  const [formData, setFormData] = useState({
    team: "",
    sport_event: "",
    notes: "",
  });

  const handleChange = (e) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.value,
    }));
  };

  const handleClose = () => {
    setFormData({
      team: "",
      sport_event: "",
      notes: "",
    });
    onClose();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      team: "",
      sport_event: "",
      notes: "",
    });

    onClose();
  };

  return (
    <section className={classes.formContainer}>
      <CgCloseO className={classes.closeIcon} onClick={handleClose} />
      <h1 className={classes.formHeader}>Join Sport Events</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label className={classes.label}>
            Sport Event <span>*</span>
          </label>
          <select
            name="sport_event"
            value={formData.sport_event}
            onChange={handleChange}
            className={classes.select}
            required
          >
            <option value={""} disabled>
              Please select a sport event
            </option>
            {sportEvents.map((sp) => (
              <option key={sp.id} value={sp.id}>
                {sp.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className={classes.label}>Notes</label>
          <input
            className={classes.input}
            type="text"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            autoComplete="off"
          />
        </div>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </section>
  );
}

export default RegisterSportEventForm;
