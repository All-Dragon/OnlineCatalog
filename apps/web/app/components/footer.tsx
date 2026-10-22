import Link from "next/link";

import styles from "../styles/footer.module.css";

export function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.inner}`}>
        <Link className={styles.brand} href="/catalog">
          полка.
        </Link>

        <p className={styles.description}>
          Вещи, которым найдётся место.
        </p>

        <a className={styles.backTop} href="#top">
          Наверх
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M6 18 18 6M6 6h12v12" />
          </svg>
        </a>
      </div>
    </footer>
  );
}