import type { JSX } from 'react';
import Image from 'next/image';

type Locale = 'en' | 'ja' | 'zh-Hans';

type Strings = {
  heading: string;
  intro: string;
  userModelTitle: string;
  userModelBody: string;
  apiModelTitle: string;
  apiModelBody: string;
  imageAlt: string;
};

const copy: Record<Locale, Strings> = {
  en: {
    heading: 'Data Model Architecture',
    intro: 'The library is designed with two distinct layers of data models.',
    userModelTitle: 'User Model (Recommended)',
    userModelBody:
      'User-friendly models with sensible defaults and automatic validation.',
    apiModelTitle: 'API Model',
    apiModelBody:
      "Direct 1:1 mapping to NovelAI's API endpoints, primarily used internally.",
    imageAlt: 'NovelAI SDK data model architecture diagram',
  },
  ja: {
    heading: 'データモデル・アーキテクチャ',
    intro: 'このライブラリは、2 つの異なるデータモデル層で設計されています。',
    userModelTitle: 'User Model (推奨)',
    userModelBody:
      '適切なデフォルト値と自動バリデーションを備えた、ユーザーフレンドリーなモデル。',
    apiModelTitle: 'API Model',
    apiModelBody:
      'NovelAI の API エンドポイントと 1 対 1 で対応する、主に内部で使用されるモデル。',
    imageAlt: 'NovelAI SDK データモデル・アーキテクチャ図',
  },
  'zh-Hans': {
    heading: '数据模型架构',
    intro: '该库设计有两层不同的数据模型：',
    userModelTitle: '用户模型 (推荐)',
    userModelBody: '具有合理默认值和自动验证的用户友好模型。',
    apiModelTitle: 'API 模型',
    apiModelBody: '直接 1:1 映射到 NovelAI 的 API 端点，主要用于内部。',
    imageAlt: 'NovelAI SDK 数据模型架构图',
  },
};

export function ArchitectureSection({ lang }: { lang: string }): JSX.Element {
  const t = copy[(lang as Locale) in copy ? (lang as Locale) : 'en'];

  return (
    <section className="px-6 pb-24">
      <div className="mx-auto max-w-6xl">
        <h2 className="nai-display text-3xl font-bold sm:text-4xl text-center">
          {t.heading}
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-fd-muted-foreground">
          {t.intro}
        </p>

        <div className="mt-12 grid items-center gap-10 md:grid-cols-2">
          <Image
            src="/images/model-architecture.png"
            alt={t.imageAlt}
            width={800}
            height={0}
            sizes="(min-width: 768px) 40vw, 100vw"
            className="h-auto w-full rounded-2xl border border-fd-border"
          />

          <ul className="grid gap-4">
            <li className="nai-card">
              <h3 className="nai-accent-cream mb-2 text-lg font-semibold">
                {t.userModelTitle}
              </h3>
              <p className="text-sm leading-relaxed text-fd-muted-foreground">
                {t.userModelBody}
              </p>
            </li>
            <li className="nai-card">
              <h3 className="mb-2 text-lg font-semibold text-fd-foreground">
                {t.apiModelTitle}
              </h3>
              <p className="text-sm leading-relaxed text-fd-muted-foreground">
                {t.apiModelBody}
              </p>
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}
