# UET v5.0 — Video & Voice Communication Spec v1

## 1. Vision
Real-time video calls, voice channels, and screen sharing for research collaboration — powered by LiveKit, integrated with Rocket.Chat and UET Workspaces.

---

## 2. Why LiveKit

- **Open-source** (Apache 2.0), Go-based WebRTC SFU
- **Scalable**: Distributed architecture, handles 1000+ participants
- **React SDK**: `@livekit/components-react` for rapid UI development
- **Rocket.Chat native integration**: LiveKit is a supported video provider
- **Recording**: Egress service for meeting recordings
- **Screen sharing**: Built-in support
- **Self-hosted**: Full control over data

---

## 3. Deployment

### 3.1 Docker Services
`yaml
livekit:
  image: livekit/livekit-server:latest
  ports:
    - 7880:7880   # HTTP API
    - 7881:7881   # WebRTC TCP
    - 50000-50100:50000-50100/udp  # WebRTC UDP
  environment:
    LIVEKIT_KEYS: ""APIKey: SecretKey""
  volumes:
    - ./livekit.yaml:/etc/livekit.yaml
  command: --config /etc/livekit.yaml

livekit-egress:  # Optional: for recording
  image: livekit/egress:latest
  environment:
    EGRESS_CONFIG_FILE: /etc/egress.yaml
`

### 3.2 LiveKit Config
`yaml
# livekit.yaml
port: 7880
rtc:
  tcp_port: 7881
  port_range_start: 50000
  port_range_end: 50100
  use_external_ip: true
keys:
  APIKey: SecretKey  # Generate unique keys
logging:
  level: info
`

---

## 4. Integration Architecture

### 4.1 Room Naming Convention
| Context | Room Name Pattern | Example |
|---------|-------------------|---------|
| Workspace voice channel | `ws-{wsId}-voice-{channelName}` | `ws-abc123-voice-general` |
| 1-on-1 video call | `call-{sortedUserIds}` | `call-user1-user2` |
| Group call | `group-{conversationId}` | `group-conv123` |

### 4.2 Token Generation (Server-side)
`	ypescript
// api/livekit/token/route.ts
import { AccessToken } from 'livekit-server-sdk';

export async function POST(req: Request) {
  const { roomName, participantName, userId } = await req.json();
  
  // Verify user has access to this room/workspace
  const hasAccess = await verifyRoomAccess(userId, roomName);
  if (!hasAccess) return Response.json({ error: 'Forbidden' }, { status: 403 });
  
  const token = new AccessToken('APIKey', 'SecretKey', {
    identity: userId,
    name: participantName,
  });
  token.addGrant({
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canSubscribe: true,
  });
  
  return Response.json({ token: await token.toJwt() });
}
`

### 4.3 React Component
`	sx
import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';

export function VideoCall({ roomName, token }: Props) {
  return (
    <LiveKitRoom
      serverUrl="ws://localhost:7880"
      token={token}
      connect={true}
    >
      <VideoConference />
    </LiveKitRoom>
  );
}
`

---

## 5. Feature Breakdown

### 5.1 Voice Channels (Workspace)
- Persistent rooms in LiveKit, users join/leave freely
- Show active participants in channel sidebar
- Mute/unmute, deafen controls
- Push-to-talk option

### 5.2 Video Calls
- 1-on-1: Click user avatar → Start video call
- Group: From workspace or DM group → Start group call
- Camera on/off, mic on/off
- Speaker view / gallery view

### 5.3 Screen Sharing
- Share entire screen or specific window/tab
- Viewers can zoom/pan
- Useful for: presenting research, code review, data visualization

### 5.4 Recording (Optional, via Egress)
- Admin can enable recording per workspace
- Stored in Cloudflare R2
- Transcription via AI (future: whisper model)

---

## 6. Rocket.Chat Integration

### 6.1 Video Call from Chat
Rocket.Chat supports LiveKit as a video call provider:
1. Configure in Rocket.Chat admin: Video Conference → LiveKit
2. Set LiveKit server URL and API keys
3. Users click video icon in any channel → LiveKit room opens
4. No custom code needed for basic integration

### 6.2 Custom UET Video UI
For workspace voice channels, use custom LiveKit React components:
- Integrated into workspace layout
- Shows participant list in sidebar
- Custom controls matching UET design system

---

## 7. Pages & Routes

| Route | Description |
|-------|-------------|
| /workspaces/[id]/voice/[name] | Voice channel (LiveKit room) |
| /call/[roomId] | Standalone call page (for DM/group calls) |

---

## 8. Bandwidth & Performance

### 8.1 Recommended Settings
| Setting | Value | Reason |
|---------|-------|--------|
| Max video resolution | 720p | Balance quality vs bandwidth |
| Audio codec | Opus | Best quality for speech |
| Simulcast | Enabled | Adaptive quality per viewer |
| Max participants (video) | 25 | Beyond this, switch to audio-only for new joiners |

### 8.2 Fallback
- If WebRTC fails (firewall): TURN server relay
- If bandwidth low: auto-downgrade to audio-only
- If LiveKit unavailable: show error with retry

---

## 9. Implementation Steps

1. Add LiveKit server to docker-compose.yml
2. Create token generation API route (`/api/livekit/token`)
3. Install `@livekit/components-react` in uet_web
4. Build VideoCall component
5. Add voice channel UI to workspace layout
6. Configure Rocket.Chat LiveKit integration
7. Add 1-on-1 call button to user profiles and DMs
8. (Optional) Add Egress for recording