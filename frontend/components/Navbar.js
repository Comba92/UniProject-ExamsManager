import Link from 'next/link'

export default function Navbar() {
  return (
    <nav>
      <div><Link href="/">Home</Link></div>
      <div><Link href="/about">About</Link></div>
      <div><Link href="/">Logout</Link></div>
    </nav>
  )
}