import type { NextConfig } from 'next';
import { createMDX } from 'fumadocs-mdx/next';

const isProd = process.env.NODE_ENV === 'production';
const repo = 'novelai-sdk';

const withMDX = createMDX();

const config: NextConfig = {
  output: 'export',
  trailingSlash: true,
  reactStrictMode: true,
  images: { unoptimized: true },
  basePath: isProd ? `/${repo}` : '',
  assetPrefix: isProd ? `/${repo}/` : '',
  env: {
    NEXT_PUBLIC_BASE_PATH: isProd ? `/${repo}` : '',
  },
};

export default withMDX(config);
