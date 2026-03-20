import { redirect } from 'next/navigation';

export default function WorkchatPage({ params }: { params: { locale: string } }) {
  redirect(`/${params.locale}/chat`);
}
