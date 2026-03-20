import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()

    const workspace = await (prisma as any).workspace.findUnique({
      where: { id: params.id },
      include: {
        owner: {
          select: { id: true, email: true, displayName: true, avatarUrl: true },
        },
        members: {
          include: {
            user: {
              select: { id: true, email: true, displayName: true, avatarUrl: true },
            },
          },
          orderBy: { joinedAt: 'asc' },
        },
        documents: {
          orderBy: { updatedAt: 'desc' },
          include: {
            createdBy: {
              select: { id: true, displayName: true },
            },
          },
        },
        projects: {
          include: {
            tasks: true,
            _count: { select: { tasks: true } },
          },
          orderBy: { updatedAt: 'desc' },
        },
        _count: {
          select: { members: true, documents: true, projects: true },
        },
      },
    })

    if (!workspace) {
      return NextResponse.json({ error: 'Workspace not found' }, { status: 404 })
    }

    return NextResponse.json(workspace)
  } catch (error) {
    console.error('Error fetching workspace:', error)
    return NextResponse.json({ error: 'Failed to fetch workspace' }, { status: 500 })
  }
}
