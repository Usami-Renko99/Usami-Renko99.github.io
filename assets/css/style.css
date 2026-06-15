:root {
  --text: #24292f;
  --muted: #6a737d;
  --border: #d8dee4;
  --bg: #ffffff;
  --soft: #f6f8fa;
  --link: #0969da;
  --accent: #7c3aed;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", "Noto Sans SC", sans-serif;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
}

.container {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 22px;
}

.site-header {
  border-bottom: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.92);
  position: sticky;
  top: 0;
  backdrop-filter: blur(8px);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
  gap: 24px;
}

.site-title {
  font-weight: 700;
  color: var(--text);
  text-decoration: none;
}

.site-nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.site-nav a {
  color: var(--muted);
  text-decoration: none;
}

.site-nav a:hover { color: var(--link); }

.page-content {
  padding-top: 36px;
  padding-bottom: 48px;
}

h1, h2, h3 {
  line-height: 1.25;
}

h1 {
  font-size: 2.25rem;
  margin: 0 0 1.2rem;
}

h2 {
  margin-top: 2.4rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid var(--border);
}

a { color: var(--link); }

code {
  background: var(--soft);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1rem 0.28rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 24px 0;
}

.tile, .note-card {
  display: block;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  text-decoration: none;
  background: var(--bg);
}

.tile:hover, .note-card:hover {
  border-color: var(--accent);
}

.tile strong {
  display: block;
  font-size: 1.1rem;
  color: var(--text);
}

.tile span, .meta, .muted {
  color: var(--muted);
  font-size: 0.95rem;
}

.note-section { margin-top: 32px; }
.note-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.note-card h3 {
  margin-top: 0;
  margin-bottom: 0.35rem;
}

.note-actions {
  margin-bottom: 0;
  display: flex;
  gap: 10px;
}

.button {
  display: inline-block;
  padding: 0.42rem 0.75rem;
  border-radius: 8px;
  background: var(--text);
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
}

.button.ghost {
  color: var(--text);
  background: var(--soft);
  border: 1px solid var(--border);
}

.empty-state {
  border: 1px dashed var(--border);
  border-radius: 12px;
  background: var(--soft);
  padding: 20px;
  margin-top: 20px;
}

.breadcrumb { color: var(--muted); }

.post-list {
  padding-left: 0;
  list-style: none;
}

.post-list li {
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.site-footer {
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.9rem;
  padding: 24px 0;
}

@media (max-width: 640px) {
  .header-inner { align-items: flex-start; flex-direction: column; padding: 14px 22px; }
  h1 { font-size: 1.8rem; }
  .post-list li { display: block; }
}
