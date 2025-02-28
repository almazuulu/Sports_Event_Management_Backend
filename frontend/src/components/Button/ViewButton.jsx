import styles from "./ViewButton.module.css";

function ViewButton({ children, ...props }) {
  return (
    <button type="button" className={styles.viewButton} {...props}>
      {children || 'View'}
    </button>
  );
}

export default ViewButton;
