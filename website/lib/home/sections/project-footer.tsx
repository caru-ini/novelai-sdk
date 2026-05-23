import Link from 'next/link';
import { localeHref } from '@/lib/i18n';

type Locale = 'en' | 'ja' | 'zh-Hans';

type Copy = {
  projectHeading: string;
  resourcesHeading: string;
  aboutHeading: string;
  tagline: string;
  linkGithub: string;
  linkPypi: string;
  linkDocs: string;
  linkIssues: string;
  linkNovelai: string;
  disclaimer: string;
  copyrightSuffix: string;
};

const copy: Record<Locale, Copy> = {
  en: {
    projectHeading: 'Project',
    resourcesHeading: 'Resources',
    aboutHeading: 'About',
    tagline: 'A modern, type-safe Python SDK for NovelAI image generation.',
    linkGithub: 'GitHub',
    linkPypi: 'PyPI',
    linkDocs: 'Documentation',
    linkIssues: 'Report an issue',
    linkNovelai: 'NovelAI Official Site',
    disclaimer:
      'This is an unofficial client library. Not affiliated with NovelAI. Requires an active NovelAI subscription.',
    copyrightSuffix: 'All rights reserved.',
  },
  ja: {
    projectHeading: 'プロジェクト',
    resourcesHeading: 'リソース',
    aboutHeading: 'About',
    tagline: 'NovelAI 画像生成のための型安全な Python SDK。',
    linkGithub: 'GitHub',
    linkPypi: 'PyPI',
    linkDocs: 'ドキュメント',
    linkIssues: 'Issue を報告',
    linkNovelai: 'NovelAI 公式サイト',
    disclaimer:
      'これは非公式のクライアントライブラリです。NovelAI とは提携していません。利用には有効な NovelAI サブスクリプションが必要です。',
    copyrightSuffix: 'All rights reserved.',
  },
  'zh-Hans': {
    projectHeading: '项目',
    resourcesHeading: '资源',
    aboutHeading: '关于',
    tagline: '用于 NovelAI 图像生成的现代、类型安全 Python SDK。',
    linkGithub: 'GitHub',
    linkPypi: 'PyPI',
    linkDocs: '文档',
    linkIssues: '提交问题',
    linkNovelai: 'NovelAI 官网',
    disclaimer:
      '这是一个非官方的客户端库，不隶属于 NovelAI。需要有效的 NovelAI 订阅。',
    copyrightSuffix: '保留所有权利。',
  },
};

const badges = [
  {
    src: 'https://img.shields.io/pypi/v/novelai-sdk.svg',
    alt: 'PyPI version',
    href: 'https://pypi.org/project/novelai-sdk/',
  },
  {
    src: 'https://img.shields.io/pypi/pyversions/novelai-sdk.svg',
    alt: 'Python version',
    href: 'https://pypi.org/project/novelai-sdk/',
  },
  {
    src: 'https://img.shields.io/badge/license-MIT-green.svg',
    alt: 'License: MIT',
    href: 'https://github.com/caru-ini/novelai-sdk/blob/main/LICENSE',
  },
  {
    src: 'https://img.shields.io/badge/code%20style-ruff-000000.svg',
    alt: 'Code style: ruff',
    href: 'https://github.com/astral-sh/ruff',
  },
];

export function ProjectFooter({ lang }: { lang: string }) {
  const t = copy[(lang as Locale) in copy ? (lang as Locale) : 'en'];
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-fd-border px-6 pt-16 pb-12">
      <div className="mx-auto max-w-6xl grid gap-12 sm:grid-cols-2 lg:grid-cols-3">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-fd-muted-foreground mb-4">
            {t.projectHeading}
          </h3>
          <p className="text-base font-semibold text-fd-foreground">
            NovelAI SDK
          </p>
          <p className="text-sm text-fd-muted-foreground mt-2 leading-relaxed">
            {t.tagline}
          </p>
          <div className="flex flex-wrap gap-2 mt-4">
            {badges.map((b) => (
              <a
                key={b.src}
                href={b.href}
                target="_blank"
                rel="noopener"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={b.src} alt={b.alt} height={20} />
              </a>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-fd-muted-foreground mb-4">
            {t.resourcesHeading}
          </h3>
          <ul className="space-y-2 text-sm">
            <li>
              <a
                href="https://github.com/caru-ini/novelai-sdk"
                target="_blank"
                rel="noopener"
                className="text-fd-foreground hover:text-fd-primary transition-colors"
              >
                {t.linkGithub}
              </a>
            </li>
            <li>
              <a
                href="https://pypi.org/project/novelai-sdk/"
                target="_blank"
                rel="noopener"
                className="text-fd-foreground hover:text-fd-primary transition-colors"
              >
                {t.linkPypi}
              </a>
            </li>
            <li>
              <Link
                href={localeHref(lang, '/docs')}
                className="text-fd-foreground hover:text-fd-primary transition-colors"
              >
                {t.linkDocs}
              </Link>
            </li>
            <li>
              <a
                href="https://github.com/caru-ini/novelai-sdk/issues"
                target="_blank"
                rel="noopener"
                className="text-fd-foreground hover:text-fd-primary transition-colors"
              >
                {t.linkIssues}
              </a>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-fd-muted-foreground mb-4">
            {t.aboutHeading}
          </h3>
          <ul className="space-y-2 text-sm">
            <li>
              <a
                href="https://novelai.net/"
                target="_blank"
                rel="noopener"
                className="text-fd-foreground hover:text-fd-primary transition-colors"
              >
                {t.linkNovelai}
              </a>
            </li>
          </ul>
          <p className="text-xs text-fd-muted-foreground mt-4 leading-relaxed">
            {t.disclaimer}
          </p>
        </div>
      </div>

      <p className="text-xs text-fd-muted-foreground mt-12 text-center">
        © {year} caru-ini. {t.copyrightSuffix}
      </p>
    </footer>
  );
}
