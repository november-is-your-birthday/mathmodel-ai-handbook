# -*- coding: utf-8 -*-
"""
把《数学建模AI手册.md》渲染成单文件 HTML（精美版）。
特性：亮/暗双主题、侧边可折叠目录树 + 滚动高亮、阅读进度条、全文搜索 + 关键词高亮、
     代码块一键复制、表格自适应、★ 标记高亮。仅依赖同目录 marked.min.js，产物离线可用。
用法：python build_manual_html.py
"""
import json, pathlib

BASE      = pathlib.Path(__file__).resolve().parent
MD_PATH   = BASE / "数学建模AI手册.md"
OUT_PATH  = BASE / "数学建模AI手册.html"
MARKED    = BASE / "marked.min.js"

md_text     = MD_PATH.read_text(encoding="utf-8")
marked_text = MARKED.read_text(encoding="utf-8")
if "</script" in marked_text:
    marked_text = marked_text.replace("</script", "<\\/script")
md_json = json.dumps(md_text, ensure_ascii=False).replace("</", "<\\/")

APP_JS = r"""
(function () {
  const $  = (s) => document.querySelector(s);
  const mdSource = JSON.parse(document.getElementById('md-source').textContent);
  const content  = document.getElementById('content');

  /* ---------- 渲染 ---------- */
  let html = marked.parse(mdSource, { gfm: true, breaks: false });
  html = html.replace(/★/g, '<span class="star">★</span>');
  content.innerHTML = html;
  content.querySelectorAll('a[href^="http"]').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  content.querySelectorAll('table').forEach(t => {
    const w = document.createElement('div'); w.className = 'twrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  /* ---------- 代码块：复制按钮 ---------- */
  content.querySelectorAll('pre').forEach(pre => {
    const bar = document.createElement('div');
    bar.className = 'codebar';
    bar.innerHTML = '<span></span><button class="copybtn" type="button">复制</button>';
    const wrap = document.createElement('div'); wrap.className = 'codewrap';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(bar); wrap.appendChild(pre);
    bar.querySelector('.copybtn').addEventListener('click', async (e) => {
      const text = pre.innerText;
      let ok = true;
      try { await navigator.clipboard.writeText(text); }
      catch (_) {
        try {
          const ta = document.createElement('textarea'); ta.value = text;
          document.body.appendChild(ta); ta.select();
          ok = document.execCommand('copy'); ta.remove();
        } catch (_) { ok = false; }
      }
      const btn = e.currentTarget;
      btn.textContent = ok ? '已复制 ✓' : '复制失败';
      setTimeout(() => { btn.textContent = '复制'; }, 1600);
    });
  });

  /* ---------- 按 H1/H2 切分成 section ---------- */
  const kids = Array.from(content.children);
  let cur = null;
  const sections = [];
  for (const el of kids) {
    if (/^H[12]$/.test(el.tagName)) {
      cur = document.createElement('section');
      cur.className = 'sec';
      content.insertBefore(cur, el);
      cur.appendChild(el);
      sections.push(cur);
    } else {
      if (!cur) {
        cur = document.createElement('section'); cur.className = 'sec';
        content.insertBefore(cur, el); sections.push(cur);
      }
      cur.appendChild(el);
    }
  }

  /* ---------- id + 侧边目录树 ---------- */
  const usedIds = new Set();
  const slug = (text) => {
    let s = text.toLowerCase().replace(/[^\w\u4e00-\u9fff\- ]/g, '').trim().replace(/ +/g, '-');
    if (!s) s = 'sec';
    let out = s, i = 2;
    while (usedIds.has(out)) out = s + '-' + (i++);
    usedIds.add(out); return out;
  };
  const toc = document.getElementById('toc');
  let group = null;   // 当前 details 组
  const crumbMap = new Map();
  sections.forEach(sec => {
    const h = sec.querySelector('h1, h2, h3');
    if (!h) return;
    const id = slug(h.textContent);
    h.id = id; sec.dataset.title = h.textContent;
    if (h.tagName === 'H1') {
      group = document.createElement('details'); group.open = true; group.className = 'tgroup';
      const sum = document.createElement('summary'); sum.textContent = h.textContent;
      group.appendChild(sum); toc.appendChild(group);
      if (sec.querySelector('h1 + * , h1')) sec.dataset.part = h.textContent;
    }
    const a = document.createElement('a');
    a.href = '#' + id; a.textContent = h.textContent;
    a.className = h.tagName === 'H2' ? 'lvl1' : 'lvl2';
    (group || toc).appendChild(a);
    crumbMap.set(sec, a);
  });

  /* ---------- 滚动高亮（scrollspy）---------- */
  const crumb = document.getElementById('crumb');
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        const link = crumbMap.get(en.target);
        if (link) {
          toc.querySelectorAll('a.active').forEach(x => x.classList.remove('active'));
          link.classList.add('active');
          link.scrollIntoView({ block: 'nearest' });
          crumb.textContent = en.target.dataset.title || '';
          if (link.parentElement && link.parentElement.tagName === 'DETAILS') link.parentElement.open = true;
        }
      }
    });
  }, { rootMargin: '-70px 0px -72% 0px' });
  sections.forEach(s => spy.observe(s));

  /* ---------- 主题 ---------- */
  const root = document.documentElement;
  const themeBtn = document.getElementById('theme');
  const applyTheme = (t) => {
    root.setAttribute('data-theme', t);
    themeBtn.textContent = t === 'dark' ? '☀️' : '🌙';
    try { localStorage.setItem('manual-theme', t); } catch (_) {}
  };
  let saved = null; try { saved = localStorage.getItem('manual-theme'); } catch (_) {}
  applyTheme(saved || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  themeBtn.addEventListener('click', () =>
    applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));

  /* ---------- 进度条 / 回到顶部 ---------- */
  const pbar = document.getElementById('pbar');
  addEventListener('scroll', () => {
    const h = document.documentElement;
    const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    pbar.style.width = (p * 100).toFixed(2) + '%';
  }, { passive: true });
  document.getElementById('backtop').addEventListener('click', () =>
    window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* ---------- 搜索：过滤章节 + 高亮关键词 ---------- */
  const input = document.getElementById('search');
  const status = document.getElementById('search-status');
  const highlight = (sec, q) => {
    const walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.parentNode && /^[A-Z]+$/.test(n.parentNode.nodeName)) || n.nodeValue.length < 1
        ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    const hits = [];
    while (walker.nextNode()) hits.push(walker.currentNode);
    hits.forEach(node => {
      const low = node.nodeValue.toLowerCase();
      let idx = low.indexOf(q);
      if (idx === -1) return;
      const frag = document.createDocumentFragment();
      let pos = 0;
      while (idx !== -1) {
        frag.appendChild(document.createTextNode(node.nodeValue.slice(pos, idx)));
        const m = document.createElement('mark');
        m.textContent = node.nodeValue.slice(idx, idx + q.length);
        frag.appendChild(m);
        pos = idx + q.length;
        idx = low.indexOf(q, pos);
      }
      frag.appendChild(document.createTextNode(node.nodeValue.slice(pos)));
      node.parentNode.replaceChild(frag, node);
    });
  };
  const runSearch = () => {
    const q = input.value.trim().toLowerCase();
    let hits = 0;
    sections.forEach(sec => {
      if (sec._orig === undefined) sec._orig = sec.innerHTML;
      sec.innerHTML = sec._orig;                       // 先还原，避免 mark 叠加
      const match = !q || sec.textContent.toLowerCase().includes(q);
      sec.style.display = match ? '' : 'none';
      if (q && match) { hits++; highlight(sec, q); }
    });
    status.textContent = q ? (hits ? hits + ' 个章节匹配' : '无匹配') : '';
  };
  input.addEventListener('input', runSearch);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { input.value = ''; runSearch(); input.blur(); }
  });
  addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== input) { e.preventDefault(); input.focus(); }
  });
})();
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数学建模 AI 手册 · 提示词 × 资源库</title>
<style>
  :root{
    --bg:#ffffff; --bg2:#f6f8fa; --text:#1c2128; --muted:#697180; --border:#e5e8ee;
    --accent:#4f46e5; --accent2:#2563eb; --star:#f59e0b; --codebg:#f7f8fa;
    --topbar:rgba(255,255,255,.82); --mark:#fff1a8; --shadow:0 1px 2px rgba(16,24,40,.05),0 4px 16px rgba(16,24,40,.05);
  }
  [data-theme="dark"]{
    --bg:#0d1017; --bg2:#11151f; --text:#e7eaf0; --muted:#98a2b3; --border:#232a37;
    --accent:#9aa6ff; --accent2:#6cb5ff; --star:#fbbf24; --codebg:#151b28;
    --topbar:rgba(13,16,23,.82); --mark:#6b5b00; --shadow:0 1px 2px rgba(0,0,0,.5),0 6px 24px rgba(0,0,0,.35);
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--text);
       font-family:"Segoe UI Variable Text","Segoe UI",system-ui,"Microsoft YaHei","PingFang SC",sans-serif;
       font-size:15px}
  ::selection{background:color-mix(in srgb,var(--accent) 26%,transparent)}

  /* ===== 侧栏 ===== */
  #sidebar{position:fixed;inset:0 auto 0 0;width:302px;display:flex;flex-direction:column;
           background:var(--bg2);border-right:1px solid var(--border);z-index:30}
  .brand{display:flex;align-items:center;gap:11px;padding:16px 16px 10px}
  .logo{width:40px;height:40px;border-radius:12px;flex:none;display:grid;place-items:center;
        background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;font-weight:800;font-size:15px;
        box-shadow:0 4px 12px color-mix(in srgb,var(--accent) 40%,transparent)}
  .brand .t1{font-weight:750;font-size:15px;letter-spacing:.2px}
  .brand .t2{font-size:11px;color:var(--muted);margin-top:2px}
  .searchwrap{padding:4px 14px 8px}
  #search{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg);
          color:var(--text);font-size:13px;outline:none;transition:.15s}
  #search:focus{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent)}
  #search-status{font-size:11px;color:var(--muted);min-height:16px;padding:3px 4px 0}
  #toc{flex:1;overflow-y:auto;padding:2px 10px 14px;scrollbar-width:thin}
  details.tgroup{margin:4px 0}
  details.tgroup>summary{cursor:pointer;user-select:none;list-style:none;display:flex;align-items:center;gap:7px;
    padding:8px 10px;margin:10px 0 5px;border-radius:9px;font-weight:800;font-size:15px;color:var(--text);
    letter-spacing:.4px;line-height:1.45;word-break:break-word;
    text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:2px;
    text-decoration-color:var(--accent)}
  details.tgroup>summary::-webkit-details-marker{display:none}
  details.tgroup>summary::before{content:"▸";font-size:10px;transition:transform .15s;color:var(--accent)}
  details.tgroup[open]>summary::before{transform:rotate(90deg)}
  details.tgroup>summary:hover{background:color-mix(in srgb,var(--accent) 8%,transparent)}
  .toc a{display:block;color:var(--text);text-decoration:none;padding:5px 10px;margin:1px 0;
         border-radius:8px;font-size:13px;line-height:1.5;border:1px solid transparent}
  .toc a:hover{background:color-mix(in srgb,var(--accent) 9%,transparent)}
  .toc a.lvl1{font-weight:520}
  .toc a.lvl2{padding-left:26px;font-size:12px;color:var(--muted)}
  .toc a.active{background:color-mix(in srgb,var(--accent) 14%,transparent);color:var(--accent);
                font-weight:650;border-color:color-mix(in srgb,var(--accent) 25%,transparent)}
  .sidefoot{padding:10px 16px;border-top:1px solid var(--border);font-size:11px;color:var(--muted);line-height:1.7}

  /* ===== 主区 ===== */
  main{margin-left:302px;min-height:100vh}
  .topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:10px;
          padding:10px 26px;background:var(--topbar);backdrop-filter:blur(10px);
          border-bottom:1px solid var(--border)}
  #crumb{font-size:12.5px;color:var(--muted);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .topbar button{border:1px solid var(--border);background:var(--bg);color:var(--text);width:32px;height:32px;
                 border-radius:9px;cursor:pointer;font-size:14px;transition:.15s}
  .topbar button:hover{border-color:var(--accent);transform:translateY(-1px)}
  #pbarwrap{position:absolute;left:0;right:0;bottom:-1px;height:2px}
  #pbar{height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--accent2))}
  #content{max-width:900px;margin:0 auto;padding:30px 40px 110px}

  /* 文档首屏 */
  .sec:first-child h1{font-size:29px;letter-spacing:.3px;margin:14px 0 10px;
    background:linear-gradient(100deg,var(--text) 55%,var(--accent));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
  h1,h2,h3{scroll-margin-top:70px;line-height:1.4}
  h1{font-size:23px;margin:64px 0 18px;padding:13px 18px;border-radius:12px;
     border-left:4px solid var(--accent);
     background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 12%,transparent),transparent 70%);
     box-shadow:var(--shadow)}
  h2{font-size:19.5px;margin:46px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border);
     display:flex;align-items:center;gap:9px}
  h2::before{content:"";width:5px;height:18px;border-radius:3px;flex:none;
             background:linear-gradient(180deg,var(--accent),var(--accent2))}
  h3{font-size:16px;margin:30px 0 10px}
  p,li{line-height:1.85;font-size:14.5px}
  .star{color:var(--star);text-shadow:0 0 8px color-mix(in srgb,var(--star) 45%,transparent)}

  /* 表格 */
  .twrap{overflow-x:auto;border:1px solid var(--border);border-radius:12px;margin:14px 0;box-shadow:var(--shadow)}
  table{border-collapse:collapse;width:100%;font-size:13.5px}
  th,td{padding:9px 13px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border)}
  th{background:var(--bg2);font-weight:650;white-space:nowrap;position:sticky;top:0}
  tbody tr:last-child td{border-bottom:none}
  tbody tr:hover td{background:color-mix(in srgb,var(--accent) 5%,transparent)}

  /* 代码块 */
  .codewrap{margin:14px 0;border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}
  .codebar{display:flex;justify-content:space-between;align-items:center;padding:6px 12px;
           background:var(--bg2);border-bottom:1px solid var(--border);font-size:11px;color:var(--muted)}
  .copybtn{border:1px solid var(--border);background:var(--bg);color:var(--muted);border-radius:6px;
           padding:2px 10px;font-size:11px;cursor:pointer}
  .copybtn:hover{color:var(--accent);border-color:var(--accent)}
  pre{margin:0;background:var(--codebg);padding:15px 17px;overflow-x:auto;
      font-family:Consolas,"Cascadia Mono","Courier New",monospace;font-size:13px;line-height:1.65}
  code{background:color-mix(in srgb,var(--accent) 8%,transparent);padding:1.5px 6px;border-radius:5px;
       font-family:Consolas,"Cascadia Mono",monospace;font-size:.92em}
  pre code{background:none;padding:0}

  /* 引用框 */
  blockquote{border:1px solid color-mix(in srgb,var(--accent) 24%,transparent);
             border-left:4px solid var(--accent);background:color-mix(in srgb,var(--accent) 6%,transparent);
             margin:14px 0;padding:10px 18px;border-radius:0 12px 12px 0}
  blockquote p{margin:7px 0}
  mark{background:var(--mark);color:inherit;border-radius:3px;padding:0 2px}
  hr{border:none;border-top:1px solid var(--border);margin:30px 0}
  a{color:var(--accent2)}

  .fab{position:fixed;right:26px;bottom:26px;display:flex;flex-direction:column;gap:10px;z-index:25}
  .fab button{width:44px;height:44px;border:none;border-radius:14px;cursor:pointer;font-size:17px;
              background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;
              box-shadow:0 6px 18px color-mix(in srgb,var(--accent) 45%,transparent);transition:.15s}
  .fab button:hover{transform:translateY(-2px)}
  ::-webkit-scrollbar{width:9px;height:9px}
  ::-webkit-scrollbar-thumb{background:color-mix(in srgb,var(--muted) 35%,transparent);border-radius:6px}
  ::-webkit-scrollbar-thumb:hover{background:var(--muted)}
  @media (max-width:1024px){#sidebar{display:none}main{margin-left:0}.topbar{padding:10px 18px}#content{padding:22px 20px 90px}}
  @media print{#sidebar,.topbar,.fab{display:none}main{margin:0}#content{max-width:none;padding:0}}
</style>
</head>
<body>
<nav id="sidebar">
  <div class="brand">
    <div class="logo">数模</div>
    <div><div class="t1">数学建模 AI 手册</div><div class="t2">提示词 × 资源库 · 2026-09</div></div>
  </div>
  <div class="searchwrap">
    <input id="search" type="search" placeholder="搜索章节内容…（按 / 聚焦）">
    <div id="search-status"></div>
  </div>
  <div id="toc" class="toc"></div>
  <div class="sidefoot">单文件 · 离线可用<br>改 MD 后可重新生成 HTML</div>
</nav>
<main>
  <header class="topbar">
    <div id="crumb">数学建模 AI 手册</div>
    <div id="pbarwrap"><div id="pbar"></div></div>
  </header>
  <div id="content"></div>
</main>
<div class="fab">
  <button id="backtop" title="回到顶部">↑</button>
  <button id="theme" title="切换亮/暗主题">🌙</button>
</div>
<script type="text/plain" id="md-source">__MD__</script>
<script>__MARKED__</script>
<script>__APP__</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("__MARKED__", marked_text)
        .replace("__APP__", APP_JS)
        .replace("__MD__", md_json))
OUT_PATH.write_text(html, encoding="utf-8")
print(f"OK  {OUT_PATH}  ({OUT_PATH.stat().st_size/1024:.0f} KB)")
