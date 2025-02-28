import styles from "./LoadingScreen.module.css";

function LoadingScreen() {
  return (
    <div className={styles.loadingContainer}>
      <div className={styles.spinner}></div>
    </div>
  );
}

export default LoadingScreen;
