import styles from "./CreateButton.module.css";

function CreateButton({ type = "button", children, ...props }) {
  return (
    <button type={type} className={styles.createButton} {...props}>
      {children || "Create New"}
    </button>
  );
}

export default CreateButton;
