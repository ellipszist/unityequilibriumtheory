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

    let balance = await (prisma as any).creditBalance.findUnique({
      where: { userId },
      include: {
        transactions: {
          orderBy: { createdAt: 'desc' },
          take: 50,
        },
      },
    })

    // Auto-create credit balance for new users with signup bonus
    if (!balance) {
      balance = await (prisma as any).creditBalance.create({
        data: {
          userId,
          balance: 500,
          lifetime: 500,
          transactions: {
            create: {
              amount: 500,
              type: 'BONUS',
              description: 'Welcome bonus — 500 free credits',
            },
          },
        },
        include: {
          transactions: { orderBy: { createdAt: 'desc' }, take: 50 },
        },
      })
    }

    return NextResponse.json(balance)
  } catch (error) {
    console.error('Error fetching credits:', error)
    return NextResponse.json({ error: 'Failed to fetch credits' }, { status: 500 })
  }
}
