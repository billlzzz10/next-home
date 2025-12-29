import Footer from '../components/Footer'
import Link from 'next/link'

export default function Asset() {
  return (
    <main className="min-h-screen px-6 py-12 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Assets</h1>
      <p className="mb-6 text-purple-200">Add your project links, images, and demos here.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-4 bg-[#081022] rounded">
          <h3 className="font-semibold">Project A</h3>
          <p className="text-sm text-purple-300">Replace with your content.</p>
        </div>
      </div>
      <div className="mt-8">
        <Link href="/doc"><a className="text-sm text-purple-300 hover:underline">Go to Docs →</a></Link>
      </div>
      <Footer />
    </main>
  )
}
