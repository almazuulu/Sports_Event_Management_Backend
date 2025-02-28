import styles from "./CancelButton.module.css";

function CancelButton({ ...props }) {
  return (
    <button type="button" className={styles.cancelButton} {...props}>
      Cancel
    </button>
  );
}

export default CancelButton;
