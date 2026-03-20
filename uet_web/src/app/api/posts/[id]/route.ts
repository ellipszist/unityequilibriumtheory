import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()

    const post = await prisma.post.findUnique({
      where: { id: params.id },
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
        tags: true,
        _count: {
          select: { comments: true } as any,
        },
      },
    })

    if (!post) {
      return NextResponse.json({ error: 'Post not found' }, { status: 404 })
    }

    return NextResponse.json(post)
  } catch (error) {
    console.error('Error fetching post:', error)
    return NextResponse.json({ error: 'Failed to fetch post' }, { status: 500 })
  }
}

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { title, content, authorId } = await request.json()

    const post = await prisma.post.findUnique({ where: { id: params.id } })
    if (!post) {
      return NextResponse.json({ error: 'Post not found' }, { status: 404 })
    }
    if (post.authorId !== authorId) {
      return NextResponse.json({ error: 'Not authorized' }, { status: 403 })
    }

    const updated = await prisma.post.update({
      where: { id: params.id },
      data: {
        ...(title && { title }),
        ...(content && { content }),
      },
    })

    return NextResponse.json(updated)
  } catch (error) {
    console.error('Error updating post:', error)
    return NextResponse.json({ error: 'Failed to update post' }, { status: 500 })
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const authorId = searchParams.get('authorId')

    const post = await prisma.post.findUnique({ where: { id: params.id } })
    if (!post) {
      return NextResponse.json({ error: 'Post not found' }, { status: 404 })
    }
    if (post.authorId !== authorId) {
      return NextResponse.json({ error: 'Not authorized' }, { status: 403 })
    }

    await prisma.post.delete({ where: { id: params.id } })
    return NextResponse.json({ deleted: true })
  } catch (error) {
    console.error('Error deleting post:', error)
    return NextResponse.json({ error: 'Failed to delete post' }, { status: 500 })
  }
}
