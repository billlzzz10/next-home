export default function VectorMemory() {
  return (
    <section className="py-12">
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-6 items-center">
        <div>
          <h3 className="text-xl font-semibold">Vector Search + Memory</h3>
          <p className="text-purple-200 mt-2">HNSW indexing, PGVECTOR compatibility, memory nodes for agents.</p>
        </div>
        <div className="p-6 bg-[#071024] rounded">
          <div className="h-40 bg-gradient-to-br from-[#041226] to-[#2b0b3f] rounded flex items-center justify-center text-sm text-purple-300">HNSW Diagram (placeholder)</div>
        </div>
      </div>
    </section>
  )
}
