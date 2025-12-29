import Hero from '../components/Hero'
import Features from '../components/Features'
import CodeSnippet from '../components/CodeSnippet'
import Stack from '../components/Stack'
import VectorMemory from '../components/VectorMemory'
import Trusted from '../components/Trusted'
import Footer from '../components/Footer'

export default function Home() {
  return (
    <main>
      <Hero />
      <Features />
      <CodeSnippet />
      <Stack />
      <VectorMemory />
      <Trusted />
      <Footer />
    </main>
  )
}
