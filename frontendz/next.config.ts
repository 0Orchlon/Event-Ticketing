import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    source: '/eventapi/:path*',
    destination: 'http://localhost:8000/eventapi/:path*', // Proxy to Django
};

export default nextConfig;
