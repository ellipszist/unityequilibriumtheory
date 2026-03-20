import { NextResponse } from 'next/server'
import { AccessToken } from 'livekit-server-sdk'

export async function POST(request: Request) {
  try {
    const { roomName, participantName, userId } = await request.json()

    if (!roomName || !participantName) {
      return NextResponse.json(
        { error: 'roomName and participantName are required' },
        { status: 400 }
      )
    }

    const apiKey = process.env.LIVEKIT_API_KEY || 'devkey'
    const apiSecret = process.env.LIVEKIT_API_SECRET || 'devsecret'

    const at = new AccessToken(apiKey, apiSecret, {
      identity: userId || participantName,
      name: participantName,
      ttl: '1h',
    })

    at.addGrant({
      room: roomName,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
    })

    const token = await at.toJwt()

    return NextResponse.json({
      token,
      serverUrl: process.env.NEXT_PUBLIC_LIVEKIT_URL || 'ws://localhost:7880',
    })
  } catch (error) {
    console.error('Error generating LiveKit token:', error)
    return NextResponse.json({ error: 'Failed to generate token' }, { status: 500 })
  }
}
