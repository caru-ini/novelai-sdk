import './global.css';
import { Inter, IBM_Plex_Serif } from 'next/font/google';
import { RootProvider } from 'fumadocs-ui/provider/next';
import type { ReactNode } from 'react';
import { i18nProvider } from '@/lib/layout.shared';
import { i18n } from '@/lib/i18n';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });
const display = IBM_Plex_Serif({
  subsets: ['latin'],
  weight: ['500', '600', '700'],
  style: ['normal', 'italic'],
  variable: '--font-display',
});

export const metadata = {
  title: 'NovelAI SDK (Unofficial)',
  description: 'A modern, type-safe Python SDK for NovelAI image generation.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang={i18n.defaultLanguage}
      className={`${inter.variable} ${display.variable}`}
      suppressHydrationWarning
    >
      <body className="flex min-h-screen flex-col font-sans antialiased">
        <RootProvider
          i18n={i18nProvider(i18n.defaultLanguage)}
          search={{ options: { type: 'static' } }}
        >
          {children}
        </RootProvider>
      </body>
    </html>
  );
}
