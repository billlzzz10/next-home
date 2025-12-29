import Link from 'next/link'

export default function Hero() {
  return (
    <section className="relative text-center py-20">
      <div className="absolute inset-0 bg-grid-circuit pointer-events-none"></div>
      <img src="/assets/blinkos-logo.svg" alt="BlinkOS Logo" className="mx-auto mb-4 w-24 relative z-10" />
      <h1 className="text-4xl md:text-6xl font-bold relative z-10">Build Deterministic Agents with BlinkOS</h1>
      <p className="mt-4 text-lg text-purple-300 relative z-10">Explicit. Audit-friendly. Agent-first.</p>
      <div className="mt-6 flex justify-center gap-4 relative z-10">
        <Link href="/start"><a className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded">Start Building</a></Link>
        <Link href="/doc"><a className="px-6 py-3 border border-purple-400 hover:bg-purple-900 rounded">View Docs</a></Link>
      </div>
    </section>
  )
}
