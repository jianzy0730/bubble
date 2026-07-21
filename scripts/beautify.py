from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

INDEX_STYLE = r'''
<!-- soft-fox-refresh -->
<meta name="theme-color" content="#f6eee8">
<style>
    :root {
        --ink: #3f3735;
        --muted: #8a7770;
        --fox: #c8755d;
        --fox-deep: #a95743;
        --cream: #fffaf5;
        --paper: rgba(255, 252, 248, 0.72);
        --line: rgba(126, 84, 67, 0.12);
        --soft-shadow: 0 24px 70px rgba(112, 72, 56, 0.12);
    }

    body {
        color: var(--ink);
        background:
            radial-gradient(circle at 14% 16%, rgba(255,255,255,.95) 0 7%, transparent 28%),
            radial-gradient(circle at 82% 18%, rgba(238,192,176,.28), transparent 29%),
            radial-gradient(circle at 52% 105%, rgba(202,148,124,.28), transparent 43%),
            linear-gradient(135deg, #fffdf9 0%, #f8f0e9 46%, #f5e9e3 100%);
    }

    body::before,
    body::after {
        content: "";
        position: fixed;
        border-radius: 999px;
        filter: blur(2px);
        pointer-events: none;
        z-index: 1;
        opacity: .8;
    }

    body::before {
        width: 28rem;
        height: 28rem;
        left: -13rem;
        bottom: -13rem;
        border: 1px solid rgba(199,125,99,.14);
        box-shadow: inset 0 0 80px rgba(255,255,255,.65);
    }

    body::after {
        width: 18rem;
        height: 18rem;
        right: -8rem;
        top: 24%;
        background: rgba(255,255,255,.18);
        border: 1px solid rgba(255,255,255,.58);
        box-shadow: 0 24px 80px rgba(199,125,99,.10);
    }

    .texture-overlay { opacity: .55; }

    .glass {
        background: linear-gradient(145deg, rgba(255,255,255,.76), rgba(255,248,242,.48));
        border: 1px solid rgba(255,255,255,.74);
        box-shadow: 0 14px 42px rgba(91,56,43,.09), inset 0 1px 0 rgba(255,255,255,.8);
        backdrop-filter: blur(22px) saturate(120%);
        -webkit-backdrop-filter: blur(22px) saturate(120%);
    }

    header {
        width: min(1180px, calc(100% - 40px)) !important;
        left: 50% !important;
        transform: translateX(-50%);
        padding: 22px 0 0 !important;
    }

    header > div:first-child {
        min-height: 48px;
        padding: 7px 14px 7px 8px !important;
        border-radius: 18px !important;
    }

    #avatar-wrap {
        width: 34px !important;
        height: 34px !important;
        border-color: rgba(255,255,255,.86) !important;
    }

    #display-name {
        color: var(--muted) !important;
        letter-spacing: .12em !important;
        font-family: ui-sans-serif, system-ui, sans-serif;
    }

    header > div:last-child {
        gap: 3px !important;
        padding: 5px;
        border: 1px solid rgba(255,255,255,.74);
        border-radius: 18px;
        background: rgba(255,250,246,.56);
        box-shadow: 0 14px 38px rgba(92,57,44,.08);
        backdrop-filter: blur(22px);
    }

    header > div:last-child > button,
    header > div:last-child > a {
        width: 38px !important;
        height: 38px !important;
        border: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
        color: #92776e !important;
    }

    header > div:last-child > button:hover,
    header > div:last-child > a:hover {
        color: var(--fox-deep) !important;
        background: rgba(199,125,99,.10) !important;
        transform: translateY(-1px);
    }

    .brand-panel {
        position: absolute;
        z-index: 22;
        top: 22%;
        left: max(6vw, calc((100vw - 1180px) / 2));
        width: min(390px, 34vw);
        pointer-events: none;
        animation: brandIn .9s cubic-bezier(.2,.75,.25,1) both;
    }

    .brand-eyebrow {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
        color: #9d7568;
        font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
        letter-spacing: .22em;
        text-transform: uppercase;
    }

    .brand-eyebrow span {
        width: 28px;
        height: 1px;
        background: var(--fox);
    }

    .brand-panel h1 {
        margin: 0;
        color: #433936;
        font-size: clamp(2.45rem, 4.3vw, 4.6rem);
        line-height: 1.08;
        letter-spacing: -.055em;
        font-weight: 700;
        text-shadow: 0 1px 0 rgba(255,255,255,.65);
    }

    .brand-panel h1 em {
        color: var(--fox);
        font-style: normal;
        font-family: 'Ma Shan Zheng', cursive;
        font-weight: 400;
        letter-spacing: -.01em;
    }

    .brand-panel p {
        max-width: 320px;
        margin: 22px 0 0;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.9;
        letter-spacing: .04em;
    }

    .brand-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 24px;
    }

    .brand-tags span {
        padding: 8px 12px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: rgba(255,255,255,.38);
        color: #92776e;
        font: 500 11px/1 ui-sans-serif, system-ui, sans-serif;
        letter-spacing: .05em;
    }

    #stage {
        mask-image: linear-gradient(to bottom, transparent 0, #000 7%, #000 82%, transparent 100%);
        -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 7%, #000 82%, transparent 100%);
    }

    .bubble-physics { filter: drop-shadow(0 18px 24px rgba(132,91,75,.08)); }

    .bubble-body {
        background:
            radial-gradient(circle at 28% 22%, rgba(255,255,255,.98) 0 4%, rgba(255,255,255,.42) 10%, transparent 23%),
            radial-gradient(circle at 72% 76%, var(--bubble-color-dark) 0%, transparent 44%),
            radial-gradient(circle at 34% 34%, rgba(255,255,255,.24), var(--bubble-color) 72%, rgba(255,255,255,.18) 100%) !important;
        border: 1px solid rgba(255,255,255,.78) !important;
        box-shadow:
            inset 8px 8px 22px rgba(255,255,255,.5),
            inset -8px -10px 25px rgba(147,94,75,.08),
            0 18px 38px rgba(120,78,61,.11) !important;
        backdrop-filter: blur(2px);
    }

    .bubble-text {
        color: rgba(70,57,53,.82) !important;
        font-size: .88rem !important;
        letter-spacing: .06em !important;
        text-shadow: 0 1px 8px rgba(255,255,255,.9) !important;
    }

    footer {
        left: auto !important;
        right: max(5vw, calc((100vw - 1180px) / 2));
        width: min(430px, calc(100% - 36px)) !important;
        padding: 0 0 34px !important;
        align-items: stretch !important;
        gap: 14px !important;
    }

    footer > .relative.group {
        align-self: center;
        margin-bottom: -4px;
    }

    footer > .relative.group > div:nth-child(2) {
        width: 92px !important;
        height: 92px !important;
        background: linear-gradient(145deg, rgba(255,255,255,.95), rgba(255,245,239,.82)) !important;
        border-width: 6px !important;
        box-shadow: 0 24px 55px rgba(167,92,67,.19) !important;
    }

    .fox-caption {
        text-align: center;
        color: #a1877d;
        font: 500 11px/1.5 ui-sans-serif, system-ui, sans-serif;
        letter-spacing: .08em;
    }

    footer .max-w-sm { max-width: none !important; }

    #mood-input {
        height: 48px !important;
        color: var(--ink) !important;
        font-family: 'Noto Serif SC', serif;
    }

    #mood-input::placeholder { color: #ad9991 !important; }

    #mood-input + button {
        width: 44px !important;
        height: 44px !important;
        background: linear-gradient(145deg, #d18469, #b8614a) !important;
        box-shadow: 0 10px 24px rgba(177,83,60,.26) !important;
    }

    footer .glass.rounded-full {
        padding: 5px 6px 5px 20px !important;
        border-radius: 21px !important;
    }

    footer .glass.rounded-2xl {
        border-radius: 18px !important;
        padding: 9px 11px !important;
    }

    #modal-container .modal-card,
    #history-panel .sheet {
        border-radius: 26px !important;
        border: 1px solid rgba(255,255,255,.86) !important;
        background: rgba(255,252,249,.88) !important;
        box-shadow: var(--soft-shadow) !important;
    }

    #history-panel .sheet { max-width: 760px !important; }
    .history-card { background: rgba(255,255,255,.62) !important; }

    @keyframes brandIn {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 860px) {
        header {
            width: calc(100% - 24px) !important;
            padding-top: 12px !important;
        }

        header > div:first-child { min-height: 44px; }
        header > div:last-child { max-width: 52vw; overflow-x: auto; scrollbar-width: none; }
        header > div:last-child::-webkit-scrollbar { display: none; }

        .brand-panel {
            top: 94px;
            left: 22px;
            width: calc(100% - 44px);
            text-align: center;
        }

        .brand-eyebrow { justify-content: center; margin-bottom: 9px; }
        .brand-panel h1 { font-size: clamp(1.75rem, 8vw, 2.55rem); line-height: 1.08; }
        .brand-panel h1 br { display: none; }
        .brand-panel p { display: none; }
        .brand-tags { display: none; }

        footer {
            right: 50%;
            transform: translateX(50%);
            width: calc(100% - 28px) !important;
            padding-bottom: max(18px, env(safe-area-inset-bottom)) !important;
        }

        footer > .relative.group > div:nth-child(2) {
            width: 76px !important;
            height: 76px !important;
        }

        .fox-caption { display: none; }
        #stage { mask-image: none; -webkit-mask-image: none; }
    }

    @media (max-width: 520px) {
        #display-name { max-width: 94px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        header > div:last-child { max-width: 49vw; }
        header > div:last-child > button,
        header > div:last-child > a { width: 36px !important; height: 36px !important; flex: 0 0 auto; }
        .brand-panel { top: 84px; }
        .brand-panel h1 { font-size: 1.72rem; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; }
    }
</style>
'''

