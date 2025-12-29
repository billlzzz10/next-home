export default function Footer() {
  return (
    <footer className="bg-black text-gray-400 text-sm py-12 px-6 mt-12">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h2 className="text-white font-bold mb-2">BlinkOS</h2>
          <ul className="space-y-1">
            <li><a href="/" className="hover:underline">Home</a></li>
            <li><a href="/doc" className="hover:underline">Docs</a></li>
            <li><a href="/asset" className="hover:underline">Asset</a></li>
          </ul>
        </div>
        <div>
          <h2 className="text-white font-bold mb-2">Connect</h2>
          <ul className="space-y-1">
            <li><a href="https://github.com/your-org/blinkos" target="_blank" rel="noreferrer" className="hover:underline">GitHub</a></li>
            <li><a href="https://discord.gg/your-server" target="_blank" rel="noreferrer" className="hover:underline">Discord</a></li>
            <li><a href="https://x.com/yourhandle" target="_blank" rel="noreferrer" className="hover:underline">X</a></li>
          </ul>
        </div>
        <div>
          <h2 className="text-white font-bold mb-2">Legal</h2>
          <ul className="space-y-1">
            <li><a href="/privacy" className="hover:underline">Privacy</a></li>
            <li><a href="/manifesto" className="hover:underline">Manifesto</a></li>
          </ul>
        </div>
      </div>
      <div className="mt-8 text-center text-xs text-gray-500">
        © {new Date().getFullYear()} BlinkOS. All rights reserved.
      </div>
    </footer>
  )
}
