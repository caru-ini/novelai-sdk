import { source } from '@/lib/source';
import { createFromSource } from 'fumadocs-core/search/server';

export const revalidate = false;
export const dynamic = 'force-static';

export const { staticGET: GET } = createFromSource(source, {
  // Orama doesn't ship Japanese/Chinese stemmers — fall back to English
  // tokenization for all locales. Search quality for CJK is reduced but
  // still functional (matches by substring).
  localeMap: {
    en: { language: 'english' },
    ja: { language: 'english' },
    'zh-Hans': { language: 'english' },
  },
});
