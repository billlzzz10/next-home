import { useState } from 'react'

export default function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)
  const handleCopy = async () => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }
  return (
    <button onClick={handleCopy} className="absolute top-3 right-3 bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 rounded text-sm">
      {copied ? 'Copied!' : 'Copy'}
    </button>
  )
}
