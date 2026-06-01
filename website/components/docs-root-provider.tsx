'use client';

import { RootProvider } from 'fumadocs-ui/provider/next';
import { usePathname, useRouter } from 'next/navigation';
import type { ComponentProps, ReactNode } from 'react';
import { i18n } from '@/lib/i18n';
import SearchDialog from '@/components/search-dialog';

type I18nProps = ComponentProps<typeof RootProvider>['i18n'];

export default function DocsRootProvider({
  i18n: i18nProps,
  children,
}: {
  i18n: I18nProps;
  children: ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();

  // The built-in language switcher always prefixes the target locale
  // (e.g. /en/docs). With hideLocale: 'default-locale' English lives at the
  // root and there is no middleware (static export) to drop the prefix, so
  // /en/* 404s. Rebuild the path with the hidden default-locale prefix in mind.
  const onLocaleChange = (target: string) => {
    const segments = pathname.split('/').filter(Boolean);
    if (
      segments[0] !== undefined &&
      segments[0] !== i18n.defaultLanguage &&
      (i18n.languages as readonly string[]).includes(segments[0])
    ) {
      segments.shift();
    }
    const rest = segments.join('/');
    const path =
      target === i18n.defaultLanguage ? `/${rest}` : `/${target}/${rest}`;
    const normalized = path.replace(/\/+$/, '');
    router.push(normalized === '' ? '/' : `${normalized}/`);
  };

  return (
    <RootProvider
      i18n={{ ...i18nProps, onLocaleChange }}
      search={{ SearchDialog }}
    >
      {children}
    </RootProvider>
  );
}
