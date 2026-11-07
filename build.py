"""Builds the installable app (index.html + sw.js) from game.html.

game.html is the whole game. It is also what gets published as the Claude artifact,
so it has no <html>/<head> of its own; this script wraps it for GitHub Pages.
Run:  python build.py
"""
import io
import time

VERSION = str(int(time.time() * 1000))

src = io.open("game.html", encoding="utf-8").read()
cut = src.index("</style>") + len("</style>")
head_part, body_part = src[:cut], src[cut:]

page = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#14213a">
<meta name="description" content="קארום לטלפון: ממקמים את הסטרייקר ומעיפים אותו באצבע. נגד המחשב, על טלפון אחד או אונליין עם חברים.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
html{{box-sizing:border-box;height:100%;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font-size:14px}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
<script>window.CARROM_VERSION = "{VERSION}";</script>
{head_part}
</head>
<body>
{body_part}
</body>
</html>
"""
io.open("index.html", "w", encoding="utf-8", newline="\n").write(page)

sw = io.open("sw.template.js", encoding="utf-8").read().replace("__VERSION__", VERSION)
io.open("sw.js", "w", encoding="utf-8", newline="\n").write(sw)
print("built version", VERSION)
