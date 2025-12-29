import fs from 'fs'
import path from 'path'
import MarkdownViewer from '../../components/MarkdownViewer'
import DocNav from '../../components/DocNav'
import Footer from '../../components/Footer'

const SLUGS = ['agent','memory','audit']

export default function DocPage({ content, slug }: { content: string, slug: string }) {
  const idx = SLUGS.indexOf(slug)
  const prev = idx > 0 ? SLUGS[idx-1] : null
  const next = idx < SLUGS.length-1 ? SLUGS[idx+1] : null

  return (
    <main className="min-h-screen px-6 py-12 max-w-4xl mx-auto">
      <MarkdownViewer content={content} />
      <DocNav prev={prev} next={next} />
      <div className="mt-6">
        <a href="/" className="text-sm text-purple-300 hover:underline">← Back to Home</a>
      </div>
      <Footer />
    </main>
  )
}

export async function getStaticPaths() {
  const paths = ['agent','memory','audit'].map(s => ({ params: { slug: s } }))
  return { paths, fallback: false }
}

export async function getStaticProps({ params }: { params: { slug: string } }) {
  const filePath = path.join(process.cwd(), `src/content/doc/${params.slug}.md`)
  const content = fs.readFileSync(filePath, 'utf8')
  return { props: { content, slug: params.slug } }
}
