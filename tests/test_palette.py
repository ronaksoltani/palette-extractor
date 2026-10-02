from palette_extractor.palette import extract_palette, render_swatch
from PIL import Image


def test_extracts_requested_palette_from_simple_image(tmp_path):
    path = tmp_path / "two-colors.png"
    image = Image.new("RGB", (20, 10), "red")
    for x in range(10, 20):
        for y in range(10):
            image.putpixel((x, y), (0, 0, 255))
    image.save(path)
    colors = extract_palette(path, colors=2)
    assert {color.hex for color in colors} == {"#FF0000", "#0000FF"}
    assert sum(color.share for color in colors) == 1.0


def test_swatch_is_saved_to_requested_path(tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (4, 4), "navy").save(source)
    colors = extract_palette(source, colors=1)
    output = render_swatch(colors, tmp_path / "nested" / "swatch.png")
    assert output.is_file()
