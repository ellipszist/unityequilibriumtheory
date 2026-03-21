# UET v5.0 — Credit & Subscription System Spec v1

> **Related:** [[09__PLATFORM_ENERGY_UNITS]] · [[12__MATHNICRY_ECONOMIC_CONSTITUTION]] · [[28__OPEN_SOURCE_STACK_SELECTION_v1]] · [[34__INTEGRATION_ARCHITECTURE_v1]]
> ⚠️ **Overlap:** "Credits" maps to Doc 09's "AEU" concept.

## 1. Vision
A credit-based system for AI usage metering + Stripe subscriptions for platform access. Credits are the internal currency for consuming AI services. UET Coins can be exchanged for credits but are NOT the same thing.

---

## 2. Core Concepts

### 2.1 Credit vs UET Coin
| | Credits | UET Coin |
|--|---------|----------|
| Purpose | Pay for AI usage on platform | Blockchain-native currency |
| Stability | Fixed value (1 credit = ~1000 AI tokens) | Market-determined |
| Acquisition | Buy with fiat (Stripe) or exchange from UET Coin | Mining, bounties, transfers |
| Storage | Prisma CreditBalance | Wallet (Prisma + future chain) |
| Depletion | Consumed by AI API calls | Transferred or exchanged |

### 2.2 Why Separate?
- UET Coin value fluctuates; credits must be stable for predictable AI costs
- Users who don't care about crypto can just buy credits with USD
- Exchange rate adjustable by governance (future)

---

## 3. Data Model

`prisma
model CreditBalance {
  id        String   @id @default(uuid())
  userId    String   @unique
  balance   Int      @default(0)  // Credits remaining
  lifetime  Int      @default(0)  // Total credits ever acquired
  updatedAt DateTime @updatedAt

  user         User              @relation(fields: [userId], references: [id])
  transactions CreditTransaction[]
}

model CreditTransaction {
  id              String          @id @default(uuid())
  creditBalanceId String
  amount          Int             // Positive = add, negative = consume
  type            CreditTxType
  description     String?
  referenceId     String?         // Stripe payment ID, AI session ID, etc.
  createdAt       DateTime        @default(now())

  creditBalance   CreditBalance   @relation(fields: [creditBalanceId], references: [id])
}

enum CreditTxType {
  PURCHASE          // Bought with Stripe
  SUBSCRIPTION      // Monthly allocation from plan
  UET_EXCHANGE      // Converted from UET Coin
  AI_USAGE          // Consumed by AI API call
  BONUS             // Free credits (signup, promo)
  REFUND            // Refunded credits
  ADMIN_ADJUSTMENT  // Manual adjustment by admin
}

model Subscription {
  id                String   @id @default(uuid())
  userId            String   @unique
  stripeCustomerId  String?  @unique
  stripeSubId       String?  @unique
  plan              PlanTier @default(FREE)
  status            SubStatus @default(ACTIVE)
  currentPeriodStart DateTime
  currentPeriodEnd   DateTime
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  user User @relation(fields: [userId], references: [id])
}

enum PlanTier {
  FREE
  PRO
  ENTERPRISE
}

enum SubStatus {
  ACTIVE
  PAST_DUE
  CANCELED
  TRIALING
}
`

---

## 4. Subscription Plans

| Feature | Free | Pro (/mo) | Enterprise (Custom) |
|---------|------|-------------|---------------------|
| Monthly Credits | 500 | 50,000 | Unlimited |
| AI Models | Standard | All models | All + custom |
| Workchat Sessions | 10/day | Unlimited | Unlimited |
| Knowledge Base Size | 100 docs | 10,000 docs | Unlimited |
| Workspace Members | 5 | 50 | Unlimited |
| Video Call Duration | 30 min/day | Unlimited | Unlimited |
| Priority Support | Community | Email | 24/7 Dedicated |
| Credit Top-up | Yes (/5000 cr) | Yes (/5000 cr) | Invoice billing |

---

## 5. AI Usage Metering

### 5.1 Credit Cost Table
| Action | Credits | Approx. Cost |
|--------|---------|-------------|
| Chat message (standard) | 1-5 | ~.001-0.005 |
| Chat message (reasoning model) | 5-20 | ~.005-0.02 |
| Document ingestion (per page) | 2 | ~.002 |
| OmegaSearch query | 1 | ~.001 |
| Image generation | 10 | ~.01 |
| Voice transcription (per minute) | 5 | ~.005 |

