import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'ja', 'zh-Hans'],
  // Default locale lives at /, non-default at /<lang>/...
  hideLocale: 'default-locale',
});

export const NON_DEFAULT_LANGUAGES = i18n.languages.filter(
  (l) => l !== i18n.defaultLanguage,
);

/** Build a locale-aware URL for a route like '/docs/getting-started'. */
export function localeHref(lang: string, path: string): string {
  if (lang === i18n.defaultLanguage) return path;
  return `/${lang}${path}`;
}
