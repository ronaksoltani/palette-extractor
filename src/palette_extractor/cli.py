import argparse
import json
from pathlib import Path

from .palette import extract_palette, render_swatch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract dominant colors from an image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--colors", type=int, default=5)
    parser.add_argument("--output", type=Path, default=Path("palette.png"))
    parser.add_argument("--json", type=Path, default=Path("palette.json"))
    args = parser.parse_args(argv)
    try:
        colors = extract_palette(args.image, args.colors)
        render_swatch(colors, args.output)
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps([color.to_dict() for color in colors], indent=2), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    for color in colors:
        print(f"{color.hex}  {color.share:.1%}")
    print(f"Swatches: {args.output}\nJSON: {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
