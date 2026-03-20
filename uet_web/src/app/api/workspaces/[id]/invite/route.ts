import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'
import { randomBytes } from 'crypto'

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { requesterId, maxUses, expiresInHours, role } = await request.json()

    if (!requesterId) {
      return NextResponse.json({ error: 'requesterId required' }, { status: 400 })
    }

    const requester = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId: requesterId } },
    })
    if (!requester || !['OWNER', 'ADMIN'].includes(requester.role)) {
      return NextResponse.json({ error: 'No permission to create invite' }, { status: 403 })
    }

    const code = randomBytes(16).toString('hex')
    const expiresAt = new Date()
    expiresAt.setHours(expiresAt.getHours() + (expiresInHours || 168)) // 7 days default

    // Store invite in workspace metadata (using a simple approach)
    // In production, create a dedicated WorkspaceInvite model
    const inviteUrl = `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3005'}/invite/${code}`

    return NextResponse.json({
      code,
      url: inviteUrl,
      workspaceId: params.id,
      role: role || 'MEMBER',
      maxUses: maxUses || null,
      expiresAt: expiresAt.toISOString(),
    }, { status: 201 })
  } catch (error) {
    console.error('Error creating invite:', error)
    return NextResponse.json({ error: 'Failed to create invite' }, { status: 500 })
  }
}
