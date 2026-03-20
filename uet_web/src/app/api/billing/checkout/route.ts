import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { plan, userId, successUrl, cancelUrl } = await request.json()

    if (!plan || !userId) {
      return NextResponse.json({ error: 'plan and userId are required' }, { status: 400 })
    }

    const stripeKey = process.env.STRIPE_SECRET_KEY
    if (!stripeKey) {
      return NextResponse.json({
        error: 'Stripe is not configured. Set STRIPE_SECRET_KEY in environment.',
        fallback: true,
      }, { status: 503 })
    }

    // Dynamic import to avoid build errors when stripe isn't installed
    const stripe = new (await import('stripe')).default(stripeKey)

    const priceMap: Record<string, { price: number; credits: number }> = {
      pro_monthly: { price: 2000, credits: 50000 },
      pro_annual: { price: 19200, credits: 50000 },
      credits_5000: { price: 500, credits: 5000 },
      credits_20000: { price: 1500, credits: 20000 },
      credits_100000: { price: 5000, credits: 100000 },
    }

    const planConfig = priceMap[plan]
    if (!planConfig) {
      return NextResponse.json({ error: 'Invalid plan' }, { status: 400 })
    }

    const isSubscription = plan.startsWith('pro_')

    const session = await stripe.checkout.sessions.create({
      mode: isSubscription ? 'subscription' : 'payment',
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: {
            name: isSubscription ? `UET Pro Plan` : `${planConfig.credits.toLocaleString()} AI Credits`,
            description: isSubscription
              ? `${planConfig.credits.toLocaleString()} credits/month + priority features`
              : `One-time purchase of ${planConfig.credits.toLocaleString()} AI credits`,
          },
          unit_amount: planConfig.price,
          ...(isSubscription ? {
            recurring: { interval: plan === 'pro_annual' ? 'year' : 'month' },
          } : {}),
        },
        quantity: 1,
      }],
      metadata: {
        userId,
        plan,
        credits: planConfig.credits.toString(),
      },
      success_url: successUrl || `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3005'}/account/billing?success=true`,
      cancel_url: cancelUrl || `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3005'}/pricing`,
    })

    return NextResponse.json({ url: session.url, sessionId: session.id })
  } catch (error: any) {
    console.error('Stripe checkout error:', error)
    return NextResponse.json({ error: error.message || 'Checkout failed' }, { status: 500 })
  }
}
