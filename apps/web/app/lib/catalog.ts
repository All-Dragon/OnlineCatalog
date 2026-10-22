import { apiBaseUrl } from "./config";

export type Product = {
  id: number;
  title: string;
  image_url: string;
};

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(new URL("/api/v1/products", apiBaseUrl), {
    cache: "no-store",
    signal: AbortSignal.timeout(5000),
  });

  if (!response.ok) {
    throw new Error(`Failed to load products: ${response.status}`);
  }

  return response.json();
}
