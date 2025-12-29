export default function CodeSnippet() {
  const snippet = `import { blink } from '@blinkos/agent';
const agent = blink({ memory: true, flow: 'deterministic' });
await agent.run('summarize');`
  return (
    <section className="py-12">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-semibold mb-4">Quickstart</h2>
        <div className="relative bg-[#071024] rounded">
          <button
            onClick={() => navigator.clipboard.writeText(snippet)}
            className="absolute top-3 right-3 bg-purple-600 px-3 py-1 rounded text-sm"
          >
            Copy
          </button>
          <pre className="p-6 overflow-auto"><code>{snippet}</code></pre>
        </div>
      </div>
    </section>
  )
}
