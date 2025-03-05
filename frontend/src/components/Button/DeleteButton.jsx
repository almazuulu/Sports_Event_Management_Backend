import styles from "./DeleteButton.module.css";

function DeleteButton({ children, ...props }) {
  return (
    <button className={styles.deleteButton} {...props}>
      {children ?? 'Delete'}
    </button>
  );
}

export default DeleteButton;
