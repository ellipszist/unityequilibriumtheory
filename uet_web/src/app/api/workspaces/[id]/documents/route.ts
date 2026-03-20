import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'
import { randomUUID } from 'crypto'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const documents = await (prisma as any).document.findMany({
      where: { workspaceId: params.id },
      orderBy: { updatedAt: 'desc' },
      include: {
        createdBy: {
          select: { id: true, email: true, displayName: true },
        },
      },
    })
    return NextResponse.json(documents)
  } catch (error) {
    console.error('Error fetching documents:', error)
    return NextResponse.json({ error: 'Failed to fetch documents' }, { status: 500 })
  }
}

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { title, createdById } = await request.json()

    if (!title || !createdById) {
      return NextResponse.json({ error: 'title and createdById are required' }, { status: 400 })
    }

    // Verify user is a member
    const member = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId: createdById } },
    })
    if (!member) {
      return NextResponse.json({ error: 'Not a member of this workspace' }, { status: 403 })
    }

    const yjsDocId = `ws-${params.id}-doc-${randomUUID()}`

    const document = await (prisma as any).document.create({
      data: {
        workspaceId: params.id,
        title,
        yjsDocId,
        createdById,
      },
      include: {
        createdBy: {
          select: { id: true, email: true, displayName: true },
        },
      },
    })

    return NextResponse.json(document, { status: 201 })
  } catch (error) {
    console.error('Error creating document:', error)
    return NextResponse.json({ error: 'Failed to create document' }, { status: 500 })
  }
}
