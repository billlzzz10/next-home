export default function Trusted() {
  const logos = ['Chonost','ByteRover','CodexUI']
  return (
    <section className="py-12">
      <div className="max-w-6xl mx-auto">
        <h4 className="text-sm text-purple-300 mb-4">Trusted by</h4>
        <div className="flex gap-6">
          {logos.map(l => <div key={l} className="px-3 py-2 bg-[#071024] rounded text-sm">{l}</div>)}
        </div>
      </div>
    </section>
  )
}
