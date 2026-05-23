import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { ReactNode } from 'react';
import { source } from '@/lib/source';
import { baseOptions } from '@/lib/layout.shared';
import { i18n } from '@/lib/i18n';

export default function DocsRootLayout({ children }: { children: ReactNode }) {
  return (
    <DocsLayout
      tree={source.getPageTree(i18n.defaultLanguage)}
      {...baseOptions(i18n.defaultLanguage)}
    >
      {children}
    </DocsLayout>
  );
}
