import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function PUT(request: Request) {
  try {
    const prisma = getPrisma()
    const body = await request.json()
    const { userId, displayName, bio, institution, website } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const updated = await prisma.user.update({
      where: { id: userId },
      data: {
        ...(displayName !== undefined && { displayName } as any),
        ...(bio !== undefined && { bio } as any),
        ...(institution !== undefined && { institution } as any),
        ...(website !== undefined && { website } as any),
      },
      select: {
        id: true,
        email: true,
        name: true,
        reputation: true,
      } as any,
    })

    return NextResponse.json(updated)
  } catch (error) {
    console.error('Error updating profile:', error)
    return NextResponse.json({ error: 'Failed to update profile' }, { status: 500 })
  }
}
