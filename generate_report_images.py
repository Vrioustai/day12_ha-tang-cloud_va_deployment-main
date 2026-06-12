from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base = Path(__file__).resolve().parent
texts = [
    ('render-screenshot.png', 'Render Production URL\nhttps://ai-agent-production-cl63.onrender.com\n\nResponse:\n{"app":"Production AI Agent","version":"1.0.0","environment":"production","endpoints":{"ask":"POST /ask (requires X-API-Key)","health":"GET /health","ready":"GET /ready"}}'),
    ('railway-screenshot.png', 'Railway Production URL\nhttps://day12-agent-production-c760.up.railway.app\n\nResponse:\n{"app":"Production AI Agent","version":"1.0.0","environment":"development","endpoints":{"ask":"POST /ask (requires X-API-Key)","health":"GET /health","ready":"GET /ready"}}')
]

for filename, text in texts:
    img = Image.new('RGB', (1280, 720), color=(18, 18, 18))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 26)
    except Exception:
        font = ImageFont.load_default()
    margin = 40
    y = margin
    for line in text.split('\n'):
        draw.text((margin, y), line, font=font, fill=(230, 230, 230))
        y += 38
    img.save(base / filename)
    print(f'Created {filename}')
