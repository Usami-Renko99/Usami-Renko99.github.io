const { chromium } = require("C:/Users/OriginObserver/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.60.0/node_modules/playwright");

const url = process.argv[2];

if (!url) {
  console.error("Usage: node scripts/fetch_zhihu_article.js <url>");
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    headless: true,
    args: ["--disable-blink-features=AutomationControlled"],
  });
  const context = await browser.newContext({
    locale: "zh-CN",
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
  });
  await context.addInitScript(() => {
    Object.defineProperty(navigator, "webdriver", { get: () => undefined });
  });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(8000);

  const data = await page.evaluate(() => {
    const pick = (...selectors) => {
      for (const selector of selectors) {
        const element = document.querySelector(selector);
        if (element) return element;
      }
      return null;
    };

    const titleElement = pick(".Post-Title", "h1.Post-Title", "h1");
    const contentElement = pick(".Post-RichTextContainer", ".RichText", "article");
    const dateElement = pick("[itemprop='datePublished']", ".ContentItem-time", "time");
    const state = document.querySelector("#js-initialData")?.textContent || "";

    return {
      title: titleElement?.textContent || document.title,
      date: dateElement?.getAttribute("datetime") || dateElement?.textContent || "",
      html: contentElement?.innerHTML || "",
      text: contentElement?.innerText || document.body.innerText,
      href: location.href,
      titleFromDocument: document.title,
      initialDataLength: state.length,
      bodyStart: document.body.innerText.slice(0, 1000),
    };
  });

  const markdown = await page.evaluate(() => {
    const escapeMd = (value) => value.replace(/([\\`*_{}\[\]()#+\-.!|>])/g, "\\$1");
    const nodeToMarkdown = (node, context = {}) => {
      if (!node) return "";
      if (node.nodeType === Node.TEXT_NODE) return node.nodeValue || "";
      if (node.nodeType !== Node.ELEMENT_NODE) return "";

      const tag = node.tagName.toLowerCase();
      const children = () => Array.from(node.childNodes).map((child) => nodeToMarkdown(child, context)).join("");
      const inline = () => children().replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n");

      if (["script", "style", "noscript", "svg"].includes(tag)) return "";
      if (tag === "br") return "\n";
      if (tag === "p") return `${inline().trim()}\n\n`;
      if (/^h[1-6]$/.test(tag)) return `${"#".repeat(Number(tag[1]))} ${inline().trim()}\n\n`;
      if (tag === "strong" || tag === "b") return `**${inline().trim()}**`;
      if (tag === "em" || tag === "i") return `*${inline().trim()}*`;
      if (tag === "code") return context.inPre ? node.textContent || "" : `\`${node.textContent || ""}\``;
      if (tag === "pre") return `\n\`\`\`\n${node.textContent || ""}\n\`\`\`\n\n`;
      if (tag === "blockquote") return `${inline().trim().split("\n").map((line) => `> ${line}`).join("\n")}\n\n`;
      if (tag === "a") {
        const href = node.getAttribute("href") || "";
        const label = inline().trim() || href;
        return href ? `[${label}](${href})` : label;
      }
      if (tag === "img") {
        const src = node.getAttribute("src") || node.getAttribute("data-original") || "";
        const alt = node.getAttribute("alt") || "";
        return src ? `![${escapeMd(alt)}](${src})\n\n` : "";
      }
      if (tag === "figure") return `${inline().trim()}\n\n`;
      if (tag === "figcaption") return `_${inline().trim()}_\n\n`;
      if (tag === "ul" || tag === "ol") {
        return `${Array.from(node.children).map((child, index) => nodeToMarkdown(child, { ...context, listTag: tag, index })).join("").trim()}\n\n`;
      }
      if (tag === "li") {
        const marker = context.listTag === "ol" ? `${context.index + 1}. ` : "- ";
        const body = inline().trim().replace(/\n+/g, "\n  ");
        return `${marker}${body}\n`;
      }
      if (tag === "hr") return "---\n\n";
      if (tag === "table") return `${node.innerText.trim()}\n\n`;

      return children();
    };

    const contentElement =
      document.querySelector(".Post-RichTextContainer") ||
      document.querySelector(".RichText") ||
      document.querySelector("article");
    return contentElement ? nodeToMarkdown(contentElement).trim() : "";
  });

  await browser.close();

  data.markdown = markdown;
  console.log(JSON.stringify(data, null, 2));
})();
