import Link from "next/link";

import styles from "../styles/header.module.css";

export function SiteHeader() {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        <Link
          className={styles.brand}
          href="/catalog"
          aria-label="Полка: каталог товаров"
        >
          <span className={styles.brandSymbol} aria-hidden="true">
            <svg viewBox="0 0 32 32">
              <path d="M5 12h22M5 26h22M8 12V6h6v6M18 12V3h6v9M8 26v-7h6v7M18 26V16h6v10" />
            </svg>
          </span>

          <span>
            полка<span className={styles.brandDot}>.</span>
          </span>
        </Link>

        <nav className={styles.nav} aria-label="Основная навигация">
          <Link className={styles.navLink} href="/catalog" aria-current="page">
            Каталог
          </Link>
        </nav>

        <span className={styles.note}>
          Простые вещи. Каждый день.
        </span>
      </div>
    </header>
  );
}
