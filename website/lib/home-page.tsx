import Link from 'next/link';
import { codeToHtml } from 'shiki';
import { localeHref } from './i18n';
import { KeyFeatures } from './home/sections/key-features';
import { ComparisonTable } from './home/sections/comparison-table';
import { ArchitectureSection } from './home/sections/architecture';
import { WhereToStart } from './home/sections/where-to-start';
import { ProjectFooter } from './home/sections/project-footer';

type Locale = 'en' | 'ja' | 'zh-Hans';

const copy: Record<Locale, {
  title: string;
  titleAccent: string;
  subtitle: string;
  cta: string;
  ctaSecondary: string;
  example: { title: string; body: string };
}> = {
  en: {
    title: 'Build with NovelAI in',
    titleAccent: 'modern Python.',
    subtitle:
      'A type-safe, Pydantic v2-powered SDK for the NovelAI image generation API — V4 models, Precise Reference, ControlNet, SSE streaming.',
    cta: 'Get started',
    ctaSecondary: 'View on GitHub',
    example: {
      title: 'One client. One call. One image.',
      body: 'Initialize, configure, generate — all type-checked.',
    },
  },
  ja: {
    title: 'NovelAI を',
    titleAccent: 'モダン Python で。',
    subtitle:
      'Pydantic v2 ベースの型安全な NovelAI 画像生成 SDK。V4 モデル、精密参照、ControlNet、SSE ストリーミングを完全サポート。',
    cta: 'はじめる',
    ctaSecondary: 'GitHub を見る',
    example: {
      title: 'クライアント1つ、呼び出し1つ、画像1つ。',
      body: '初期化、設定、生成 — すべて型チェック付き。',
    },
  },
  'zh-Hans': {
    title: '用现代 Python',
    titleAccent: '驾驭 NovelAI。',
    subtitle:
      '基于 Pydantic v2 的类型安全 NovelAI 图像生成 SDK。完整支持 V4 模型、精确参考、ControlNet 与 SSE 流式生成。',
    cta: '快速开始',
    ctaSecondary: '查看 GitHub',
    example: {
      title: '一个客户端。一次调用。一张图。',
      body: '初始化、配置、生成 —— 全程类型检查。',
    },
  },
};

const SAMPLE = `from novelai import NovelAI
from novelai.types import GenerateImageParams

client = NovelAI()  # picks up NOVELAI_API_KEY from env

params = GenerateImageParams(
    prompt="1girl, cat ears, masterpiece, best quality",
    model="nai-diffusion-4-5-full",
    size="portrait",
    steps=28,
    scale=5.0,
)

images = client.image.generate(params)
images[0].save("output.png")`;

export async function HomePage({ lang }: { lang: string }) {
  const t = copy[(lang as Locale) in copy ? (lang as Locale) : 'en'];

  const codeHtml = await codeToHtml(SAMPLE, {
    lang: 'python',
    themes: { light: 'github-light', dark: 'vesper' },
    defaultColor: false,
  });

  return (
    <main className="relative">
      {/* Hero */}
      <section className="relative px-6 pt-28 pb-20 sm:pt-36">
        <div className="mx-auto max-w-5xl text-center">
          <h1 className="nai-display text-balance text-5xl font-bold leading-[1.05] tracking-tight sm:text-7xl">
            {t.title}
            <br />
            <span className="nai-accent-cream italic font-bold">
              {t.titleAccent}
            </span>
          </h1>
          <p className="mx-auto mt-8 max-w-2xl text-balance text-lg leading-relaxed text-fd-muted-foreground sm:text-xl">
            {t.subtitle}
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
            <Link
              href={localeHref(lang, '/docs/getting-started')}
              className="nai-cta"
            >
              {t.cta}
              <span aria-hidden>→</span>
            </Link>
            <Link
              href="https://github.com/caru-ini/novelai-sdk"
              className="nai-cta-secondary"
            >
              {t.ctaSecondary}
            </Link>
          </div>
        </div>
      </section>

      {/* Key features (4-card grid) */}
      <KeyFeatures lang={lang} />

      {/* Comparison vs other libraries */}
      <ComparisonTable lang={lang} />

      {/* Architecture diagram + two-layer explanation */}
      <ArchitectureSection lang={lang} />

      {/* Code example */}
      <section className="px-6 pb-32">
        <div className="mx-auto max-w-5xl">
          <div className="mb-8 text-center">
            <h2 className="nai-display text-3xl font-bold sm:text-4xl">
              {t.example.title}
            </h2>
            <p className="mt-3 text-fd-muted-foreground">{t.example.body}</p>
          </div>
          <div className="nai-card !p-0">
            <div className="flex items-center gap-1.5 border-b border-fd-border px-4 py-3">
              <span className="h-2.5 w-2.5 rounded-full bg-fd-muted-foreground/40" />
              <span className="h-2.5 w-2.5 rounded-full bg-fd-muted-foreground/40" />
              <span className="h-2.5 w-2.5 rounded-full bg-fd-muted-foreground/40" />
              <span className="ml-3 font-mono text-xs font-medium text-fd-muted-foreground">
                generate.py
              </span>
            </div>
            <div
              className="nai-code-block"
              dangerouslySetInnerHTML={{ __html: codeHtml }}
            />
          </div>
        </div>
      </section>

      {/* Where to start — 4 cards linking to docs */}
      <WhereToStart lang={lang} />

      {/* Project footer with links, badges, disclaimer */}
      <ProjectFooter lang={lang} />
    </main>
  );
}
