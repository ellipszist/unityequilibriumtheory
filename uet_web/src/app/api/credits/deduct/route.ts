import { NextResponse } from 'next/server'
import { checkCredits, deductCredits, CREDIT_COSTS } from '@/lib/credits'

export async function POST(request: Request) {
  try {
    const { userId, action, amount, description, referenceId } = await request.json()

    if (!userId || !action) {
      return NextResponse.json({ error: 'userId and action are required' }, { status: 400 })
    }

    // Determine cost
    const cost = amount || (CREDIT_COSTS as any)[action] || 1

    // Check balance first
    try {
      await checkCredits(userId, cost)
    } catch (e: any) {
      return NextResponse.json({
        error: 'Insufficient credits',
        balance: e.balance,
        required: e.required,
      }, { status: 402 })
    }

    // Deduct
    const result = await deductCredits(
      userId,
      cost,
      'AI_USAGE',
      description || `${action}: ${cost} credits`,
      referenceId,
    )

    return NextResponse.json({
      success: true,
      deducted: cost,
      newBalance: result.newBalance,
    })
  } catch (error) {
    console.error('Credit deduction error:', error)
    return NextResponse.json({ error: 'Failed to deduct credits' }, { status: 500 })
  }
}
