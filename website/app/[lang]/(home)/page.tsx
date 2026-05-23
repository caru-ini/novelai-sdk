import { HomePage } from '@/lib/home-page';
import { NON_DEFAULT_LANGUAGES } from '@/lib/i18n';

export function generateStaticParams() {
  return NON_DEFAULT_LANGUAGES.map((lang) => ({ lang }));
}

export default async function Page({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <HomePage lang={lang} />;
}
