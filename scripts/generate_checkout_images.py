from pathlib import Path

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CANVAS_SIZE = 1600


APPS = [
    {
        "slug": "echotext",
        "source": ROOT / "echotext" / "2026-04-04 20_45_38-EchoText.jpg",
        "output": ROOT / "echotext" / "checkout-square.png",
        "title": "EchoText",
        "subtitle": "Word-level transcripts, sentence clips, and stills. Offline.",
        "pill": "Windows App  •  Whisper Powered",
        "accent": "#69DAFF",
        "accent_2": "#E6A7FF",
    },
    {
        "slug": "markdownforge",
        "source": ROOT / "markdownforge" / "screenshot.jpg",
        "output": ROOT / "markdownforge" / "checkout-square.png",
        "title": "MarkdownForge",
        "subtitle": "Convert docs, URLs, and PDFs into clean Markdown.",
        "pill": "Windows App  •  Offline Conversion",
        "accent": "#FFB938",
        "accent_2": "#69DAFF",
    },
    {
        "slug": "picframes",
        "source": ROOT / "picframes" / "screenshot.jpg",
        "output": ROOT / "picframes" / "checkout-square.png",
        "title": "PicFrames",
        "subtitle": "Frame, mask, and remove backgrounds in one pass.",
        "pill": "Windows App  •  AI Runs Offline",
        "accent": "#69DAFF",
        "accent_2": "#FF8AAE",
    },
    {
        "slug": "bulkwebp",
        "source": ROOT / "bulkwebp" / "screenshot.png",
        "output": ROOT / "bulkwebp" / "checkout-square.png",
        "title": "Bulk WebP",
        "subtitle": "Batch convert folders of images to WebP in seconds.",
        "pill": "Windows App  •  Fully Offline",
        "accent": "#69DAFF",
        "accent_2": "#5BF2B5",
    },
]


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if mono:
        candidates = ["consolab.ttf", "consola.ttf"]
    elif bold:
        candidates = ["segoeuib.ttf", "arialbd.ttf", "bahnschrift.ttf"]
    else:
        candidates = ["segoeui.ttf", "arial.ttf", "bahnschrift.ttf"]

    font_dir = Path("C:/Windows/Fonts")
    for name in candidates:
        path = font_dir / name
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


def hex_rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    return (*ImageColor.getrgb(color), alpha)


def make_vertical_gradient(size: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGBA", (size, size), top)
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    pixels = []
    for y in range(size):
        ratio = y / max(size - 1, 1)
        pixels.append(
            (
                int(top_rgb[0] * (1 - ratio) + bottom_rgb[0] * ratio),
                int(top_rgb[1] * (1 - ratio) + bottom_rgb[1] * ratio),
                int(top_rgb[2] * (1 - ratio) + bottom_rgb[2] * ratio),
                255,
            )
        )
    line = Image.new("RGBA", (1, size))
    line.putdata(pixels)
    return line.resize((size, size))


def add_grid(image: Image.Image, spacing: int = 56) -> None:
    draw = ImageDraw.Draw(image)
    for x in range(0, image.width, spacing):
        draw.line((x, 0, x, image.height), fill=(255, 255, 255, 14), width=1)
    for y in range(0, image.height, spacing):
        draw.line((0, y, image.width, y), fill=(255, 255, 255, 14), width=1)


def add_orb(image: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=hex_rgba(color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=120))
    image.alpha_composite(layer)


def fit_screenshot(source_path: Path, max_size: tuple[int, int]) -> Image.Image:
    screenshot = Image.open(source_path).convert("RGBA")
    screenshot.thumbnail(max_size, Image.Resampling.LANCZOS)
    return screenshot


def add_card_shadow(base: Image.Image, rect: tuple[int, int, int, int], radius: int = 36) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.rounded_rectangle(rect, radius=radius, fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=55))
    base.alpha_composite(shadow)


def draw_centered_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill, anchor: str = "mm") -> None:
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)


def create_checkout_image(config: dict) -> None:
    canvas = make_vertical_gradient(CANVAS_SIZE, "#090B10", "#05060A")
    add_grid(canvas)
    add_orb(canvas, (240, 320), 320, config["accent"], 70)
    add_orb(canvas, (1220, 1240), 340, config["accent_2"], 55)
    add_orb(canvas, (560, 1080), 260, config["accent"], 40)

    draw = ImageDraw.Draw(canvas)
    title_font = load_font(112, bold=True)
    subtitle_font = load_font(42)
    pill_font = load_font(24, bold=True)
    mono_font = load_font(22, mono=True)

    pill_box = (110, 92, 510, 150)
    draw.rounded_rectangle(pill_box, radius=28, fill=(255, 255, 255, 18), outline=hex_rgba(config["accent"], 80), width=2)
    draw.text((pill_box[0] + 26, pill_box[1] + 30), config["pill"], font=pill_font, fill=hex_rgba(config["accent"], 255))

    draw.text((108, 250), config["title"], font=title_font, fill=(250, 250, 252, 255))
    draw.text((110, 372), config["subtitle"], font=subtitle_font, fill=(178, 184, 194, 255))

    stat_box = (110, 452, 350, 520)
    draw.rounded_rectangle(stat_box, radius=24, fill=(255, 255, 255, 14), outline=(255, 255, 255, 18), width=1)
    draw.text((138, 475), "OFFLINE  •  ONE-TIME  •  WINDOWS", font=mono_font, fill=(145, 153, 168, 255))

    card_rect = (108, 580, 1492, 1410)
    add_card_shadow(canvas, card_rect)
    draw.rounded_rectangle(card_rect, radius=42, fill=(19, 19, 19, 235), outline=hex_rgba(config["accent"], 64), width=2)

    header_rect = (108, 580, 1492, 646)
    draw.rounded_rectangle(header_rect, radius=42, fill=(28, 30, 36, 255))
    draw.rectangle((108, 624, 1492, 646), fill=(28, 30, 36, 255))
    for idx, color in enumerate([(112, 115, 123, 255), (112, 115, 123, 255), ImageColor.getrgb(config["accent"]) + (255,)]):
        x = 150 + idx * 26
        draw.ellipse((x, 602, x + 12, 614), fill=color)
    draw.text((1370, 605), config["slug"].upper(), font=mono_font, fill=(124, 132, 148, 255), anchor="ra")

    screenshot = fit_screenshot(config["source"], (1280, 720))
    shot_x = (CANVAS_SIZE - screenshot.width) // 2
    shot_y = 676
    canvas.alpha_composite(screenshot, (shot_x, shot_y))

    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle((1000, 1120, 1440, 1300), radius=28, fill=hex_rgba(config["accent"], 46))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=35))
    canvas.alpha_composite(glow)

    note_box = (1010, 1130, 1450, 1298)
    draw.rounded_rectangle(note_box, radius=28, fill=(20, 22, 27, 235), outline=(255, 255, 255, 20), width=1)
    draw.text((1040, 1164), config["title"].upper(), font=mono_font, fill=hex_rgba(config["accent"], 220))
    draw.text((1040, 1206), "Built for focused offline workflows.", font=load_font(28), fill=(236, 238, 242, 255))
    draw.text((1040, 1248), "Clean UI. Real desktop utility. No fluff.", font=load_font(24), fill=(145, 153, 168, 255))

    config["output"].parent.mkdir(parents=True, exist_ok=True)
    canvas.save(config["output"], format="PNG", optimize=True)


def main() -> None:
    for app in APPS:
        create_checkout_image(app)
        print(f"Wrote {app['output'].relative_to(ROOT)}")


if __name__ == "__main__":
    main()