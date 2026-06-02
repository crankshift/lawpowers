import { readdirSync, readFileSync } from "node:fs"
import { dirname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../..")
const JURISDICTIONS = ["pl", "ua"]
const FRONTMATTER_RE = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/

function parseFrontmatter(markdown) {
  const match = markdown.match(FRONTMATTER_RE)
  if (!match) return { metadata: {}, body: markdown }

  const metadata = {}
  for (const line of match[1].split("\n")) {
    if (!line.trim() || line.startsWith(" ")) continue
    const separator = line.indexOf(":")
    if (separator === -1) continue
    const key = line.slice(0, separator).trim()
    const value = line.slice(separator + 1).trim().replace(/^["']|["']$/g, "")
    metadata[key] = value
  }

  return { metadata, body: match[2] }
}

function loadAgents() {
  const agents = {}
  for (const jurisdiction of JURISDICTIONS) {
    const directory = join(ROOT, "agents", jurisdiction)
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) continue
      const file = join(directory, entry.name)
      const { metadata, body } = parseFrontmatter(readFileSync(file, "utf8"))
      const name = metadata.name || entry.name.replace(/\.md$/, "")
      agents[name] = {
        description: metadata.description,
        mode: "subagent",
        prompt: body.trim(),
      }
    }
  }
  return agents
}

function skillPaths() {
  return JURISDICTIONS.map((jurisdiction) => join(ROOT, "skills", jurisdiction))
}

export default async function lawpowers() {
  return {
    config(cfg) {
      cfg.skills = {
        ...(cfg.skills || {}),
        paths: [...new Set([...(cfg.skills?.paths || []), ...skillPaths()])],
      }
      cfg.agent = { ...(cfg.agent || {}), ...loadAgents() }
    },
  }
}
