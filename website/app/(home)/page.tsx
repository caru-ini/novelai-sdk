import { HomePage } from '@/lib/home-page';
import { i18n } from '@/lib/i18n';

export default function Page() {
  return <HomePage lang={i18n.defaultLanguage} />;
}
