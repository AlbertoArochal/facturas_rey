import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/api/generar",
          destination: "http://localhost:3001/api/generar",
        },
      ];
    }
    return [];
  },
};

export default nextConfig;
