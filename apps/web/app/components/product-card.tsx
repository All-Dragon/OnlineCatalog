import type { Product } from "../lib/catalog";

import styles from "../styles/product-card.module.css";

type ProductCardProps = {
  product: Product;
};

export function ProductCard({ product }: ProductCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.image}>
        <img
          src={product.image_url}
          alt={product.title}
          width={800}
          height={800}
          loading="lazy"
          decoding="async"
        />
      </div>

      <h2 className={styles.title}>{product.title}</h2>
    </article>
  );
}