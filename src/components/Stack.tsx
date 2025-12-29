export default function Stack() {
  const logos = ['Python','Rust','PowerShell','LangChain','Next.js']
  return (
    <section className="py-12">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-xl font-semibold mb-4">Works with your stack</h3>
        <div className="flex gap-6 items-center overflow-x-auto">
          {logos.map(l => <div key={l} className="px-4 py-2 bg-[#071026] rounded">{l}</div>)}
        </div>
      </div>
    </section>
  )
}
