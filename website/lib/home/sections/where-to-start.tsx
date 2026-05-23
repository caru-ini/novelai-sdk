import Link from 'next/link';
import { localeHref } from '@/lib/i18n';

type Locale = 'en' | 'ja' | 'zh-Hans';

const copy: Record<Locale, {
  heading: string;
  subtitle: string;
  cards: { title: string; body: string; icon: string; path: string }[];
}> = {
  en: {
    heading: 'Where to start?',
    subtitle: 'Pick a path and dive in.',
    cards: [
      {
        title: 'Getting Started',
        body: 'Install, configure, generate your first image.',
        icon: '✦',
        path: '/docs/getting-started',
      },
      {
        title: 'Authentication',
        body: 'Set up your NovelAI API key safely.',
        icon: '◇',
        path: '/docs/authentication',
      },
      {
        title: 'Examples',
        body: 'Precise Reference, ControlNet, streaming, FastAPI.',
        icon: '◉',
        path: '/docs/examples',
      },
      {
        title: 'Anlas Calculation',
        body: 'Preview cost before sending requests.',
        icon: '✧',
        path: '/docs/anlas-calculation',
      },
    ],
  },
  ja: {
    heading: 'どこから始めますか？',
    subtitle: '目的に合わせて入口を選んでください。',
    cards: [
      {
        title: 'はじめに',
        body: 'インストールから最初の画像生成まで。',
        icon: '✦',
        path: '/docs/getting-started',
      },
      {
        title: '認証',
        body: 'API キーを安全に設定する。',
        icon: '◇',
        path: '/docs/authentication',
      },
      {
        title: '機能例',
        body: '精密参照、ControlNet、ストリーミング、FastAPI。',
        icon: '◉',
        path: '/docs/examples',
      },
      {
        title: 'Anlas 計算',
        body: 'リクエスト前に消費量を見積もる。',
        icon: '✧',
        path: '/docs/anlas-calculation',
      },
    ],
  },
  'zh-Hans': {
    heading: '从哪里开始？',
    subtitle: '选择一条路径开始。',
    cards: [
      {
        title: '快速开始',
        body: '安装、配置、生成第一张图像。',
        icon: '✦',
        path: '/docs/getting-started',
      },
      {
        title: '认证',
        body: '安全配置 API 密钥。',
        icon: '◇',
        path: '/docs/authentication',
      },
      {
        title: '示例',
        body: '精确参考、ControlNet、流式、FastAPI。',
        icon: '◉',
        path: '/docs/examples',
      },
      {
        title: 'Anlas 计算',
        body: '在请求前预估消耗。',
        icon: '✧',
        path: '/docs/anlas-calculation',
      },
    ],
  },
};

function pick(lang: string): Locale {
  return (['en', 'ja', 'zh-Hans'] as const).find((l) => l === lang) ?? 'en';
}

export function WhereToStart({ lang }: { lang: string }) {
  const t = copy[pick(lang)];

  return (
    <section className="px-6 pb-24">
      <div className="mx-auto max-w-6xl">
        <div className="mb-10 text-center">
          <h2 className="nai-display text-3xl font-bold sm:text-4xl">{t.heading}</h2>
          <p className="mt-3 text-fd-muted-foreground">{t.subtitle}</p>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {t.cards.map((card) => (
            <Link key={card.title} href={localeHref(lang, card.path)} className="nai-card group">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-fd-primary/10 text-2xl text-fd-primary">
                {card.icon}
              </div>
              <h3 className="mb-2 text-lg font-semibold text-fd-foreground">{card.title}</h3>
              <p className="text-sm leading-relaxed text-fd-muted-foreground">{card.body}</p>
              <span
                aria-hidden
                className="mt-4 inline-block text-fd-muted-foreground transition-transform group-hover:translate-x-1 group-hover:text-fd-primary"
              >
                →
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
