import styles from "./DeleteButton.module.css";

function DeleteButton({ ...props }) {
  return (
    <button className={styles.deleteButton} {...props}>
      Delete
    </button>
  );
}

export default DeleteButton;
