import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function POST(request: Request) {
  try {
    const body = await request.text()
    const sig = request.headers.get('stripe-signature')

    if (!sig) {
      return NextResponse.json({ error: 'Missing stripe-signature' }, { status: 400 })
    }

    const stripeKey = process.env.STRIPE_SECRET_KEY
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET

    if (!stripeKey || !webhookSecret) {
      return NextResponse.json({ error: 'Stripe not configured' }, { status: 503 })
    }

    const stripe = new (await import('stripe')).default(stripeKey)
    const event = stripe.webhooks.constructEvent(body, sig, webhookSecret)

    const prisma = getPrisma()

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as any
        const userId = session.metadata?.userId
        const credits = parseInt(session.metadata?.credits || '0')
        const plan = session.metadata?.plan

        if (userId && credits > 0) {
          // Add credits
          await (prisma as any).creditBalance.upsert({
            where: { userId },
            update: {
              balance: { increment: credits },
              lifetime: { increment: credits },
            },
            create: {
              userId,
              balance: credits,
              lifetime: credits,
            },
          })

          // Log transaction
          const balance = await (prisma as any).creditBalance.findUnique({ where: { userId } })
          if (balance) {
            await (prisma as any).creditTransaction.create({
              data: {
                creditBalanceId: balance.id,
                amount: credits,
                type: plan?.startsWith('pro_') ? 'SUBSCRIPTION' : 'PURCHASE',
                description: `${plan} — ${credits.toLocaleString()} credits`,
                referenceId: session.id,
              },
            })
          }
        }

        // Create/update subscription if it's a plan
        if (plan?.startsWith('pro_') && userId) {
          const now = new Date()
          const periodEnd = new Date(now)
          periodEnd.setMonth(periodEnd.getMonth() + (plan === 'pro_annual' ? 12 : 1))

          await (prisma as any).subscription.upsert({
            where: { userId },
            update: {
              plan: 'PRO',
              status: 'ACTIVE',
              stripeCustomerId: session.customer,
              stripeSubId: session.subscription,
              currentPeriodStart: now,
              currentPeriodEnd: periodEnd,
            },
            create: {
              userId,
              plan: 'PRO',
              status: 'ACTIVE',
              stripeCustomerId: session.customer,
              stripeSubId: session.subscription,
              currentPeriodStart: now,
              currentPeriodEnd: periodEnd,
            },
          })
        }
        break
      }

      case 'customer.subscription.deleted': {
        const sub = event.data.object as any
        await (prisma as any).subscription.updateMany({
          where: { stripeSubId: sub.id },
          data: { status: 'CANCELED', plan: 'FREE' },
        })
        break
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as any
        if (invoice.subscription) {
          await (prisma as any).subscription.updateMany({
            where: { stripeSubId: invoice.subscription },
            data: { status: 'PAST_DUE' },
          })
        }
        break
      }
    }

    return NextResponse.json({ received: true })
  } catch (error: any) {
    console.error('Webhook error:', error)
    return NextResponse.json({ error: error.message }, { status: 400 })
  }
}
