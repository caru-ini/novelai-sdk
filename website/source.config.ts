import { defineDocs, defineConfig } from 'fumadocs-mdx/config';
import { visit } from 'unist-util-visit';

export const docs = defineDocs({
  dir: 'content/docs',
});

/**
 * Rewrite `/docs/...` MDX links so they remain locale-aware after Fumadocs
 * processes them. Default locale (en) keeps the bare `/docs/...` URL.
 * Other locales get prefixed: `/ja/docs/...`, `/zh-Hans/docs/...`.
 *
 * Locale is inferred from the source file name suffix (e.g. `foo.ja.mdx`).
 */
function remarkLocalizeDocsLinks() {
  const NON_DEFAULT = ['ja', 'zh-Hans'];
  return (tree: unknown, file: { path?: string }) => {
    const name = file.path?.split('/').pop() ?? '';
    const match = name.match(/\.([^.]+)\.mdx$/);
    const lang = match && NON_DEFAULT.includes(match[1]) ? match[1] : 'en';

    const rewrite = (url: string | undefined) => {
      if (!url) return url;
      if (lang === 'en') return url; // no prefix for default
      if (url.startsWith('/docs/') || url === '/docs') {
        return `/${lang}${url}`;
      }
      return url;
    };

    visit(
      tree as never,
      (node: {
        type: string;
        url?: string;
        attributes?: { name: string; value: unknown }[];
      }) => {
        if (node.type === 'link' && typeof node.url === 'string') {
          node.url = rewrite(node.url) ?? node.url;
        }
        if (
          (node.type === 'mdxJsxFlowElement' ||
            node.type === 'mdxJsxTextElement') &&
          Array.isArray(node.attributes)
        ) {
          for (const attr of node.attributes) {
            if (attr.name === 'href' && typeof attr.value === 'string') {
              attr.value = rewrite(attr.value) ?? attr.value;
            }
          }
        }
      },
    );
  };
}

export default defineConfig({
  mdxOptions: {
    remarkPlugins: [remarkLocalizeDocsLinks],
  },
});
