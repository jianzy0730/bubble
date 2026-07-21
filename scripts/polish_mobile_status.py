from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'index.html'
text = path.read_text(encoding='utf-8')
marker = '<!-- mobile-status-polish -->'
css = '''
<!-- mobile-status-polish -->
<style>
@media (max-width: 520px) {
    #display-name {
        max-width: none !important;
        overflow: visible !important;
        font-size: 0 !important;
        white-space: nowrap !important;
    }

    #display-name::after {
        content: "ONLINE";
        font-size: 12px;
        font-weight: 600;
        letter-spacing: .09em;
    }
}
</style>
'''
if marker not in text:
    text = text.replace('</head>', css + '\n</head>')
path.write_text(text, encoding='utf-8')
