import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const logs = await prisma.computeLog.findMany({
      where: { userId },
      orderBy: {
        createdAt: 'desc'
      },
      take: 100,
    })

    // Compute aggregate stats
    const stats = await prisma.computeLog.aggregate({
      where: { userId },
      _sum: { rewardEarned: true },
      _count: true,
      _max: { difficulty: true },
    })

    return NextResponse.json({
      logs,
      stats: {
        totalReward: stats._sum.rewardEarned || 0,
        totalTasksSolved: stats._count,
        maxDifficulty: stats._max.difficulty || 0,
      }
    })
  } catch (error) {
    console.error('Error fetching compute logs:', error)
    return NextResponse.json({ error: 'Failed to fetch compute logs' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const prisma = getPrisma()
    const body = await request.json()
    const { userId, rustTaskId, nonce, resultHash, difficulty, rewardEarned } = body

    if (!userId || !rustTaskId || !resultHash) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    const log = await prisma.computeLog.create({
      data: {
        userId,
        rustTaskId,
        nonce: BigInt(nonce || 0),
        resultHash,
        difficulty: difficulty || 1,
        rewardEarned: rewardEarned || 0,
      }
    })

    // Also credit the user's wallet
    if (rewardEarned && rewardEarned > 0) {
      await prisma.wallet.update({
        where: { userId },
        data: {
          balance: { increment: rewardEarned }
        }
      })
    }

    return NextResponse.json(log, { status: 201 })
  } catch (error) {
    console.error('Error creating compute log:', error)
    return NextResponse.json({ error: 'Failed to create compute log' }, { status: 500 })
  }
}
