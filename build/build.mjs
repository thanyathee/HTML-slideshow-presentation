// Bundles the gradient background and copies html2canvas into ../assets
import { build } from 'esbuild'
import { copyFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const out = resolve(here, '../assets')
mkdirSync(out, { recursive: true })

await build({
  entryPoints: [resolve(here, 'bg.jsx')],
  outfile: resolve(out, 'bg.js'),
  bundle: true,
  minify: true,
  format: 'iife',
  jsx: 'automatic',
  target: 'es2019',
  define: { 'process.env.NODE_ENV': '"production"' },
  legalComments: 'none',
  logLevel: 'info'
})
copyFileSync(resolve(here, 'node_modules/html2canvas/dist/html2canvas.min.js'), resolve(out, 'html2canvas.min.js'))
console.log('done')
