import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()

    const comments = await prisma.comment.findMany({
      where: { postId: params.id },
      orderBy: { createdAt: 'asc' },
      include: {
        author: {
          select: {
            id: true,
            email: true,
            name: true,
            image: true,
            reputation: true,
          } as any,
        },
      },
    })

    return NextResponse.json(comments)
  } catch (error) {
    console.error('Error fetching comments:', error)
    return NextResponse.json({ error: 'Failed to fetch comments' }, { status: 500 })
  }
}

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { authorId, content } = await request.json()

    if (!authorId || !content) {
      return NextResponse.json({ error: 'authorId and content are required' }, { status: 400 })
    }

    const comment = await prisma.comment.create({
      data: {
        postId: params.id,
        authorId,
        content,
      },
      include: {
        author: {
          select: { id: true, email: true, name: true, image: true } as any,
        },
      },
    })

    return NextResponse.json(comment, { status: 201 })
  } catch (error) {
    console.error('Error creating comment:', error)
    return NextResponse.json({ error: 'Failed to create comment' }, { status: 500 })
  }
}
