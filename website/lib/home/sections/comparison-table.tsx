type Locale = 'en' | 'ja' | 'zh-Hans';

interface Row {
  feature: Record<Locale, string>;
  sdk: string;
  api: string;
  python: string;
  highlight?: boolean;
}

const rows: Row[] = [
  {
    feature: {
      en: 'Type Safety (Pydantic v2)',
      ja: '型安全 (Pydantic v2)',
      'zh-Hans': '类型安全 (Pydantic v2)',
    },
    sdk: '✅', api: '❌', python: '✅',
  },
  {
    feature: {
      en: 'Async Support',
      ja: '非同期サポート',
      'zh-Hans': '异步支持',
    },
    sdk: '✅', api: '✅', python: '✅',
  },
  {
    feature: {
      en: 'Image Generation',
      ja: '画像生成',
      'zh-Hans': '图像生成',
    },
    sdk: '✅', api: '✅', python: '✅',
  },
  {
    feature: {
      en: 'Text Generation',
      ja: 'テキスト生成',
      'zh-Hans': '文本生成',
    },
    sdk: '🚧', api: '✅', python: '✅',
  },
  {
    feature: {
      en: 'Precise Reference',
      ja: '精密参照 (キャラ参照)',
      'zh-Hans': '精确参考 (角色参考)',
    },
    sdk: '✅', api: '❌', python: '❌',
    highlight: true,
  },
  {
    feature: {
      en: 'Multi-Character Positioning',
      ja: 'マルチキャラクター配置',
      'zh-Hans': '多角色定位',
    },
    sdk: '✅', api: '❌', python: '✅',
    highlight: true,
  },
  {
    feature: {
      en: 'ControlNet / Vibe Transfer',
      ja: 'ControlNet / Vibe Transfer',
      'zh-Hans': 'ControlNet / Vibe Transfer',
    },
    sdk: '✅', api: '❌', python: '✅',
  },
  {
    feature: {
      en: 'SSE Streaming',
      ja: 'SSE ストリーミング',
      'zh-Hans': 'SSE 流式传输',
    },
    sdk: '✅', api: '❌', python: '✅',
  },
  {
    feature: {
      en: 'Python 3.10+',
      ja: 'Python 3.10+',
      'zh-Hans': 'Python 3.10+',
    },
    sdk: '✅', api: '❌', python: '❌',
  },
  {
    feature: {
      en: 'Active Maintenance',
      ja: 'アクティブメンテナンス',
      'zh-Hans': '积极维护',
    },
    sdk: '✅', api: '✅', python: '⚠️',
  },
];

const copy: Record<Locale, { heading: string; subtitle: string; columnFeature: string; legend: string }> = {
  en: {
    heading: 'Comparison with Alternatives',
    subtitle: 'How novelai-sdk stacks up against the other unofficial Python clients.',
    columnFeature: 'Feature',
    legend: '✅ Supported · ❌ Not supported · 🚧 Planned · ⚠️ Limited maintenance',
  },
  ja: {
    heading: '他ライブラリとの比較',
    subtitle: '他の非公式 Python クライアントと novelai-sdk を比較。',
    columnFeature: '機能',
    legend: '✅ 対応 · ❌ 未対応 · 🚧 予定 · ⚠️ 限定的なメンテナンス',
  },
  'zh-Hans': {
    heading: '与替代方案的比较',
    subtitle: 'novelai-sdk 与其他非官方 Python 客户端的对比。',
    columnFeature: '特性',
    legend: '✅ 支持 · ❌ 不支持 · 🚧 计划中 · ⚠️ 维护有限',
  },
};

function pick(lang: string): Locale {
  return (['en', 'ja', 'zh-Hans'] as const).find((l) => l === lang) ?? 'en';
}

export function ComparisonTable({ lang }: { lang: string }) {
  const locale = pick(lang);
  const t = copy[locale];

  return (
    <section className="px-6 pb-24">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 text-center">
          <h2 className="nai-display text-3xl font-bold sm:text-4xl">{t.heading}</h2>
          <p className="mt-3 text-fd-muted-foreground">{t.subtitle}</p>
        </div>

        <div className="nai-card !p-0 overflow-x-auto">
          <table className="w-full min-w-[640px] border-collapse text-sm">
            <thead>
              <tr className="bg-fd-muted/50 text-fd-foreground">
                <th className="sticky left-0 z-10 bg-fd-card border-b border-fd-border px-4 py-3 text-left font-semibold">
                  {t.columnFeature}
                </th>
                <th className="border-b border-fd-border px-4 py-3 text-center font-semibold text-fd-primary">
                  novelai-sdk
                </th>
                <th className="border-b border-fd-border px-4 py-3 text-center font-semibold text-fd-muted-foreground">
                  <a
                    href="https://github.com/Aedial/novelai-api"
                    target="_blank"
                    rel="noopener"
                    className="hover:text-fd-primary transition-colors"
                  >
                    novelai-api
                  </a>
                </th>
                <th className="border-b border-fd-border px-4 py-3 text-center font-semibold text-fd-muted-foreground">
                  <a
                    href="https://github.com/LlmKira/novelai-python"
                    target="_blank"
                    rel="noopener"
                    className="hover:text-fd-primary transition-colors"
                  >
                    novelai-python
                  </a>
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={idx} className="border-b border-fd-border/60 last:border-0">
                  <td
                    className={`sticky left-0 bg-fd-card px-4 py-3 ${
                      row.highlight ? 'font-semibold text-fd-foreground' : 'text-fd-foreground/90'
                    }`}
                  >
                    {row.feature[locale]}
                  </td>
                  <td className="px-4 py-3 text-center text-lg">{row.sdk}</td>
                  <td className="px-4 py-3 text-center text-lg text-fd-muted-foreground">{row.api}</td>
                  <td className="px-4 py-3 text-center text-lg text-fd-muted-foreground">{row.python}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="mt-4 text-center text-xs text-fd-muted-foreground">{t.legend}</p>
      </div>
    </section>
  );
}
