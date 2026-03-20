import { NextResponse } from 'next/server'
import { randomUUID } from 'crypto'

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File | null
    const userId = formData.get('userId') as string | null
    const postId = formData.get('postId') as string | null

    if (!file || !userId) {
      return NextResponse.json({ error: 'file and userId are required' }, { status: 400 })
    }

    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      return NextResponse.json({ error: 'File too large (max 10MB)' }, { status: 400 })
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'video/mp4']
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json({ error: 'File type not allowed' }, { status: 400 })
    }

    const ext = file.name.split('.').pop() || 'bin'
    const key = `uploads/${userId}/${randomUUID()}.${ext}`

    // Check if R2 is configured
    const r2AccountId = process.env.R2_ACCOUNT_ID
    const r2AccessKey = process.env.R2_ACCESS_KEY_ID
    const r2SecretKey = process.env.R2_SECRET_ACCESS_KEY
    const r2Bucket = process.env.R2_BUCKET_NAME || 'uet-media'

    if (r2AccountId && r2AccessKey && r2SecretKey) {
      // Upload to Cloudflare R2 via S3 API
      const { S3Client, PutObjectCommand } = await import('@aws-sdk/client-s3')

      const s3 = new S3Client({
        region: 'auto',
        endpoint: `https://${r2AccountId}.r2.cloudflarestorage.com`,
        credentials: {
          accessKeyId: r2AccessKey,
          secretAccessKey: r2SecretKey,
        },
      })

      const buffer = Buffer.from(await file.arrayBuffer())

      await s3.send(new PutObjectCommand({
        Bucket: r2Bucket,
        Key: key,
        Body: buffer,
        ContentType: file.type,
      }))

      const url = `https://pub-${r2AccountId}.r2.dev/${key}`

      return NextResponse.json({
        url,
        key,
        filename: file.name,
        size: file.size,
        type: file.type,
        storage: 'r2',
      })
    }

    // Fallback: save locally in /public/uploads (dev mode only)
    const fs = await import('fs/promises')
    const path = await import('path')
    const uploadDir = path.join(process.cwd(), 'public', 'uploads', userId)
    await fs.mkdir(uploadDir, { recursive: true })

    const filename = `${randomUUID()}.${ext}`
    const filepath = path.join(uploadDir, filename)
    const buffer = Buffer.from(await file.arrayBuffer())
    await fs.writeFile(filepath, buffer)

    const url = `/uploads/${userId}/${filename}`

    return NextResponse.json({
      url,
      key: `uploads/${userId}/${filename}`,
      filename: file.name,
      size: file.size,
      type: file.type,
      storage: 'local',
    })
  } catch (error) {
    console.error('Upload error:', error)
    return NextResponse.json({ error: 'Upload failed' }, { status: 500 })
  }
}
