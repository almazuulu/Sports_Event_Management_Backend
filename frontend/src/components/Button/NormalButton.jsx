import styles from "./NormalButton.module.css";

function NormalButton({ type = "button", children, ...props }) {
  return (
    <button type={type} className={styles.normalButton} {...props}>
      {children || "Back"}
    </button>
  );
}

export default NormalButton;
