import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET() {
  try {
    const prisma = getPrisma()

    const workspaces = await (prisma as any).workspace.findMany({
      where: { isPublic: true },
      orderBy: { createdAt: 'desc' },
      include: {
        owner: {
          select: { id: true, email: true, displayName: true, avatarUrl: true },
        },
        _count: {
          select: { members: true, projects: true, documents: true },
        },
      },
    })

    return NextResponse.json(workspaces)
  } catch (error) {
    console.error('Error fetching workspaces:', error)
    return NextResponse.json({ error: 'Failed to fetch workspaces' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const prisma = getPrisma()
    const body = await request.json()
    const { name, description, ownerId, isPublic } = body

    if (!name || !ownerId) {
      return NextResponse.json({ error: 'name and ownerId are required' }, { status: 400 })
    }

    const workspace = await (prisma as any).workspace.create({
      data: {
        name,
        description: description || null,
        ownerId,
        isPublic: isPublic ?? false,
        members: {
          create: {
            userId: ownerId,
            role: 'OWNER',
          },
        },
      },
      include: {
        members: true,
        _count: { select: { members: true, projects: true } },
      },
    })

    return NextResponse.json(workspace, { status: 201 })
  } catch (error) {
    console.error('Error creating workspace:', error)
    return NextResponse.json({ error: 'Failed to create workspace' }, { status: 500 })
  }
}
