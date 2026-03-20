'use client';

import { useState, useCallback } from 'react';
import { Phone, PhoneOff, Mic, MicOff, Video, VideoOff, Monitor, Users } from 'lucide-react';

interface VideoCallProps {
  roomName: string;
  participantName: string;
  userId?: string;
  className?: string;
}

export default function VideoCall({ roomName, participantName, userId, className = '' }: VideoCallProps) {
  const [token, setToken] = useState<string | null>(null);
  const [serverUrl, setServerUrl] = useState<string>('');
  const [connecting, setConnecting] = useState(false);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState('');
  const [micEnabled, setMicEnabled] = useState(true);
  const [camEnabled, setCamEnabled] = useState(true);

  const connect = useCallback(async () => {
    setConnecting(true);
    setError('');
    try {
      const res = await fetch('/api/livekit/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ roomName, participantName, userId }),
      });
      if (!res.ok) throw new Error('Failed to get token');
      const data = await res.json();
      setToken(data.token);
      setServerUrl(data.serverUrl);
      setConnected(true);
    } catch (e: any) {
      setError(e.message || 'Connection failed');
    } finally {
      setConnecting(false);
    }
  }, [roomName, participantName, userId]);

  const disconnect = useCallback(() => {
    setToken(null);
    setConnected(false);
  }, []);

  if (!connected) {
    return (
      <div className={`flex flex-col items-center justify-center bg-card border border-border rounded-xl p-8 ${className}`}>
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-4">
          <Phone size={28} className="text-primary" />
        </div>
        <h3 className="text-lg font-semibold mb-1">Join Voice/Video</h3>
        <p className="text-sm text-muted-foreground mb-1">Room: <code className="bg-muted px-1.5 rounded">{roomName}</code></p>
        <p className="text-xs text-muted-foreground mb-6">Powered by LiveKit (WebRTC)</p>
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive text-sm w-full max-w-xs text-center">
            {error}
          </div>
        )}
        <button
          onClick={connect}
          disabled={connecting}
          className="flex items-center gap-2 px-8 py-3 rounded-xl bg-green-600 text-white font-semibold hover:bg-green-700 disabled:opacity-40 transition-colors"
        >
          {connecting ? (
            <div className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full" />
          ) : (
            <Phone size={16} />
          )}
          {connecting ? 'Connecting...' : 'Join Call'}
        </button>
      </div>
    );
  }

  // Connected state — show call UI
  // In production, use LiveKitRoom + VideoConference from @livekit/components-react
  return (
    <div className={`flex flex-col bg-[#111] rounded-xl overflow-hidden ${className}`}>
      {/* Video area */}
      <div className="flex-1 flex items-center justify-center min-h-[400px] relative">
        <div className="text-center text-white/60">
          <Users size={48} className="mx-auto mb-3 opacity-40" />
          <p className="text-sm font-medium mb-1">Connected to {roomName}</p>
          <p className="text-xs opacity-60">
            LiveKit Room active at {serverUrl}
          </p>
          <p className="text-[10px] opacity-40 mt-2">
            Wire @livekit/components-react LiveKitRoom + VideoConference components here
          </p>
        </div>

        {/* Self view (placeholder) */}
        <div className="absolute bottom-4 right-4 w-32 h-24 rounded-lg bg-gray-800 border border-gray-600 flex items-center justify-center">
          <span className="text-white/40 text-xs">You ({participantName})</span>
        </div>
      </div>

      {/* Controls bar */}
      <div className="flex items-center justify-center gap-3 py-4 bg-[#1a1a1a] border-t border-white/10">
        <button
          onClick={() => setMicEnabled(!micEnabled)}
          className={`p-3 rounded-full transition-colors ${micEnabled ? 'bg-white/10 text-white hover:bg-white/20' : 'bg-red-500 text-white'}`}
        >
          {micEnabled ? <Mic size={18} /> : <MicOff size={18} />}
        </button>
        <button
          onClick={() => setCamEnabled(!camEnabled)}
          className={`p-3 rounded-full transition-colors ${camEnabled ? 'bg-white/10 text-white hover:bg-white/20' : 'bg-red-500 text-white'}`}
        >
          {camEnabled ? <Video size={18} /> : <VideoOff size={18} />}
        </button>
        <button className="p-3 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors">
          <Monitor size={18} />
        </button>
        <button
          onClick={disconnect}
          className="p-3 rounded-full bg-red-500 text-white hover:bg-red-600 transition-colors ml-4"
        >
          <PhoneOff size={18} />
        </button>
      </div>
    </div>
  );
}
