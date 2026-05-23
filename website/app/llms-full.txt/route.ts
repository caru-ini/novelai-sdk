import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';

export const dynamic = 'force-static';
export const revalidate = false;

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
  return /^[^.]+\.mdx$/.test(base);
}

function stripFrontmatter(raw: string): { title?: string; description?: string; body: string } {
  if (!raw.startsWith('---')) return { body: raw };
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { body: raw };
  const fm = raw.slice(3, end);
  const body = raw.slice(end + 4).replace(/^\n+/, '');
  const title = fm.match(/^title:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '');
  const description = fm.match(/^description:\s*(.+)$/m)?.[1]?.trim().replace(/^['"]|['"]$/g, '');
  return { title, description, body };
}

function fileToUrl(file: string): string {
  let slug = relative(ROOT, file).replace(/\.mdx$/, '');
  slug = slug.replace(/(?:^|\/)index$/, '');
  return slug ? `${SITE}/docs/${slug}/` : `${SITE}/docs/`;
}

export async function GET() {
  const files = (await walk(ROOT)).filter(isEnglish).sort();
  const sections: string[] = [];
  sections.push('# NovelAI SDK (Unofficial) — Full Documentation');
  sections.push('');
  sections.push(
    '> Generated for LLMs and AI dev tools. See `/llms.txt` for the index.',
  );
  sections.push('');

  for (const file of files) {
    const raw = await readFile(file, 'utf8');
    const { title, description, body } = stripFrontmatter(raw);
    sections.push('---');
    sections.push(`url: ${fileToUrl(file)}`);
    if (title) sections.push(`title: ${title}`);
    if (description) sections.push(`description: ${description}`);
    sections.push('---');
    sections.push('');
    sections.push(body);
    sections.push('');
  }

  return new Response(sections.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
