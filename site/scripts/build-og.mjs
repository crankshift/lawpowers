// Build-time generator for the Open Graph / Twitter card image.
// Writes site/public/og.png at 1200×630. Run via `pnpm build:og`.
//
// The SVG source is authored here so we don't need a separate design file
// and so the image is reproducible from git history alone.

import sharp from 'sharp'
import { writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const outPath = join(__dirname, '..', 'public', 'og.png')

const W = 1200
const H = 630

// Tokens lifted from site/src/styles/global.css (light theme) so the card
// matches the landing. Hex equivalents — OG image must not depend on CSS.
const BG = '#fbf9f3'
const INK = '#272320'
const INK_2 = '#4a423c'
const INK_3 = '#786c62'
const ACCENT = '#a3443c'
const RULE = '#d9d1c4'

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <rect width="100%" height="100%" fill="${BG}"/>

  <!-- Hairline frame, echoes the minimal editorial style -->
  <rect x="48" y="48" width="${W - 96}" height="${H - 96}" fill="none"
        stroke="${RULE}" stroke-width="1"/>

  <!-- Top eyebrow / monospace kicker -->
  <text x="96" y="128"
        font-family="ui-monospace, 'SF Mono', Menlo, monospace"
        font-size="22" letter-spacing="4" fill="${INK_3}">
    OPEN-SOURCE · MIT · FOR CLAUDE CODE
  </text>

  <!-- § seal on the left, matches the site BrandMark -->
  <g transform="translate(96, 196)">
    <circle cx="44" cy="44" r="42" fill="none" stroke="${INK}" stroke-width="2"/>
    <circle cx="44" cy="44" r="36" fill="none" stroke="${INK}" stroke-width="1" opacity="0.35"/>
    <text x="44" y="62" text-anchor="middle"
          font-family="'Instrument Serif', Georgia, serif"
          font-size="54" font-style="italic" fill="${INK}">§</text>
  </g>

  <!-- Wordmark -->
  <text x="220" y="258"
        font-family="'Instrument Serif', Georgia, serif"
        font-size="64" font-weight="400" fill="${INK}">
    law<tspan font-style="italic" fill="${ACCENT}">·</tspan>powers
  </text>

  <!-- Headline, two lines, italic accent on the verb -->
  <text x="96" y="372"
        font-family="'Instrument Serif', Georgia, serif"
        font-size="72" font-weight="400" fill="${INK}" letter-spacing="-1.5">
    Jurisdiction-aware <tspan font-style="italic" fill="${ACCENT}">legal drafting,</tspan>
  </text>
  <text x="96" y="452"
        font-family="'Instrument Serif', Georgia, serif"
        font-size="72" font-weight="400" fill="${INK}" letter-spacing="-1.5">
    inside Claude Code.
  </text>

  <!-- Footer row: jurisdictions + URL -->
  <line x1="96" y1="498" x2="${W - 96}" y2="498" stroke="${RULE}" stroke-width="1"/>

  <text x="96" y="548"
        font-family="ui-monospace, 'SF Mono', Menlo, monospace"
        font-size="22" letter-spacing="2" fill="${INK_2}">
    /ua:… · /pl:…
  </text>

  <text x="${W - 96}" y="548" text-anchor="end"
        font-family="ui-monospace, 'SF Mono', Menlo, monospace"
        font-size="22" letter-spacing="2" fill="${INK_3}">
    lawpowers.web.app
  </text>
</svg>`

const png = await sharp(Buffer.from(svg))
  .resize(W, H)
  .png({ compressionLevel: 9 })
  .toBuffer()

writeFileSync(outPath, png)
console.log(`Wrote ${outPath} (${png.length.toLocaleString()} bytes)`)
