import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const members = await (prisma as any).workspaceMember.findMany({
      where: { workspaceId: params.id },
      include: {
        user: {
          select: { id: true, email: true, displayName: true, avatarUrl: true, reputation: true },
        },
      },
      orderBy: { joinedAt: 'asc' },
    })
    return NextResponse.json(members)
  } catch (error) {
    console.error('Error fetching members:', error)
    return NextResponse.json({ error: 'Failed to fetch members' }, { status: 500 })
  }
}

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { userId, role, inviterId } = await request.json()

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    // Check inviter has permission
    if (inviterId) {
      const inviter = await (prisma as any).workspaceMember.findUnique({
        where: { workspaceId_userId: { workspaceId: params.id, userId: inviterId } },
      })
      if (!inviter || !['OWNER', 'ADMIN'].includes(inviter.role)) {
        return NextResponse.json({ error: 'No permission to invite' }, { status: 403 })
      }
    }

    const existing = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId } },
    })
    if (existing) {
      return NextResponse.json({ error: 'User already a member' }, { status: 409 })
    }

    const member = await (prisma as any).workspaceMember.create({
      data: {
        workspaceId: params.id,
        userId,
        role: role || 'MEMBER',
      },
      include: {
        user: { select: { id: true, email: true, displayName: true, avatarUrl: true } },
      },
    })

    return NextResponse.json(member, { status: 201 })
  } catch (error) {
    console.error('Error adding member:', error)
    return NextResponse.json({ error: 'Failed to add member' }, { status: 500 })
  }
}

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { userId, role, requesterId } = await request.json()

    if (!userId || !role || !requesterId) {
      return NextResponse.json({ error: 'userId, role, and requesterId required' }, { status: 400 })
    }

    const requester = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId: requesterId } },
    })
    if (!requester || !['OWNER', 'ADMIN'].includes(requester.role)) {
      return NextResponse.json({ error: 'No permission' }, { status: 403 })
    }

    if (role === 'OWNER' && requester.role !== 'OWNER') {
      return NextResponse.json({ error: 'Only owner can transfer ownership' }, { status: 403 })
    }

    const updated = await (prisma as any).workspaceMember.update({
      where: { workspaceId_userId: { workspaceId: params.id, userId } },
      data: { role },
    })

    return NextResponse.json(updated)
  } catch (error) {
    console.error('Error updating member:', error)
    return NextResponse.json({ error: 'Failed to update member' }, { status: 500 })
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    const requesterId = searchParams.get('requesterId')

    if (!userId) {
      return NextResponse.json({ error: 'userId required' }, { status: 400 })
    }

    // Self-leave or admin removal
    if (userId !== requesterId) {
      const requester = await (prisma as any).workspaceMember.findUnique({
        where: { workspaceId_userId: { workspaceId: params.id, userId: requesterId } },
      })
      if (!requester || !['OWNER', 'ADMIN'].includes(requester.role)) {
        return NextResponse.json({ error: 'No permission' }, { status: 403 })
      }
    }

    // Can't remove the owner
    const target = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId } },
    })
    if (target?.role === 'OWNER') {
      return NextResponse.json({ error: 'Cannot remove workspace owner' }, { status: 400 })
    }

    await (prisma as any).workspaceMember.delete({
      where: { workspaceId_userId: { workspaceId: params.id, userId } },
    })

    return NextResponse.json({ removed: true })
  } catch (error) {
    console.error('Error removing member:', error)
    return NextResponse.json({ error: 'Failed to remove member' }, { status: 500 })
  }
}
