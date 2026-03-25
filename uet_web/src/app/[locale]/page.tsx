import { redirect } from 'next/navigation';

export default function Home({ params }: { params: { locale: string } }) {
  const locale = params?.locale || 'en';
  redirect(`/${locale}/community`);
}