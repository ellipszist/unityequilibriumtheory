import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const projects = await (prisma as any).project.findMany({
      where: { workspaceId: params.id },
      include: {
        tasks: {
          include: {
            assignee: {
              select: { id: true, email: true, name: true } as any,
            },
          },
          orderBy: { createdAt: 'desc' },
        },
        _count: { select: { tasks: true } },
      },
      orderBy: { updatedAt: 'desc' },
    })
    return NextResponse.json(projects)
  } catch (error) {
    console.error('Error fetching workspace tasks:', error)
    return NextResponse.json({ error: 'Failed to fetch tasks' }, { status: 500 })
  }
}

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const prisma = getPrisma()
    const { projectId, title, description, bountyAmount, assigneeId, userId } = await request.json()

    if (!title || !userId) {
      return NextResponse.json({ error: 'title and userId required' }, { status: 400 })
    }

    // Verify membership
    const member = await (prisma as any).workspaceMember.findUnique({
      where: { workspaceId_userId: { workspaceId: params.id, userId } },
    })
    if (!member) {
      return NextResponse.json({ error: 'Not a member' }, { status: 403 })
    }

    // Auto-create project if none specified
    let targetProjectId = projectId
    if (!targetProjectId) {
      const defaultProject = await (prisma as any).project.findFirst({
        where: { workspaceId: params.id, name: 'Default' },
      })
      if (defaultProject) {
        targetProjectId = defaultProject.id
      } else {
        const newProject = await (prisma as any).project.create({
          data: {
            workspaceId: params.id,
            ownerId: userId,
            name: 'Default',
            description: 'Default project board',
          },
        })
        targetProjectId = newProject.id
      }
    }

    const task = await prisma.task.create({
      data: {
        projectId: targetProjectId,
        title,
        description: description || '',
        bountyAmount: bountyAmount || 0,
        assigneeId: assigneeId || null,
      },
      include: {
        assignee: { select: { id: true, email: true, name: true } as any },
      },
    })

    return NextResponse.json(task, { status: 201 })
  } catch (error) {
    console.error('Error creating task:', error)
    return NextResponse.json({ error: 'Failed to create task' }, { status: 500 })
  }
}
