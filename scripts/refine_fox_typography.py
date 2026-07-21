from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

index_path = ROOT / "index.html"
settings_path = ROOT / "settings.html"

index = index_path.read_text(encoding="utf-8")
settings = settings_path.read_text(encoding="utf-8")

font_link = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Noto+Serif+SC:wght@600;700&display=swap" rel="stylesheet">'
index = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Ma\+Shan\+Zheng&family=Noto\+Serif\+SC:[^"]+" rel="stylesheet">', font_link, index)
settings = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Ma\+Shan\+Zheng&family=Noto\+Serif\+SC:[^"]+" rel="stylesheet">', font_link, settings)

fox_svg = '''<svg id="fox-svg" class="fox-svg w-[76%] h-[76%]" viewBox="0 0 120 120" fill="none" aria-label="小狐狸头像">
                    <defs>
                        <linearGradient id="foxFur" x1="25" y1="24" x2="94" y2="102" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#E99373"/>
                            <stop offset="1" stop-color="#C96F52"/>
                        </linearGradient>
                    </defs>
                    <path class="fox-ear-left" d="M25 45L20 15L50 34L42 52Z" fill="url(#foxFur)"/>
                    <path class="fox-ear-right" d="M95 45L100 15L70 34L78 52Z" fill="url(#foxFur)"/>
                    <path d="M27 37L24 23L43 37L37 45Z" fill="#F8C2B2"/>
                    <path d="M93 37L96 23L77 37L83 45Z" fill="#F8C2B2"/>
                    <path d="M31 39C38 28 49 24 60 24C71 24 82 28 89 39C98 53 98 78 87 92C80 101 70 105 60 105C50 105 40 101 33 92C22 78 22 53 31 39Z" fill="url(#foxFur)"/>
                    <path d="M31 58C36 48 44 43 52 41C49 56 45 68 34 78C30 72 28 65 31 58Z" fill="#FFF4ED"/>
                    <path d="M89 58C84 48 76 43 68 41C71 56 75 68 86 78C90 72 92 65 89 58Z" fill="#FFF4ED"/>
                    <path d="M52 31L60 45L68 31L66 58L60 64L54 58Z" fill="#FFF8F3"/>
                    <ellipse cx="51" cy="72" rx="13" ry="11" fill="#FFF4ED"/>
                    <ellipse cx="69" cy="72" rx="13" ry="11" fill="#FFF4ED"/>
                    <ellipse class="fox-eye" cx="45" cy="61" rx="3.5" ry="4" fill="#49332D"/>
                    <ellipse class="fox-eye" cx="75" cy="61" rx="3.5" ry="4" fill="#49332D"/>
                    <circle cx="36" cy="72" r="4" fill="#EFA693" opacity="0.75"/>
                    <circle cx="84" cy="72" r="4" fill="#EFA693" opacity="0.75"/>
                    <path d="M55 72C56.5 69.8 63.5 69.8 65 72C63.8 75.7 61.9 77 60 77C58.1 77 56.2 75.7 55 72Z" fill="#49332D"/>
                    <path d="M60 77V80" stroke="#49332D" stroke-width="2" stroke-linecap="round"/>
                    <path d="M60 80C57.8 83.2 54.7 83.5 52.5 81.8" stroke="#49332D" stroke-width="2" stroke-linecap="round"/>
                    <path d="M60 80C62.2 83.2 65.3 83.5 67.5 81.8" stroke="#49332D" stroke-width="2" stroke-linecap="round"/>
                </svg>'''
index, replaced = re.subn(r'<svg id="fox-svg".*?</svg>', fox_svg, index, count=1, flags=re.S)
if replaced != 1:
    raise RuntimeError("fox svg not found")

index_css = '''
<!-- fox-and-type-refinement -->
<style>
    body,
    button,
    input,
    select,
    textarea {
        font-family: 'Noto Sans SC', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-variant-numeric: tabular-nums;
    }

    .brand-panel {
        width: min(540px, 42vw) !important;
    }

    .brand-panel h1 {
        font-family: 'Noto Sans SC', sans-serif !important;
        font-size: clamp(2.7rem, 3.9vw, 4.15rem) !important;
        font-weight: 700 !important;
        line-height: 1.18 !important;
        letter-spacing: -0.055em !important;
    }

    .brand-panel h1 em {
        display: inline-block;
        white-space: nowrap;
        font-family: 'Noto Sans SC', sans-serif !important;
        font-style: normal !important;
        font-weight: 700 !important;
        letter-spacing: -0.055em !important;
    }

    .brand-eyebrow {
        letter-spacing: .15em !important;
        font-weight: 600 !important;
    }

    .brand-panel p {
        max-width: 430px;
        color: #75625b !important;
        font-size: 14px !important;
        line-height: 1.85 !important;
        letter-spacing: 0 !important;
    }

    .brand-tags span,
    .fox-caption,
    #display-name {
        font-family: 'Noto Sans SC', sans-serif !important;
        letter-spacing: .04em !important;
    }

    #display-name {
        font-weight: 500 !important;
    }

    .bubble-text {
        max-width: 76%;
        font-family: 'Noto Sans SC', sans-serif !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        letter-spacing: 0 !important;
        text-align: center;
        overflow-wrap: anywhere;
    }

    #mood-input {
        font-size: 14px !important;
        letter-spacing: 0 !important;
    }

    #fox-svg {
        filter: drop-shadow(0 4px 7px rgba(123, 67, 49, .13));
    }

    @media (max-width: 860px) {
        .brand-panel {
            width: calc(100% - 44px) !important;
        }

        .brand-panel h1 {
            font-size: clamp(2rem, 8vw, 2.55rem) !important;
            line-height: 1.2 !important;
            letter-spacing: -0.045em !important;
        }

        .brand-panel h1 em {
            white-space: normal;
        }

        .brand-eyebrow {
            letter-spacing: .11em !important;
        }
    }

    @media (max-width: 520px) {
        .brand-panel h1 {
            font-size: 2rem !important;
        }

        #display-name {
            letter-spacing: .03em !important;
        }
    }
</style>
'''

settings_css = '''
<!-- settings-type-refinement -->
<style>
    body,
    button,
    input,
    select,
    textarea {
        font-family: 'Noto Sans SC', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-variant-numeric: tabular-nums;
    }

    body {
        color: #4b403c !important;
    }

    body > .max-w-3xl > header h1,
    .settings-intro h2,
    .settings-intro h2 em {
        font-family: 'Noto Sans SC', sans-serif !important;
        font-style: normal !important;
        font-weight: 700 !important;
        letter-spacing: -0.045em !important;
    }

    .settings-intro h2 {
        line-height: 1.2 !important;
    }

    .settings-intro h2 em {
        display: inline-block;
        color: var(--fox) !important;
    }

    .settings-intro .eyebrow {
        letter-spacing: .14em !important;
        font-weight: 600 !important;
    }

    .settings-intro p {
        color: #75635c !important;
        font-size: 14px !important;
        line-height: 1.85 !important;
        letter-spacing: 0 !important;
    }

    .tab-btn {
        font-weight: 600 !important;
        letter-spacing: .02em !important;
    }

    .tab-panel h2 {
        color: #895f52 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
        letter-spacing: .055em !important;
    }

    .tab-panel h3,
    .tab-panel label,
    .tab-panel p,
    .tab-panel span,
    .tab-panel button {
        letter-spacing: 0 !important;
    }

    .tab-panel label {
        color: #765f56 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }

    .tab-panel p,
    .tab-panel .text-\[10px\] {
        color: #8a756c !important;
        line-height: 1.65 !important;
    }

    .input-fox {
        font-family: 'Noto Sans SC', sans-serif !important;
        font-size: 13px !important;
        line-height: 1.4 !important;
    }

    body > .max-w-3xl > header a {
        white-space: nowrap;
        font-weight: 500;
    }

    @media (max-width: 720px) {
        .settings-intro h2 {
            font-size: 2rem !important;
        }

        .settings-intro p {
            font-size: 13px !important;
        }
    }
</style>
'''

if '<!-- fox-and-type-refinement -->' not in index:
    index = index.replace('</head>', index_css + '\n</head>')
if '<!-- settings-type-refinement -->' not in settings:
    settings = settings.replace('</head>', settings_css + '\n</head>')

index_path.write_text(index, encoding="utf-8")
settings_path.write_text(settings, encoding="utf-8")
