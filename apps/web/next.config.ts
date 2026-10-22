import type { NextConfig } from "next";

import { apiBaseUrl } from "./app/lib/config";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/v1/products/:productId/image",
        destination: new URL(
          "/api/v1/products/:productId/image",
          apiBaseUrl,
        ).toString(),
      },
    ];
  },
};

export default nextConfig;
