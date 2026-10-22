import type { Product } from "../lib/catalog";

import styles from "../styles/product-card.module.css";

type ProductCardProps = {
  product: Product;
};

export function ProductCard({ product }: ProductCardProps) {
  return (
    <article className={styles.card}>
      <a className={styles.link} href={product.image_url}>
        <div className={styles.image}>
          <img
            src={product.image_url}
            alt={product.title}
            width={800}
            height={800}
            loading="lazy"
            decoding="async"
          />

          <span className={styles.arrow} aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M6 18 18 6M6 6h12v12" />
            </svg>
          </span>
        </div>

        <h2 className={styles.title}>{product.title}</h2>
      </a>
    </article>
  );
}