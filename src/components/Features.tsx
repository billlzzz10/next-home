export default function Features() {
  const items = [
    { title: 'Logic Flow', desc: 'Explicit deterministic branching', icon: '⟲' },
    { title: 'Memory Graph', desc: 'Persistent vector memory', icon: '▦' },
    { title: 'Audit Trail', desc: 'Immutable action logs', icon: '✱' }
  ]
  return (
    <section className="py-12">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {items.map(i => (
          <div key={i.title} className="p-6 bg-[#081022] rounded border border-purple-800">
            <div className="text-2xl mb-3">{i.icon}</div>
            <h3 className="font-semibold text-xl">{i.title}</h3>
            <p className="mt-2 text-sm text-purple-200">{i.desc}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
