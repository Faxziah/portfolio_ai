import { revalidatePath } from 'next/cache'
import { NextResponse } from 'next/server'

export async function POST() {
  try {
    revalidatePath('/', 'layout')
    return NextResponse.json({ revalidated: true, timestamp: new Date().toISOString() })
  } catch (error) {
    console.error('Revalidate error:', error)
    return NextResponse.json({ error: 'Failed to revalidate' }, { status: 500 })
  }
}
