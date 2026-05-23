# NovelAI SDK Documentation

Powered by [Fumadocs](https://fumadocs.dev/) (Next.js + MDX).
Deployed to GitHub Pages: <https://caru-ini.github.io/novelai-sdk/>.

## Develop

```bash
bun install
bun run dev
```

Then open http://localhost:3000.

## Build (static export for GH Pages)

```bash
bun run build
```

Output is in `./out/`.

## Structure

```
website/
├─ app/                     Next.js App Router
│  ├─ [lang]/               i18n root (en, ja, zh-Hans)
│  │  ├─ (home)/            Landing page
│  │  └─ docs/[[...slug]]/  Docs catch-all
│  ├─ llms.txt/             llms.txt for AI tools
│  └─ llms-full.txt/        Full text dump for LLMs
├─ content/docs/            MDX content per locale
├─ lib/                     i18n, source loader, layout
├─ public/                  Static assets
└─ source.config.ts         fumadocs-mdx config
```

## AI accessibility

The site exposes `/llms.txt` (index) and `/llms-full.txt` (full content)
so that AI dev tools (Claude Code, Cursor, Copilot, etc.) can ingest
the documentation. See <https://llmstxt.org/>.
