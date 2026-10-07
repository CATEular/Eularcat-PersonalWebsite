"""Extract rendered image regions or an explicitly selected PDF crop."""
import argparse
import re
from pathlib import Path
import pymupdf
from paths import load_paths

def extract(pdf, output, page_number=None, crop=None, dpi=180):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with pymupdf.open(pdf) as document:
        pages = [page_number - 1] if page_number else range(len(document))
        for index in pages:
            if index < 0 or index >= len(document):
                raise ValueError("Page number is outside the PDF")
            page = document[index]
            regions = [pymupdf.Rect(crop)] if crop else [pymupdf.Rect(info["bbox"]) for info in page.get_image_info()]
            unique = set()
            for rectangle in regions:
                rectangle &= page.rect
                identity = tuple(round(value, 3) for value in rectangle)
                if rectangle.is_empty or identity in unique:
                    continue
                unique.add(identity)
                target = output / f"p{index + 1:03d}-figure{len(unique):02d}.png"
                if target.exists():
                    raise FileExistsError(f"Refusing to overwrite {target.name}")
                page.get_pixmap(matrix=pymupdf.Matrix(dpi / 72, dpi / 72), clip=rectangle, alpha=False).save(target)
                results.append(target)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("--config")
    parser.add_argument("--paper-id", required=True, help="A unique paper folder name")
    parser.add_argument("--output", help="Optional explicit image directory")
    parser.add_argument("--page", type=int, help="One-based page number")
    parser.add_argument("--crop", nargs=4, type=float, metavar=("X0", "Y0", "X1", "Y1"), help="PDF points, requires --page")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()
    if not re.fullmatch(r"[\w-]+", args.paper_id) or args.paper_id in {".", ".."}:
        parser.error("paper-id must contain only letters, digits, underscores or hyphens")
    if args.page is not None and args.page < 1:
        parser.error("page must be positive")
    if args.crop and args.page is None:
        parser.error("crop requires page")
    if not 72 <= args.dpi <= 600:
        parser.error("dpi must be between 72 and 600")
    paths = load_paths(args.config)
    pdf = Path(args.pdf).expanduser()
    if not pdf.is_absolute():
        pdf = paths["papers"] / pdf
    output = Path(args.output).expanduser() if args.output else paths["images"] / args.paper_id
    results = extract(pdf, output, args.page, args.crop, args.dpi)
    print(f"Extracted {len(results)} image regions")
    if not results:
        print("No raster regions found; use --page and --crop for vector figures")
    for result in results:
        print(result)
