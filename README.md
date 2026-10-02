# Palette Extractor

Extract a compact palette from an image with deterministic K-Means clustering. The CLI writes both a JSON color report and a PNG swatch image with HEX values and pixel shares.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
palette-extract screenshot.png --colors 5 --output build/palette.png --json build/palette.json
```

The source image is resized before sampling to keep memory and runtime predictable. Percentages are approximate because colors are clustered. Transparent pixels are composited onto white before analysis.

## Learning notes

This project practices image loading, bounded sampling, K-Means clustering, deterministic random seeds, and converting RGB triplets to CSS HEX strings.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