BRAND_PANEL = r'''
    <section class="brand-panel" aria-label="产品介绍">
        <div class="brand-eyebrow"><span></span> mood bubble studio</div>
        <h1>把说不出口的<br><em>心情吹成泡泡。</em></h1>
        <p>写下一句话，让它慢慢浮起来。戳破泡泡时，你会听见一份只属于此刻的温柔回应。</p>
        <div class="brand-tags" aria-hidden="true">
            <span>轻触互动</span><span>智能回复</span><span>本地记录</span>
        </div>
    </section>
'''

FOX_CAPTION = r'''
        <div class="fox-caption">点点小狐狸，或者写下此刻的心情</div>
'''

SETTINGS_STYLE = r'''
<!-- soft-fox-settings-refresh -->
<meta name="theme-color" content="#f7efe9">
<style>
    :root {
        --ink: #423936;
        --muted: #917c73;
        --fox: #c8755d;
        --fox-deep: #a95743;
        --paper: rgba(255,252,249,.78);
        --line: rgba(126,84,67,.13);
    }

    body {
        background:
            radial-gradient(circle at 8% 8%, rgba(255,255,255,.95), transparent 29%),
            radial-gradient(circle at 92% 18%, rgba(231,170,150,.22), transparent 28%),
            linear-gradient(135deg, #fffdf9, #f7eee8 58%, #f3e4de) !important;
        color: var(--ink) !important;
    }

    body::before {
        content: "";
        position: fixed;
        width: 34rem;
        height: 34rem;
        right: -18rem;
        bottom: -19rem;
        border-radius: 50%;
        border: 1px solid rgba(199,125,99,.14);
        box-shadow: inset 0 0 90px rgba(255,255,255,.5);
        pointer-events: none;
    }

    body > .max-w-3xl {
        max-width: 1080px !important;
        padding-bottom: 50px;
    }

    body > .max-w-3xl > header {
        position: sticky;
        top: 12px;
        z-index: 30;
        padding: 12px 16px !important;
        border: 1px solid rgba(255,255,255,.78) !important;
        border-radius: 20px;
        background: rgba(255,251,247,.64);
        box-shadow: 0 18px 52px rgba(101,64,49,.08);
        backdrop-filter: blur(22px);
    }

    body > .max-w-3xl > header h1 {
        color: var(--ink) !important;
        letter-spacing: -.03em;
    }

    body > .max-w-3xl > header > div > div:first-child {
        background: linear-gradient(145deg, #d4866b, #b75e48) !important;
        box-shadow: 0 10px 24px rgba(169,79,57,.22) !important;
    }

    .settings-intro {
        display: grid;
        grid-template-columns: 1.2fr .8fr;
        gap: 18px;
        align-items: end;
        padding: 32px 4px 6px;
    }

    .settings-intro .eyebrow {
        color: #9e7769;
        font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
        letter-spacing: .22em;
        text-transform: uppercase;
    }

    .settings-intro h2 {
        margin: 12px 0 0;
        color: var(--ink);
        font-size: clamp(2rem, 4vw, 3.4rem);
        line-height: 1.12;
        letter-spacing: -.045em;
    }

    .settings-intro h2 em {
        color: var(--fox);
        font-style: normal;
        font-family: 'Ma Shan Zheng', cursive;
        font-weight: 400;
    }

    .settings-intro p {
        margin: 0;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.8;
        text-align: right;
    }

    .glass-card {
        background: linear-gradient(145deg, rgba(255,255,255,.78), rgba(255,248,243,.54)) !important;
        border: 1px solid rgba(255,255,255,.8) !important;
        box-shadow: 0 18px 52px rgba(101,64,49,.08), inset 0 1px 0 rgba(255,255,255,.82) !important;
        backdrop-filter: blur(22px) saturate(115%) !important;
    }

    body > .max-w-3xl > .flex.gap-3 {
        width: 100% !important;
        border-radius: 18px !important;
        padding: 5px !important;
    }

    .tab-btn { flex: 1; border-radius: 14px !important; padding-top: 11px !important; padding-bottom: 11px !important; }
    .tab-btn.active { background: linear-gradient(145deg, #d18469, #b7614a) !important; box-shadow: 0 8px 20px rgba(173,81,59,.2) !important; }

    .tab-panel { border-radius: 26px !important; padding: clamp(18px, 3vw, 34px) !important; }
    .tab-panel h2 { color: #966f62 !important; }

    .tab-panel .bg-white\/30,
    .tab-panel .hover\:bg-white\/50:hover {
        background: rgba(255,255,255,.47) !important;
    }

    .tab-panel .rounded-xl { border-radius: 18px !important; }

    .input-fox {
        min-height: 42px;
        border-radius: 12px !important;
        border-color: rgba(154,102,82,.16) !important;
        background: rgba(255,255,255,.68) !important;
        color: var(--ink) !important;
    }

    .input-fox:focus {
        border-color: rgba(199,117,93,.7) !important;
        box-shadow: 0 0 0 4px rgba(199,117,93,.10) !important;
    }

    .btn-fox { background: linear-gradient(145deg, #d18469, #b7614a) !important; box-shadow: 0 9px 20px rgba(173,81,59,.18); }
    .btn-fox-outline { border-color: rgba(160,103,81,.18) !important; background: rgba(255,255,255,.35) !important; }

    @media (max-width: 720px) {
        body { padding: 12px !important; }
        body > .max-w-3xl > header { top: 8px; }
        .settings-intro { grid-template-columns: 1fr; padding: 24px 4px 2px; }
        .settings-intro p { text-align: left; }
        .settings-intro h2 { font-size: 2.1rem; }
    }
</style>
'''

