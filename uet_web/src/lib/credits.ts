import { getPrisma } from '@/lib/prisma'

export class InsufficientCreditsError extends Error {
  balance: number
  required: number
  constructor(balance: number, required: number) {
    super(`Insufficient credits: have ${balance}, need ${required}`)
    this.balance = balance
    this.required = required
  }
}

export async function checkCredits(userId: string, estimatedCost: number): Promise<number> {
  const prisma = getPrisma()
  const balance = await (prisma as any).creditBalance.findUnique({
    where: { userId },
  })

  const current = balance?.balance ?? 0
  if (current < estimatedCost) {
    throw new InsufficientCreditsError(current, estimatedCost)
  }
  return current
}

export async function deductCredits(
  userId: string,
  amount: number,
  type: string = 'AI_USAGE',
  description?: string,
  referenceId?: string,
): Promise<{ newBalance: number }> {
  const prisma = getPrisma()

  const balance = await (prisma as any).creditBalance.findUnique({
    where: { userId },
  })

  if (!balance || balance.balance < amount) {
    throw new InsufficientCreditsError(balance?.balance ?? 0, amount)
  }

  // Atomic deduction + transaction log
  const [updated] = await (prisma as any).$transaction([
    (prisma as any).creditBalance.update({
      where: { userId },
      data: { balance: { decrement: amount } },
    }),
    (prisma as any).creditTransaction.create({
      data: {
        creditBalanceId: balance.id,
        amount: -amount,
        type,
        description: description || `AI usage: ${amount} credits`,
        referenceId,
      },
    }),
  ])

  return { newBalance: updated.balance }
}

export async function addCredits(
  userId: string,
  amount: number,
  type: string = 'BONUS',
  description?: string,
  referenceId?: string,
): Promise<{ newBalance: number }> {
  const prisma = getPrisma()

  // Upsert credit balance (create if not exists)
  const balance = await (prisma as any).creditBalance.upsert({
    where: { userId },
    update: {
      balance: { increment: amount },
      lifetime: { increment: amount },
    },
    create: {
      userId,
      balance: amount,
      lifetime: amount,
    },
  })

  // Log transaction
  await (prisma as any).creditTransaction.create({
    data: {
      creditBalanceId: balance.id,
      amount,
      type,
      description,
      referenceId,
    },
  })

  return { newBalance: balance.balance }
}

// Credit cost estimates per action
export const CREDIT_COSTS = {
  CHAT_STANDARD: 3,
  CHAT_REASONING: 15,
  DOC_INGEST_PER_PAGE: 2,
  OMEGA_SEARCH: 1,
  IMAGE_GENERATION: 10,
  VOICE_TRANSCRIPTION_PER_MIN: 5,
} as const
