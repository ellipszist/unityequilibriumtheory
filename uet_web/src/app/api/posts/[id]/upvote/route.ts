import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { userId, value } = await request.json()

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const voteValue = value === -1 ? -1 : 1

    const existing = await (prisma as any).vote.findUnique({
      where: { postId_userId: { postId: params.id, userId } },
    })

    if (existing) {
      if (existing.value === voteValue) {
        // Remove vote (toggle off)
        await (prisma as any).vote.delete({
          where: { id: existing.id },
        })
        await prisma.post.update({
          where: { id: params.id },
          data: { upvotes: { decrement: existing.value } },
        })
        return NextResponse.json({ voted: false, value: 0 })
      } else {
        // Change vote direction
        await (prisma as any).vote.update({
          where: { id: existing.id },
          data: { value: voteValue },
        })
        await prisma.post.update({
          where: { id: params.id },
          data: { upvotes: { increment: voteValue - existing.value } },
        })
        return NextResponse.json({ voted: true, value: voteValue })
      }
    }

    // New vote
    await (prisma as any).vote.create({
      data: { postId: params.id, userId, value: voteValue },
    })
    await prisma.post.update({
      where: { id: params.id },
      data: { upvotes: { increment: voteValue } },
    })

    return NextResponse.json({ voted: true, value: voteValue })
  } catch (error) {
    console.error('Error voting:', error)
    return NextResponse.json({ error: 'Failed to vote' }, { status: 500 })
  }
}
