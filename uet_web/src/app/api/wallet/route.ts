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

    const wallet = await prisma.wallet.findUnique({
      where: { userId },
      include: {
        transactionsSent: {
          orderBy: { createdAt: 'desc' },
          take: 50,
        },
        transactionsReceived: {
          orderBy: { createdAt: 'desc' },
          take: 50,
        }
      }
    })

    if (!wallet) {
      return NextResponse.json({ error: 'Wallet not found' }, { status: 404 })
    }

    return NextResponse.json(wallet)
  } catch (error) {
    console.error('Error fetching wallet:', error)
    return NextResponse.json({ error: 'Failed to fetch wallet' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const prisma = getPrisma()
    const body = await request.json()
    const { userId, address } = body

    if (!userId || !address) {
      return NextResponse.json({ error: 'userId and address are required' }, { status: 400 })
    }

    const existing = await prisma.wallet.findUnique({ where: { userId } })
    if (existing) {
      return NextResponse.json({ error: 'User already has a wallet' }, { status: 409 })
    }

    const wallet = await prisma.wallet.create({
      data: {
        userId,
        address,
        balance: 0,
      }
    })

    return NextResponse.json(wallet, { status: 201 })
  } catch (error) {
    console.error('Error creating wallet:', error)
    return NextResponse.json({ error: 'Failed to create wallet' }, { status: 500 })
  }
}
