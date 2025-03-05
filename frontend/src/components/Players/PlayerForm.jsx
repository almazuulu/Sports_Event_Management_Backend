import { useEffect, useRef, useState } from "react";

import classes from "./PlayerForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";

function PlayerForm({
  initialData = null,
  onSubmit,
  loading,
  onClose,
  allowedEdit = false,
}) {
  const [formData, setFormData] = useState({
    userID: "",
    first_name: "",
    last_name: "",
    jersey_number: "",
    position: "",
    date_of_birth: "",
    photo: null,
    is_active: "active",
    joined_date: "",
    notes: "",
  });

  const fileInputRef = useRef(null);
  const [previewImage, setPreviewImage] = useState(null);

  const handleChange = (e) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await onSubmit(formData);

      if (res.success) {
        setFormData({
          userID: "",
          first_name: "",
          last_name: "",
          jersey_number: "",
          position: "",
          date_of_birth: "",
          photo: null,
          is_active: "active",
          joined_date: "",
          notes: "",
        });
      }
    } catch (error) {
      console.error(error);
    }

    // if (fileInputRef.current) {
    //   fileInputRef.current.value = "";
    // }
    // setPreviewImage(null);
  };

  const handleClose = () => {
    setFormData({
      userID: "",
      first_name: "",
      last_name: "",
      jersey_number: "",
      position: "",
      date_of_birth: "",
      photo: null,
      is_active: "active",
      joined_date: "",
      notes: "",
    });
    // if (fileInputRef.current) {
    //   fileInputRef.current.value = "";
    // }
    // setPreviewImage(null);
    onClose();
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
    <section className={classes.formContainer}>
      <CgCloseO className={classes.closeIcon} onClick={handleClose} />
      <h1 className={classes.formHeader}>
        {allowedEdit && !initialData
          ? "Create New Player"
          : allowedEdit
          ? "Update Player"
          : initialData
          ? "View Player"
          : "Create New Player"}
      </h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label className={classes.label}>
            User ID (optional for existing user only)
          </label>
          <input
            className={classes.input}
            type="text"
            name="userID"
            value={formData.userID}
            onChange={handleChange}
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        <div>
          <label className={classes.label}>
            First Name <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        <div>
          <label className={classes.label}>
            Last Name <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        <div>
          <label className={classes.label}>
            Jersey Number <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="jersey_number"
            value={formData.jersey_number}
            onChange={handleChange}
            required
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        <div>
          <label className={classes.label}>Position</label>
          <input
            className={classes.input}
            type="text"
            name="position"
            value={formData.position}
            onChange={handleChange}
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        <div>
          <label className={classes.label}>
            Date of Birth <span>*</span>
          </label>
          <input
            className={classes.input}
            type="date"
            name="date_of_birth"
            value={formData.date_of_birth}
            onChange={handleChange}
            required
            autoComplete="off"
            disabled={!allowedEdit}
          />
        </div>

        {/* <div className={classes.imageGroup}>
            <label className={classes.label}>Team Logo</label>
            {previewImage && (
              <img
                src={previewImage}
                alt="Team Logo"
                className={classes.logoPreview}
                width="100"
                height="100"
              />
            )}
            <input
              className={classes.input}
              type="file"
              name="logo"
              accept="image/*"
              onChange={handleImageChange}
              ref={fileInputRef}
            />
          </div> */}

        <div>
          <label className={classes.label}>Active</label>
          <select
            name={"is_active"}
            value={formData.is_active ? "active" : "inactive"}
            onChange={handleChange}
            className={classes.select}
            disabled={!allowedEdit}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        <div>
          <label className={classes.label}>
            Joined Date <span>*</span>
          </label>
          <input
            className={classes.input}
            type="date"
            name="joined_date"
            value={formData.joined_date}
            onChange={handleChange}
            required
            autoComplete="off"
            disabled={!allowedEdit}
          />
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
            disabled={!allowedEdit}
          />
        </div>

        {allowedEdit && (
          <button type="submit" className={classes.button} disabled={loading}>
            {loading ? "Submitting..." : "Submit"}
          </button>
        )}
      </form>
    </section>
  );
}

export default PlayerForm;
