import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';

export const dynamic = 'force-static';
export const revalidate = false;

const SITE_TITLE = 'NovelAI SDK (Unofficial)';
const SITE_DESC =
  'A modern, type-safe Python SDK for the NovelAI image generation API.';
const SITE = 'https://caru-ini.github.io/novelai-sdk';
const ROOT = join(process.cwd(), 'content/docs');

async function walk(dir: string): Promise<string[]> {
  const out: string[] = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (e.isFile() && e.name.endsWith('.mdx')) out.push(p);
  }
  return out;
}

function isEnglish(file: string): boolean {
  const base = file.split('/').pop() ?? '';
  // Skip per-locale variants: anything matching *.xx.mdx or *.xx-YY.mdx
  return /^[^.]+\.mdx$/.test(base);
}

function fm(raw: string): { title?: string; description?: string } {
  if (!raw.startsWith('---')) return {};
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return {};
  const block = raw.slice(3, end);
  const t = block.match(/^title:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '');
  const d = block.match(/^description:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '');
  return { title: t, description: d };
}

function fileToUrl(file: string): string {
  let slug = relative(ROOT, file).replace(/\.mdx$/, '');
  slug = slug.replace(/(?:^|\/)index$/, '');
  return slug ? `${SITE}/docs/${slug}/` : `${SITE}/docs/`;
}

export async function GET() {
  const files = (await walk(ROOT)).filter(isEnglish).sort();
  const lines: string[] = [];
  lines.push(`# ${SITE_TITLE}`);
  lines.push('');
  lines.push(`> ${SITE_DESC}`);
  lines.push('');
  lines.push('## Docs');
  lines.push('');
  for (const file of files) {
    const raw = await readFile(file, 'utf8');
    const { title, description } = fm(raw);
    const url = fileToUrl(file);
    const desc = description ? `: ${description}` : '';
    lines.push(`- [${title ?? file}](${url})${desc}`);
  }
  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
