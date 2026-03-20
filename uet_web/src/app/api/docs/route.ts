import { NextRequest, NextResponse } from 'next/server';
import { getAllDocs } from '@/lib/docs';

// Simple API to provide all docs for client-side Fuse.js searching
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const locale = searchParams.get('locale') || 'en';
  const docs = getAllDocs(locale);
  return NextResponse.json(docs);
}
