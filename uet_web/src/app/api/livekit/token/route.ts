import { NextResponse } from 'next/server'

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

    // Manual JWT token creation for LiveKit
    // In production, use: import { AccessToken } from 'livekit-server-sdk'
    // For now, create a simple token structure
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
    const now = Math.floor(Date.now() / 1000)
    const payload = btoa(JSON.stringify({
      iss: apiKey,
      sub: userId || participantName,
      name: participantName,
      iat: now,
      exp: now + 3600, // 1 hour
      video: {
        room: roomName,
        roomJoin: true,
        canPublish: true,
        canSubscribe: true,
      },
    }))

    // Note: This is a simplified token for development.
    // In production, install livekit-server-sdk and use AccessToken class.
    const token = `${header}.${payload}.dev-signature`

    return NextResponse.json({ token, serverUrl: process.env.NEXT_PUBLIC_LIVEKIT_URL || 'ws://localhost:7880' })
  } catch (error) {
    console.error('Error generating LiveKit token:', error)
    return NextResponse.json({ error: 'Failed to generate token' }, { status: 500 })
  }
}
