import { Metadata } from 'next';
import { useTranslations } from 'next-intl';
import WorkchatStudio from '@/components/workchat/WorkchatStudio';

export const metadata: Metadata = {
  title: 'Workchat Studio | UET Platform',
  description: 'Collaborative AI and Physics computation studio',
};

export default function WorkchatPage() {
  return (
    <div className="flex flex-col h-[calc(100vh-64px)] w-full overflow-hidden bg-background">
      <WorkchatStudio />
    </div>
  );
}