SETTINGS_INTRO = r'''
        <section class="settings-intro">
            <div>
                <div class="eyebrow">personalize your bubble space</div>
                <h2>把这里调成<br><em>你喜欢的样子。</em></h2>
            </div>
            <p>模型、声音、头像与泡泡质感都在这里配置。所有偏好仍然只保存在当前浏览器。</p>
        </section>
'''

README = r'''# Bubble · 小狐狸情绪泡泡机

一个轻量、温柔的情绪互动网页。写下一句话，它会变成缓慢上浮的泡泡；戳破泡泡后，可以获得本地预设或大模型生成的回应，并选择使用语音播放。

## 功能

- 3D 质感泡泡与碰撞动画
- 自定义心情、颜色、头像与狐狸图片
- OpenAI / Google Gemini 智能回复
- MiniMax TTS 语音回复
- 本地历史记录与备注
- 自定义背景音乐
- 响应式桌面与移动端界面

## 使用

这是一个纯前端项目，不需要构建步骤。

```bash
python -m http.server 8000
```

浏览器打开 `http://localhost:8000`。也可以直接部署到 GitHub Pages、Vercel 或任意静态网站托管服务。

> API Key 会写入浏览器 LocalStorage。不要在公共或不可信设备上保存真实密钥，也不要把密钥直接提交到仓库。

## 页面

- `index.html`：情绪泡泡主界面
- `settings.html`：模型、语音、个人资料与主题设置

## 技术

HTML、Tailwind CSS CDN、Font Awesome、原生 JavaScript 与 LocalStorage。
'''


