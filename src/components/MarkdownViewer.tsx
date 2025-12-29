import ReactMarkdown from 'react-markdown'
import CopyButton from './CopyButton'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism'

export default function MarkdownViewer({ content }: { content: string }) {
  return (
    <article className="prose prose-invert max-w-none">
      <ReactMarkdown
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || '')
            const code = String(children).replace(/\n$/, '')
            return !inline && match ? (
              <div className="relative my-4 bg-[#071023] rounded p-3">
                <CopyButton text={code} />
                <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" {...props}>
                  {code}
                </SyntaxHighlighter>
              </div>
            ) : (
              <code className="bg-[#071023] px-1 rounded">{children}</code>
            )
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  )
}
