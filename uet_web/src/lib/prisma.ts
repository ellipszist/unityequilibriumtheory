import { PrismaClient } from '@prisma/client'

const prismaClientSingleton = () => new PrismaClient()

declare global {
  var prismaGlobal: undefined | ReturnType<typeof prismaClientSingleton>
}

export function getPrisma() {
  if (process.env.NODE_ENV === 'production') {
    return prismaClientSingleton()
  }

  if (!globalThis.prismaGlobal) {
    globalThis.prismaGlobal = prismaClientSingleton()
  }

  return globalThis.prismaGlobal
}