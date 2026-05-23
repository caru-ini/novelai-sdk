import { HomeLayout } from 'fumadocs-ui/layouts/home';
import type { ReactNode } from 'react';
import { baseOptions } from '@/lib/layout.shared';
import { i18n } from '@/lib/i18n';

export default function HomePageLayout({ children }: { children: ReactNode }) {
  return (
    <HomeLayout {...baseOptions(i18n.defaultLanguage)}>{children}</HomeLayout>
  );
}
