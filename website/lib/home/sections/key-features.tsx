import type { JSX } from 'react';

type Locale = 'en' | 'ja' | 'zh-Hans';

type Feature = {
  title: string;
  body: string;
  icon: string;
};

type Strings = {
  heading: string;
  subtitle: string;
  features: [Feature, Feature, Feature, Feature];
};

const ICONS: [string, string, string, string] = ['✦', '◇', '◉', '✧'];

const copy: Record<Locale, Strings> = {
  en: {
    heading: 'Key Features',
    subtitle: 'Built for production Python.',
    features: [
      {
        title: 'Type Safety',
        body: 'Python 3.10+ support, robust validation with Pydantic v2.',
        icon: ICONS[0],
      },
      {
        title: 'High-Level API',
        body: 'Intuitive, batteries-included interface for everyday use.',
        icon: ICONS[1],
      },
      {
        title: 'Modern Models',
        body: 'V4 model family, Precise Reference, ControlNet / Vibe Transfer.',
        icon: ICONS[2],
      },
      {
        title: 'Utilities',
        body: 'PIL/Pillow integration, SSE streaming, multi-character positioning.',
        icon: ICONS[3],
      },
    ],
  },
  ja: {
    heading: '主な機能',
    subtitle: '本番品質の Python のために設計。',
    features: [
      {
        title: '完全な型安全性',
        body: 'Python 3.10+ 対応、Pydantic v2 による厳格なバリデーション。',
        icon: ICONS[0],
      },
      {
        title: '高レベル API',
        body: '直感的で使いやすいインターフェース、すぐに使える。',
        icon: ICONS[1],
      },
      {
        title: '最新機能',
        body: 'V4 モデルファミリ、精密参照、ControlNet / Vibe Transfer。',
        icon: ICONS[2],
      },
      {
        title: '便利なユーティリティ',
        body: 'PIL/Pillow 統合、SSE ストリーミング、マルチキャラ配置。',
        icon: ICONS[3],
      },
    ],
  },
  'zh-Hans': {
    heading: '主要特性',
    subtitle: '为生产级 Python 而构建。',
    features: [
      {
        title: '类型安全',
        body: '支持 Python 3.10+，使用 Pydantic v2 进行强大验证。',
        icon: ICONS[0],
      },
      {
        title: '高级 API',
        body: '直观、开箱即用的接口。',
        icon: ICONS[1],
      },
      {
        title: '现代功能',
        body: 'V4 模型系列、精确参考、ControlNet / Vibe Transfer。',
        icon: ICONS[2],
      },
      {
        title: '实用工具',
        body: 'PIL/Pillow 集成、SSE 流式、多角色定位。',
        icon: ICONS[3],
      },
    ],
  },
};

export function KeyFeatures({ lang }: { lang: string }): JSX.Element {
  const t = copy[(lang as Locale) in copy ? (lang as Locale) : 'en'];

  return (
    <section className="px-6 pb-24">
      <div className="mx-auto max-w-6xl">
        <div className="text-center">
          <h2 className="nai-display text-3xl font-bold sm:text-4xl">
            {t.heading}
          </h2>
          <p className="mt-3 text-fd-muted-foreground">{t.subtitle}</p>
        </div>

        <div className="mt-10 mx-auto max-w-6xl grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {t.features.map((f) => (
            <div key={f.title} className="nai-card">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-fd-primary/10 text-2xl text-fd-primary">
                {f.icon}
              </div>
              <h3 className="mb-2 text-lg font-semibold text-fd-foreground">
                {f.title}
              </h3>
              <p className="text-sm leading-relaxed text-fd-muted-foreground">
                {f.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
