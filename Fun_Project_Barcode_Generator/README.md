# Barcode Generator

## Description

A Python application that generates **EAN-13, Code-128, and other standard barcodes** for products. The program offers two modes: **Interactive Mode** (manual entry) and **Batch Mode** (CSV import). Users can input product information (product ID, name, price) and the system produces ready-to-print PNG barcode images for retail labeling, inventory management, or product identification.

---

## Dataset

- **Source**: User input (Interactive) / CSV file (Batch)
- **Description of data**: 
  - **product_id**: 12-digit EAN prefix for EAN-13 format (or other format-specific IDs)
  - **name**: Product name (used in filename)
  - **price**: Product price in ₹ (for display/logging)

### Sample Data (products.csv)

| product_id    | name             | price |
|---------------|------------------|-------|
| 890123456789  | Green Tea 250g   | 120.00 |
| 890234567890  | Dark Chocolate   | 85.50  |
| 890345678901  | Almonds 500g     | 349.00 |
| 890456789012  | Mineral Water 1L | 20.00  |
| 890567890123  | Oats 1kg         | 175.00 |

---

## Steps Performed

1. **Mode Selection**
   - User chooses between Interactive Mode (manual entry) or Batch Mode (CSV import)

2. **Format Selection**
   - User selects barcode format (EAN-13, Code-128, UPC-A, etc.)
   - System displays format requirements (digit length, character types)

3. **Data Input**
   - **Interactive**: User enters products one by one with validation
   - **Batch**: System loads products from CSV file using `csv.DictReader`

4. **Barcode Generation**
   - `barcode.get_barcode_class()` fetches the appropriate encoder
   - Creates barcode instance with `ImageWriter()` for PNG output
   - Each barcode is rendered and saved to `barcodes/` directory

5. **Validation & Error Handling**
   - Product IDs validated against format requirements
   - Invalid entries rejected with clear error messages
   - Success/failure count displayed after processing

---

## Results

- **Key findings**:
  - Successfully generated barcodes for all valid products
  - PNG images created with machine-readable barcode pattern
  - Human-readable product ID displayed below barcode
  - All images saved in `barcodes/` folder with product ID in filename

- **Metrics** (Sample Run):
  - Products processed: 5
  - Successfully generated: 5
  - Failed: 0
  - Success rate: 100%
  - Barcode format: EAN-13
  - Output format: PNG (300 DPI, ~4-6 KB per file)

---

## Tools Used

- **Python 3.x**
- **python-barcode** - Barcode generation library (EAN, Code-128, UPC, etc.)
- **Pillow (PIL)** - Image rendering backend for ImageWriter
- **csv** (built-in) - CSV file parsing
- **os** (built-in) - Directory and path management

---

## Conclusion

This Barcode Generator project demonstrates practical automation of barcode creation for retail and inventory management. The dual-mode approach (interactive + batch) makes it flexible for different use cases - from generating a few barcodes manually to processing large product catalogs from CSV files.

**Key takeaways**:
- **Flexibility**: Supports multiple barcode standards (EAN-13, Code-128, UPC-A, Code-39)
- **Validation**: Format-specific validation prevents errors
- **Scalability**: Batch mode handles large product lists efficiently
- **Production-ready**: Clean error handling and user-friendly output
- **Extensibility**: Easy to add new barcode formats or data sources

**Real-world applications**:
- Retail product labeling
- Inventory management systems
- Warehouse tracking
- E-commerce product catalogs
- Library book management

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install python-barcode[images]
```

### 2. Run the Program

```bash
python barcode_generator.py
```

### 3. Choose Mode

**Option 1: Interactive Mode**
```
Select [1 or 2] (default = 1): 1

Choose barcode format → Enter products manually → Generate
```

**Option 2: Batch Mode**
```
Select [1 or 2] (default = 1): 2

Loads from products.csv → Choose format → Generate all
```

---

## Sample Output

```
=======================================================
      BARCODE GENERATOR — Abhijeet Kaushik
=======================================================

Choose mode:
  1. Interactive Mode (enter products manually)
  2. Batch Mode (load from products.csv)

Select [1 or 2] (default = 1): 2

✔  Loaded 5 products from products.csv

Supported barcode formats:
  1. ean13      (12 digits (check digit auto-added))
  2. ean8       (7 digits (check digit auto-added))
  3. code128    (any alphanumeric string)
  4. upca       (11 digits (check digit auto-added))
  5. code39     (alphanumeric, max 43 chars)

Choose format [1-5] (default = 1 → ean13): 1

Generating EAN-13 barcodes for 5 products…

✔  Green Tea 250g          │  ₹120.00 → barcodes/890123456789_Green_Tea_250g.png
✔  Dark Chocolate          │   ₹85.50 → barcodes/890234567890_Dark_Chocolate.png
✔  Almonds 500g            │  ₹349.00 → barcodes/890345678901_Almonds_500g.png
✔  Mineral Water 1L        │   ₹20.00 → barcodes/890456789012_Mineral_Water_1L.png
✔  Oats 1kg                │  ₹175.00 → barcodes/890567890123_Oats_1kg.png

───────────────────────────────────────────────────────
  Generated : 5   Failed : 0
  Output    : /your/path/barcodes/
=======================================================
```

---

## File Structure

```
barcode-generator/
│
├── barcode_generator.py    # Main script
├── products.csv            # Sample product data (for batch mode)
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── barcodes/               # Generated barcode images (auto-created)
    ├── 890123456789_Green_Tea_250g.png
    ├── 890234567890_Dark_Chocolate.png
    └── ...
```

---

## Author

Abhijeet Kaushik
