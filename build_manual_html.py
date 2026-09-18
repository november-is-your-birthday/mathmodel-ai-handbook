# -*- coding: utf-8 -*-
"""
把《数学建模AI手册.md》渲染成单文件 HTML（精美版）。
特性：亮/暗双主题、侧边可折叠目录树 + 滚动高亮、阅读进度条、全文搜索 + 关键词高亮、
     代码块一键复制、表格自适应、★ 标记高亮。仅依赖同目录 marked.min.js，产物离线可用。
主题：Neubrutalism（硬边框 3px / 硬投影 5px 5px 0 / 高饱和平色 / 零渐变 / 直角）。
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
      sum.title = '展开 / 收起「' + h.textContent + '」';
      group.appendChild(sum); toc.appendChild(group);
      if (sec.querySelector('h1 + * , h1')) sec.dataset.part = h.textContent;
      // 组标题本身即这一节的入口，不再生成重复的叶链接（否则每部分会出现两行同名条目）
      crumbMap.set(sec, sum);
      return;
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
          toc.querySelectorAll('a.active, summary.active').forEach(x => x.classList.remove('active'));
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
  const ICON_MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.6 8.6 0 1 1 9.8 3.5a6.9 6.9 0 0 0 10.7 10.7Z"/></svg>';
  const ICON_SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.2v2.4M12 19.4v2.4M2.2 12h2.4M19.4 12h2.4M5 5l1.7 1.7M17.3 17.3 19 19M19 5l-1.7 1.7M6.7 17.3 5 19"/></svg>';
  const applyTheme = (t) => {
    root.setAttribute('data-theme', t);
    themeBtn.innerHTML = t === 'dark' ? ICON_SUN : ICON_MOON;
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
/* ============================================================
   Neubrutalism theme — 数学建模 AI 手册
   Spec source: ui-ux-pro-max / styles.csv#neubrutalism
     · border: 3px solid #000        · box-shadow: 5px 5px 0 #000
     · no gradients / no blur        · sharp corners (0px)
     · high-saturation flat colors   · bold typography
   Typography pairing: "Neubrutalist Bold" (Lexend Mega + Public Sans)
     — listed as local-first fallbacks, no webfont request, so the
       single file stays fully offline-capable.
   ============================================================ */

/* ---------- 设计令牌 ---------- */
:root{
  /* 平面 / 文字 */
  --bg:#FFFBF0;            /* 暖纸底 */
  --bg2:#FFFFFF;
  --text:#0B0B0B;
  --muted:#4A4A4A;
  --ink:#000000;           /* 硬边框 / 硬投影颜色 */
  --link:#1D4ED8;          /* 正文链接：白底 6.4:1 */
  --codebg:#FFFFFF;

  /* 高饱和主色（技能指定 #FFEB3B / #FF5252 / #2196F3 谱系） */
  --accent:#FFD93D;        /* 黄 · 主强调 */
  --accent2:#4D96FF;       /* 蓝 · 次级 */
  --accent3:#FF6B6B;       /* 红 · 标记 */
  --accent4:#6BCB77;       /* 绿 · 成功 */
  --star:#FFB020;

  /* 硬几何 */
  --fw:3px;                /* 边框宽 */
  --so:5px;                /* 投影位移 */
  --shadow:var(--so) var(--so) 0 var(--ink);
  --shadow-sm:3px 3px 0 var(--ink);
  --topbar:#FFFBF0;
  --mark:#FFD93D;
}
[data-theme="dark"]{
  --bg:#121216;
  --bg2:#1A1A20;
  --text:#F7F7F5;
  --muted:#A9A9B4;         /* 深底 8.1:1 */
  --ink:#F2F2EF;           /* 深色主题下边框翻转为浅色 */
  --link:#9CC7FF;
  --codebg:#1A1A20;

  --accent:#FFD93D;
  --accent2:#7FB2FF;
  --accent3:#FF8080;
  --accent4:#7FD68A;
  --star:#FFC552;

  --topbar:#121216;
  --mark:#FFD93D;
}

/* ---------- 基础 ---------- */
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
     font-family:"Public Sans","Lexend Mega","Segoe UI Variable Text","Segoe UI",system-ui,"Microsoft YaHei","PingFang SC",sans-serif;
     font-size:15px;-webkit-font-smoothing:antialiased}
::selection{background:var(--accent);color:#0B0B0B}
:focus-visible{outline:var(--fw) solid var(--accent2);outline-offset:2px}

/* ---------- 侧栏 ---------- */
#sidebar{position:fixed;inset:0 auto 0 0;width:302px;display:flex;flex-direction:column;
         background:var(--bg2);border-right:var(--fw) solid var(--ink);z-index:30}
.brand{display:flex;align-items:center;gap:12px;padding:18px 16px 12px}
.logo{width:44px;height:44px;flex:none;display:grid;place-items:center;
      background:var(--accent3);color:#0B0B0B;font-weight:900;font-size:15px;letter-spacing:.5px;
      border:var(--fw) solid var(--ink);box-shadow:var(--shadow-sm)}
.brand .t1{font-weight:900;font-size:15px;letter-spacing:.3px;line-height:1.3}
.brand .t2{font-size:11px;color:var(--muted);margin-top:3px;font-weight:700;letter-spacing:.6px}

.searchwrap{padding:6px 14px 10px}
#search{width:100%;padding:9px 12px;border:var(--fw) solid var(--ink);background:var(--bg);color:var(--text);
        font-size:13px;font-weight:600;outline:none;transition:box-shadow .12s,transform .12s}
#search::placeholder{color:var(--muted);opacity:1;font-weight:500}
#search:focus{box-shadow:var(--shadow);transform:translate(-1px,-1px)}
#search-status{font-size:11px;font-weight:800;color:var(--muted);min-height:16px;padding:5px 2px 0;letter-spacing:.3px}

#toc{flex:1;overflow-y:auto;padding:2px 12px 16px}
details.tgroup{margin:6px 0}
details.tgroup>summary{cursor:pointer;user-select:none;list-style:none;display:flex;align-items:center;gap:8px;
  padding:9px 11px;margin:12px 0 6px;font-weight:900;font-size:15px;line-height:1.45;word-break:break-word;
  letter-spacing:.3px;color:#0B0B0B;background:var(--accent);
  border:var(--fw) solid var(--ink);box-shadow:var(--shadow-sm);
  transition:transform .12s,box-shadow .12s}
details.tgroup>summary::-webkit-details-marker{display:none}
details.tgroup>summary::before{content:"▸";font-size:11px;line-height:1;transition:transform .15s}
details.tgroup[open]>summary::before{transform:rotate(90deg)}
details.tgroup>summary:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
details.tgroup>summary.active{background:var(--accent2);box-shadow:var(--shadow-sm)}
details.tgroup>summary.active::before{color:#0B0B0B}
.toc a{display:block;color:var(--text);text-decoration:none;padding:6px 10px;margin:3px 0;font-size:13px;line-height:1.5;
       border:2px solid transparent;
       transition:transform .12s,box-shadow .12s,background .12s,color .12s}
.toc a:hover{background:var(--accent);color:#0B0B0B;border-color:var(--ink);font-weight:700;
             transform:translate(-2px,-2px);box-shadow:3px 3px 0 var(--ink)}
.toc a.lvl1{font-weight:700}
.toc a.lvl2{padding-left:26px;font-size:12px;color:var(--muted)}
.toc a.lvl2:hover{color:#0B0B0B}
.toc a.active{background:var(--accent2);color:#0B0B0B;border-color:var(--ink);font-weight:900;
              box-shadow:var(--shadow-sm)}
.sidefoot{padding:11px 16px;border-top:var(--fw) solid var(--ink);background:var(--bg2);
          font-size:11px;font-weight:700;color:var(--muted);line-height:1.7;letter-spacing:.3px}

/* ---------- 主区 ---------- */
main{margin-left:302px;min-height:100vh}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:10px;
        padding:11px 26px;background:var(--topbar);border-bottom:var(--fw) solid var(--ink)}
#crumb{font-size:12.5px;font-weight:800;color:var(--text);flex:1;white-space:nowrap;overflow:hidden;
       text-overflow:ellipsis;letter-spacing:.3px}
.topbar button{border:var(--fw) solid var(--ink);background:var(--accent);color:#0B0B0B;width:34px;height:34px;
               cursor:pointer;font-size:14px;font-weight:900;box-shadow:var(--shadow-sm);
               transition:transform .12s,box-shadow .12s}
.topbar button:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
#pbarwrap{position:absolute;left:0;right:0;bottom:-3px;height:5px;background:transparent}
#pbar{height:100%;width:0;background:var(--accent3);border-right:2px solid var(--ink)}
#content{max-width:900px;margin:0 auto;padding:34px 40px 120px}

/* ---------- 标题 ---------- */
h1,h2,h3{scroll-margin-top:80px;line-height:1.4}
h1,h2,h3,.brand .t1,details.tgroup>summary{font-family:"Lexend Mega","Public Sans","Segoe UI Variable Text","Segoe UI",system-ui,"Microsoft YaHei","PingFang SC",sans-serif}

/* 文档首屏大标题：双层硬投影 */
.sec:first-child h1{font-size:33px;font-weight:900;letter-spacing:.5px;line-height:1.35;
  margin:18px 0 20px;padding:22px 26px;background:var(--accent);color:#0B0B0B;
  border:var(--fw) solid var(--ink);
  box-shadow:7px 7px 0 var(--ink),14px 14px 0 var(--accent2)}

h1{font-size:23px;font-weight:900;letter-spacing:.4px;margin:66px 0 22px;padding:15px 20px;
   background:var(--accent);color:#0B0B0B;border:var(--fw) solid var(--ink);box-shadow:var(--shadow)}

h2{font-size:19.5px;font-weight:900;letter-spacing:.3px;margin:48px 0 16px;padding:0 0 11px 15px;
   display:flex;align-items:center;gap:11px;border-bottom:var(--fw) solid var(--ink)}
h2::before{content:"";width:14px;height:14px;flex:none;background:var(--accent3);
           border:2.5px solid var(--ink)}

h3{font-size:16px;font-weight:900;letter-spacing:.2px;margin:32px 0 12px;display:inline-block;
   padding:4px 11px;background:var(--accent4);color:#0B0B0B;
   border:2.5px solid var(--ink);box-shadow:var(--shadow-sm)}

p,li{line-height:1.85;font-size:14.5px}
strong,b{font-weight:800}
.star{color:var(--star);font-weight:900}

/* ---------- 表格 ---------- */
.twrap{overflow-x:auto;margin:16px 0;background:var(--bg2);
       border:var(--fw) solid var(--ink);box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:10px 13px;text-align:left;vertical-align:top;
      border-bottom:2px solid var(--ink);border-right:2px solid var(--ink)}
th:last-child,td:last-child{border-right:none}
th{background:var(--accent);color:#0B0B0B;font-weight:900;white-space:nowrap;letter-spacing:.2px;
   border-bottom:var(--fw) solid var(--ink)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:color-mix(in srgb,var(--accent) 26%,transparent)}

/* ---------- 代码块 ---------- */
.codewrap{margin:16px 0;background:var(--bg2);overflow:hidden;
          border:var(--fw) solid var(--ink);box-shadow:var(--shadow)}
.codebar{display:flex;justify-content:space-between;align-items:center;padding:7px 12px;
         background:var(--accent);color:#0B0B0B;border-bottom:var(--fw) solid var(--ink)}
.codebar span{font-size:10.5px;font-weight:900;letter-spacing:1.2px}
.codebar span::before{content:"CODE"}
.copybtn{border:2.5px solid var(--ink);background:var(--bg2);color:#0B0B0B;
         padding:3px 12px;font-size:11px;font-weight:800;cursor:pointer;letter-spacing:.4px;
         box-shadow:2px 2px 0 var(--ink);transition:transform .1s,box-shadow .1s,background .1s}
.copybtn:hover{background:var(--accent4)}
.copybtn:active{transform:translate(2px,2px);box-shadow:0 0 0 var(--ink)}
pre{margin:0;background:var(--codebg);padding:16px 18px;overflow-x:auto;
    font-family:"JetBrains Mono","Cascadia Mono",Consolas,"Courier New",monospace;
    font-size:13px;line-height:1.7}
code{background:var(--accent);color:#0B0B0B;padding:1.5px 6px;font-weight:700;
     font-family:"JetBrains Mono","Cascadia Mono",Consolas,monospace;font-size:.88em;
     border:2px solid var(--ink)}
pre code{background:transparent;border:none;padding:0;font-weight:400;color:var(--text)}

/* ---------- 引用 / 杂项 ---------- */
blockquote{margin:16px 0;padding:12px 20px;background:var(--bg2);
           border:var(--fw) solid var(--ink);border-left:12px solid var(--accent3);
           box-shadow:var(--shadow-sm)}
blockquote p{margin:7px 0}
blockquote strong{background:var(--accent);padding:0 3px}
mark{background:var(--mark);color:#0B0B0B;padding:1px 3px;font-weight:700}
hr{border:none;border-top:var(--fw) dashed var(--ink);margin:34px 0}
a{color:var(--link);font-weight:600;text-decoration-thickness:2px;text-underline-offset:3px}
a:hover{background:var(--accent);color:#0B0B0B;text-decoration:none}

/* ---------- 悬浮按钮 ---------- */
.fab{position:fixed;right:26px;bottom:26px;display:flex;flex-direction:column;gap:12px;z-index:25}
.fab button{width:50px;height:50px;display:grid;place-items:center;cursor:pointer;
            background:var(--accent);color:#0B0B0B;border:var(--fw) solid var(--ink);
            box-shadow:var(--shadow);transition:transform .12s,box-shadow .12s}
.fab button:hover{transform:translate(-3px,-3px);box-shadow:8px 8px 0 var(--ink)}
.fab button:active{transform:translate(5px,5px);box-shadow:0 0 0 var(--ink)}
.fab button#theme{background:var(--accent2)}
.fab svg{display:block;width:21px;height:21px}

/* ---------- 滚动条 ---------- */
::-webkit-scrollbar{width:14px;height:14px}
::-webkit-scrollbar-track{background:var(--bg2);border-left:2px solid var(--ink)}
::-webkit-scrollbar-thumb{background:var(--accent);border:2.5px solid var(--ink)}
::-webkit-scrollbar-thumb:hover{background:var(--accent3)}
#toc::-webkit-scrollbar{width:11px}

/* ---------- 响应式 / 无障碍 / 打印 ---------- */
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *{transition:none !important;animation:none !important}
  .toc a:hover,details.tgroup>summary:hover,.fab button:hover,
  #search:focus{transform:none}
}
@media (max-width:1024px){
  #sidebar{display:none}
  main{margin-left:0}
  .topbar{padding:11px 18px}
  #content{padding:24px 20px 100px}
  .sec:first-child h1{font-size:25px;padding:18px;box-shadow:5px 5px 0 var(--ink),10px 10px 0 var(--accent2)}
  h1{font-size:20px}
}
@media print{
  #sidebar,.topbar,.fab{display:none}
  main{margin:0}
  #content{max-width:none;padding:0}
  body{background:#fff}
  h1,.sec:first-child h1,th,.codebar,.logo{border-color:#000;box-shadow:none;background:#f2f2f2;color:#000}
  h3{background:#f2f2f2;color:#000;box-shadow:none}
  .twrap,.codewrap,blockquote{box-shadow:none;border-color:#000}
  a{color:#000}
}
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
  <button id="backtop" title="回到顶部"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
  <button id="theme" title="切换亮/暗主题"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.6 8.6 0 1 1 9.8 3.5a6.9 6.9 0 0 0 10.7 10.7Z"/></svg></button>
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
