import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function POST(request: Request) {
  try {
    const prisma = getPrisma()
    const body = await request.json()
    const { fromUserId, toUserId, amount, memo } = body

    if (!fromUserId || !toUserId || !amount || amount <= 0) {
      return NextResponse.json({ error: 'Invalid transfer parameters' }, { status: 400 })
    }

    // Execute transfer in a transaction
    const result = await prisma.$transaction(async (tx) => {
      // 1. Check sender wallet
      const senderWallet = await tx.wallet.findUnique({ where: { userId: fromUserId } })
      if (!senderWallet) throw new Error('Sender wallet not found')
      if (senderWallet.balance < amount) throw new Error('Insufficient funds')

      // 2. Check receiver wallet
      const receiverWallet = await tx.wallet.findUnique({ where: { userId: toUserId } })
      if (!receiverWallet) throw new Error('Receiver wallet not found')

      // 3. Deduct from sender
      await tx.wallet.update({
        where: { userId: fromUserId },
        data: { balance: { decrement: amount } }
      })

      // 4. Add to receiver
      await tx.wallet.update({
        where: { userId: toUserId },
        data: { balance: { increment: amount } }
      })

      // 5. Record transaction (sender side)
      const transaction = await tx.transaction.create({
        data: {
          fromWalletId: senderWallet.id,
          toWalletId: receiverWallet.id,
          type: 'TRANSFER',
          amount: amount,
          status: 'CONFIRMED',
        }
      })

      return transaction
    })

    return NextResponse.json({ success: true, transactionId: result.id })
  } catch (error: any) {
    console.error('Transfer error:', error)
    const message = error?.message || 'Transfer failed'
    const status = message.includes('Insufficient') ? 400 : 500
    return NextResponse.json({ error: message }, { status })
  }
}
