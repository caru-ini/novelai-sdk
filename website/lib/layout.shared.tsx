import { defineI18nUI } from 'fumadocs-ui/i18n';
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import Image from 'next/image';
import { i18n, localeHref } from './i18n';

export const { provider: i18nProvider } = defineI18nUI(i18n, {
  translations: {
    en: { displayName: 'English' },
    ja: { displayName: '日本語', search: 'ドキュメント検索' },
    'zh-Hans': { displayName: '简体中文', search: '搜索文档' },
  },
});

export const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

const titleByLocale: Record<string, string> = {
  en: 'NovelAI SDK',
  ja: 'NovelAI SDK',
  'zh-Hans': 'NovelAI SDK',
};

const docsLabelByLocale: Record<string, string> = {
  en: 'Docs',
  ja: 'ドキュメント',
  'zh-Hans': '文档',
};

export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: {
      title: (
        <span className="flex items-center gap-2">
          <Image
            src={`${basePath}/fountain_pen.svg`}
            alt="NovelAI SDK"
            width={22}
            height={22}
          />
          <span className="font-semibold tracking-tight">
            {titleByLocale[locale] ?? 'NovelAI SDK'}
            <span className="ml-1 text-[10px] uppercase tracking-widest text-fd-muted-foreground">
              unofficial
            </span>
          </span>
        </span>
      ),
    },
    links: [
      {
        text: docsLabelByLocale[locale] ?? 'Docs',
        url: localeHref(locale, '/docs'),
        active: 'nested-url',
      },
      {
        text: 'GitHub',
        url: 'https://github.com/caru-ini/novelai-sdk',
        external: true,
      },
      {
        text: 'PyPI',
        url: 'https://pypi.org/project/novelai-sdk/',
        external: true,
      },
    ],
    githubUrl: 'https://github.com/caru-ini/novelai-sdk',
    i18n: true,
  };
}
