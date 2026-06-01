import type { ReactNode } from 'react';
import { i18nProvider } from '@/lib/layout.shared';
import { NON_DEFAULT_LANGUAGES } from '@/lib/i18n';
import { SyncHtmlLang } from './sync-html-lang';
import DocsRootProvider from '@/components/docs-root-provider';

export function generateStaticParams() {
  return NON_DEFAULT_LANGUAGES.map((lang) => ({ lang }));
}

export default async function LangLayout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: ReactNode;
}) {
  const { lang } = await params;
  return (
    <DocsRootProvider i18n={i18nProvider(lang)}>
      <SyncHtmlLang lang={lang} />
      {children}
    </DocsRootProvider>
  );
}
