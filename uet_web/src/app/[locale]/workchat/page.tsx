import AppShell from '@/components/layout/AppShell';
import EmbeddedLobeChat from '@/components/workchat/EmbeddedLobeChat';

export default function WorkChatPage() {
  return (
    <AppShell>
      <div className="h-[calc(100vh-56px)] overflow-hidden">
        <EmbeddedLobeChat projectScope="workchat" />
      </div>
    </AppShell>
  );
}