def insert_before(text: str, marker: str, payload: str) -> str:
    if payload.strip().splitlines()[0] in text:
        return text
    if marker not in text:
        raise RuntimeError(f"marker not found: {marker}")
    return text.replace(marker, payload + "\n" + marker, 1)


def refresh_index(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "soft-fox-refresh" not in text:
        text = insert_before(text, "</head>", INDEX_STYLE)
        text = insert_before(text, "    <!-- Game Stage -->", BRAND_PANEL)
        text = insert_before(text, "        <!-- Controls Container -->", FOX_CAPTION)
        text = re.sub(r"<title>.*?</title>", "<title>Bubble · 小狐狸情绪泡泡机</title>", text, count=1)
    path.write_text(text, encoding="utf-8")


def refresh_settings(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "soft-fox-settings-refresh" not in text:
        text = insert_before(text, "</head>", SETTINGS_STYLE)
        text = insert_before(text, "        <!-- Tabs -->", SETTINGS_INTRO)
        text = re.sub(r"<title>.*?</title>", "<title>Bubble · 个性化设置</title>", text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    refresh_index(ROOT / "index.html")
    refresh_settings(ROOT / "settings.html")
    (ROOT / "README.md").write_text(README, encoding="utf-8")
    print("Soft fox refresh applied.")


if __name__ == "__main__":
    main()
