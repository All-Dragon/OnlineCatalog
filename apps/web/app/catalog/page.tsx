import { ProductCard } from "../components/product-card";
import { getProducts } from "../lib/catalog";

import styles from "../styles/catalog.module.css";

export const dynamic = "force-dynamic";

export default async function CatalogPage() {
  const products = await getProducts();

  return (
    <main className={`container ${styles.main}`}>
      <section className={styles.heading} aria-labelledby="catalog-title">
        <p className={styles.eyebrow}>
          МЕНЬШЕ ШУМА. БОЛЬШЕ ХОРОШИХ ВЕЩЕЙ.
        </p>

        <h1 id="catalog-title" className={styles.title}>
          Каталог<span className={styles.dot}>.</span>
        </h1>

        <p className={styles.intro}>
          Небольшая коллекция для вашего обычного дня.
        </p>
      </section>

      {products.length === 0 ? (
        <section className={styles.empty} aria-label="Пустой каталог">
          <h2>На полке пока пусто</h2>
          <p>Как только появятся товары, вы найдёте их здесь.</p>
        </section>
      ) : (
        <ul className={styles.grid} aria-label="Товары">
          {products.map((product) => (
            <li key={product.id}>
              <ProductCard product={product} />
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}