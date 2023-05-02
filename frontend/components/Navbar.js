import Link from 'next/link'
import { useState, useEffect } from 'react'

export default function Navbar() {
  return (
    <nav>
      <div><Link href="/">Home</Link></div>
      <div><Link href="/about">About</Link></div>
    </nav>
  )
}