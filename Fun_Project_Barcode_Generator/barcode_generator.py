# ============================================================
#  Barcode Generator — Interactive + Batch Mode
#  Author : Abhijeet Kaushik
#  Description: Generate barcodes interactively or from CSV
# ============================================================

import barcode
from barcode.writer import ImageWriter
import os
import csv

# ── Configuration ───────────────────────────────────────────
OUTPUT_DIR = "barcodes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_FORMATS = ["ean13", "ean8", "code128", "upca", "code39"]

FORMAT_RULES = {
    "ean13":   ("12 digits (check digit auto-added)", lambda x: x.isdigit() and len(x) == 12),
    "ean8":    ("7 digits (check digit auto-added)",  lambda x: x.isdigit() and len(x) == 7),
    "upca":    ("11 digits (check digit auto-added)", lambda x: x.isdigit() and len(x) == 11),
    "code128": ("any alphanumeric string",            lambda x: len(x) > 0),
    "code39":  ("alphanumeric, max 43 chars",         lambda x: 0 < len(x) <= 43),
}


# ── Core generator ──────────────────────────────────────────
def generate_barcode(product_id: str, name: str, barcode_format: str = "ean13") -> str:
    """Generate and save a barcode PNG. Returns the saved file path."""
    BarcodeClass = barcode.get_barcode_class(barcode_format)
    bc = BarcodeClass(product_id, writer=ImageWriter())
    filepath = os.path.join(OUTPUT_DIR, f"{product_id}_{name.replace(' ', '_')}")
    return bc.save(filepath)


# ── Batch Mode (CSV) ────────────────────────────────────────
def load_from_csv(filename: str = "products.csv") -> list:
    """Load products from a CSV file."""
    products = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append({
                    'product_id': row['product_id'],
                    'name': row['name'],
                    'price': float(row['price'])
                })
        print(f"  ✔  Loaded {len(products)} products from {filename}")
        return products
    except FileNotFoundError:
        print(f"  ✘  File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"  ✘  Error reading CSV: {e}")
        return []


def process_batch(products: list, barcode_format: str = "ean13"):
    """Process a list of products and generate barcodes."""
    if not products:
        print("\n  No products to process.")
        return
    
    print(f"\n  Generating {barcode_format.upper()} barcodes for {len(products)} product(s)…\n")
    success, failed = 0, 0

    for p in products:
        try:
            path = generate_barcode(p['product_id'], p['name'], barcode_format)
            print(f"  ✔  {p['name']:25s} │ ₹{p['price']:>8.2f} │ → {path}")
            success += 1
        except Exception as e:
            print(f"  ✘  {p['name']:25s} │ Error: {e}")
            failed += 1

    print(f"\n{'─'*55}")
    print(f"  Generated : {success}   Failed : {failed}")
    print(f"  Output    : {os.path.abspath(OUTPUT_DIR)}/")


# ── Interactive Mode ────────────────────────────────────────
def get_barcode_format() -> str:
    """Let the user pick a barcode format from the supported list."""
    print("\n  Supported barcode formats:")
    for i, fmt in enumerate(SUPPORTED_FORMATS, 1):
        hint, _ = FORMAT_RULES[fmt]
        print(f"    {i}. {fmt:10s}  ({hint})")

    while True:
        choice = input(f"\n  Choose format [1-{len(SUPPORTED_FORMATS)}] (default = 1 → ean13): ").strip()
        if choice == "":
            return SUPPORTED_FORMATS[0]
        if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_FORMATS):
            return SUPPORTED_FORMATS[int(choice) - 1]
        print("  ✘  Invalid choice. Enter a number from the list.")


def get_valid_price() -> float:
    """Prompt until a valid float price is entered."""
    while True:
        raw = input("  Price (e.g. 99.99)  : ").strip()
        try:
            return float(raw)
        except ValueError:
            print("  ✘  Please enter a valid number (e.g. 49.99).\n")


def collect_products(barcode_format: str) -> list:
    """Interactively collect product entries from the user."""
    hint, validator = FORMAT_RULES.get(barcode_format, ("any string", lambda x: len(x) > 0))
    products = []
    index = 1

    print(f"\n  Enter product details below.")
    print(f"  (Press Enter on 'Product ID' with no input to finish)\n")

    while True:
        print(f"  ── Product #{index} ──────────────────────────────")

        pid = input(f"  Product ID [{hint}]: ").strip()
        if pid == "":
            break

        if not validator(pid):
            print(f"  ✘  Invalid ID for {barcode_format}. Required: {hint}. Try again.\n")
            continue

        name = input("  Product Name        : ").strip() or f"Product_{pid}"
        price = get_valid_price()

        products.append({"product_id": pid, "name": name, "price": price})
        print(f"  ✔  Added → {name} | ₹{price:.2f}\n")
        index += 1

    return products


# ── Main Menu ───────────────────────────────────────────────
def main():
    print("=" * 55)
    print("      BARCODE GENERATOR — Abhijeet Kaushik")
    print("=" * 55)
    print("\n  Choose mode:")
    print("    1. Interactive Mode (enter products manually)")
    print("    2. Batch Mode (load from products.csv)")
    
    mode = input("\n  Select [1 or 2] (default = 1): ").strip()
    
    if mode == "2":
        # Batch mode
        products = load_from_csv("products.csv")
        if products:
            fmt = get_barcode_format()
            process_batch(products, fmt)
        else:
            print("\n  Switching to interactive mode...\n")
            mode = "1"
    
    if mode != "2":
        # Interactive mode
        fmt = get_barcode_format()
        products = collect_products(fmt)
        
        if not products:
            print("\n  No products entered. Exiting.")
            return
        
        process_batch(products, fmt)

    print("=" * 55)


if __name__ == "__main__":
    main()
