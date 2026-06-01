import { RootProvider } from 'fumadocs-ui/provider/next';
import type { ReactNode } from 'react';
import { i18nProvider } from '@/lib/layout.shared';
import { NON_DEFAULT_LANGUAGES } from '@/lib/i18n';
import { SyncHtmlLang } from './sync-html-lang';
import SearchDialog from '@/components/search-dialog';

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
    <RootProvider
      i18n={i18nProvider(lang)}
      search={{ SearchDialog }}
    >
      <SyncHtmlLang lang={lang} />
      {children}
    </RootProvider>
  );
}