### 5.2 Metering Middleware
`	ypescript
// middleware/creditCheck.ts
export async function checkCredits(userId: string, estimatedCost: number) {
  const balance = await prisma.creditBalance.findUnique({
    where: { userId }
  });
  
  if (!balance || balance.balance < estimatedCost) {
    throw new InsufficientCreditsError(balance?.balance || 0, estimatedCost);
  }
}

export async function deductCredits(userId: string, amount: number, description: string) {
  await prisma.([
    prisma.creditBalance.update({
      where: { userId },
      data: { balance: { decrement: amount } }
    }),
    prisma.creditTransaction.create({
      data: {
        creditBalance: { connect: { userId } },
        amount: -amount,
        type: 'AI_USAGE',
        description
      }
    })
  ]);
}
`

### 5.3 Integration Points
`
User sends chat message
  → creditCheck middleware (enough credits?)
  → Python Agent processes request
  → Count tokens used in response
  → deductCredits(userId, tokenCost, 'chat-session-xyz')
  → Return response to user
`

---

## 6. Stripe Integration

### 6.1 Webhook Events to Handle
| Stripe Event | Action |
|-------------|--------|
| checkout.session.completed | Create/update subscription, add credits |
| customer.subscription.updated | Update plan tier |
| customer.subscription.deleted | Downgrade to Free |
| invoice.payment_succeeded | Allocate monthly credits |
| invoice.payment_failed | Mark subscription as past_due |

### 6.2 API Routes
| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/billing/checkout | Create Stripe checkout session |
| POST | /api/billing/webhook | Stripe webhook handler |
| GET | /api/billing/subscription | Get current subscription |
| POST | /api/billing/credits/purchase | Buy credit top-up |
| GET | /api/credits | Get credit balance + history |
| POST | /api/credits/exchange | UET Coin → Credits exchange |

### 6.3 Checkout Flow
`
1. User clicks ""Upgrade to Pro"" on /pricing
2. POST /api/billing/checkout → creates Stripe Checkout Session
3. Redirect to Stripe Checkout page
4. User pays → Stripe webhook fires
5. Webhook handler:
   a. Creates Subscription record
   b. Adds monthly credits to CreditBalance
   c. Updates User plan
6. User redirected back to /account with Pro badge
`

---

## 7. UET Coin → Credit Exchange

### 7.1 Exchange Rate
- Default: 1 UET Coin = 100 Credits
- Rate stored in platform config (adjustable)
- Future: governed by uet_governance proposals

### 7.2 Exchange Flow
`
1. User navigates to /account → Wallet tab
2. Clicks ""Exchange to Credits""
3. Enters UET Coin amount
4. System shows credit equivalent
5. Confirm → deduct from Wallet.balance, add to CreditBalance
6. Both transactions logged
`

---

## 8. Free Tier Provisions

### 8.1 Signup Bonus
- New users get 500 credits on registration
- One-time bonus, logged as BONUS type

### 8.2 Monthly Reset (Free Tier)
- Free users get 500 credits refreshed monthly
- Unused credits do NOT roll over (Free tier only)
- Pro/Enterprise credits DO roll over

### 8.3 Earning Free Credits
- Complete profile: +100 credits
- First post on feed: +50 credits
- Verify research contribution: +200 credits
- Refer a user: +500 credits (both get it)

---

## 9. UI Pages

| Route | Description |
|-------|-------------|
| /pricing | Plan comparison (existing, wire to Stripe) |
| /account | Credit balance shown in overview |
| /account/billing | Subscription management, payment history |
| /account/credits | Credit balance, transaction history, top-up |

### 9.1 Credit Balance Widget (Dashboard)
`
┌─────────────────────────────────┐
│  Credits: 47,320 / 50,000      │
│  ████████████████░░░  94.6%    │
│  Plan: Pro  |  Renews: Apr 20  │
│  [Top Up]  [View History]       │
└─────────────────────────────────┘
`

---

## 10. Implementation Steps

1. Add CreditBalance, CreditTransaction, Subscription models to Prisma
2. Create credit check + deduction middleware
3. Wire Stripe SDK (stripe npm package)
4. Create billing API routes (checkout, webhook, subscription)
5. Update /pricing page to call Stripe checkout
6. Add credit balance widget to /account
7. Create /account/billing and /account/credits pages
8. Wire credit check into AI chat flow (Python agent proxy)
9. Add signup bonus logic
10. Add UET Coin → Credit exchange flow