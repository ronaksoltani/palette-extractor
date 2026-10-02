from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans


@dataclass(frozen=True)
class Color:
    hex: str
    rgb: tuple[int, int, int]
    share: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_palette(path: Path, colors: int = 5, sample_size: int = 120) -> list[Color]:
    if not 1 <= colors <= 12:
        raise ValueError("colors must be between 1 and 12")
    image = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    image = Image.alpha_composite(background, image).convert("RGB")
    image.thumbnail((sample_size, sample_size))
    pixels = np.asarray(image, dtype=np.uint8).reshape(-1, 3)
    unique = len(np.unique(pixels, axis=0))
    count = min(colors, unique)
    model = KMeans(n_clusters=count, random_state=7, n_init=10)
    labels = model.fit_predict(pixels)
    amounts = np.bincount(labels, minlength=count)
    output = []
    for center, amount in zip(model.cluster_centers_, amounts):
        rgb = tuple(int(round(value)) for value in center)
        output.append(Color("#%02X%02X%02X" % rgb, rgb, round(float(amount / len(labels)), 4)))
    return sorted(output, key=lambda color: (-color.share, color.hex))


def render_swatch(colors: list[Color], output: Path, width: int = 1000, height: int = 260) -> Path:
    if not colors:
        raise ValueError("palette cannot be empty")
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    block_width = width / len(colors)
    for index, color in enumerate(colors):
        left, right = round(index * block_width), round((index + 1) * block_width)
        draw.rectangle((left, 0, right, height - 60), fill=color.hex)
        draw.text((left + 12, height - 46), f"{color.hex} · {color.share:.1%}", fill="#202020", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG")
    return output
