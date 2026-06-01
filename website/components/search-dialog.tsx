'use client';

import { create } from '@orama/orama';
import { useDocsSearch } from 'fumadocs-core/search/client';
import { useI18n } from 'fumadocs-ui/contexts/i18n';
import {
  SearchDialog,
  SearchDialogClose,
  SearchDialogContent,
  SearchDialogFooter,
  SearchDialogHeader,
  SearchDialogIcon,
  SearchDialogInput,
  SearchDialogList,
  SearchDialogOverlay,
  type SharedProps,
} from 'fumadocs-ui/components/dialog/search';

// basePath is empty in dev and '/novelai-sdk' in prod (see next.config.ts).
// A raw fetch() does not pick up Next.js basePath, so the index URL must
// carry it explicitly or the GitHub Pages project page returns 404.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

// Orama ships no Japanese/Chinese tokenizer, so the server indexes every
// locale as English (see app/api/search/route.ts). The browser-side index
// must use the same language. The built-in static dialog instead feeds the
// locale code ('en'/'ja'/'zh-Hans') to Orama as a language, which throws
// "Language ... is not supported" and leaves the search box empty.
function initOrama() {
  return create({ schema: { _: 'string' }, language: 'english' });
}

export default function I18nSearchDialog({ open, onOpenChange }: SharedProps) {
  const { locale } = useI18n();
  const { search, setSearch, query } = useDocsSearch({
    type: 'static',
    from: `${basePath}/api/search`,
    initOrama,
    locale,
  });

  return (
    <SearchDialog
      open={open}
      onOpenChange={onOpenChange}
      search={search}
      onSearchChange={setSearch}
      isLoading={query.isLoading}
    >
      <SearchDialogOverlay />
      <SearchDialogContent>
        <SearchDialogHeader>
          <SearchDialogIcon />
          <SearchDialogInput />
          <SearchDialogClose />
        </SearchDialogHeader>
        <SearchDialogList items={query.data !== 'empty' ? query.data : null} />
      </SearchDialogContent>
      <SearchDialogFooter />
    </SearchDialog>
  );
}
