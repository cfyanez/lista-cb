# AI Agent Instructions for lista-cb

This project is a web-based product listing application that displays CENABAST (Central Nacional de Abastecimiento) products with their alternatives. It consists of a Python data processing script and a single-page web application.

## Project Structure

- `csv_a_products_json_autodelim_v2.py`: Python script that converts CSV product data to JSON
- `index.html`: Single-page web application with search functionality
- `productos.csv`: Source data file containing product information
- `products.json`: Generated JSON file used by the web interface
- `img/`: Directory containing images and assets

## Core Components

### Data Processing Script

The Python script (`csv_a_products_json_autodelim_v2.py`) handles:
- CSV to JSON conversion with automatic delimiter detection (`,` or `;`)
- Product data normalization and validation
- Special handling for:
  - Alternative products (via `is_alt` and `alts` columns)
  - CENABAST equivalents (via `alt_cb` column)
  - Stock status conversion to boolean
  - Price cleaning and integer conversion

Usage:
```bash
python3 csv_a_products_json_autodelim_v2.py productos.csv products.json
```

### Web Interface

The web application (`index.html`) features:
- Responsive design with mobile-first approach
- Client-side search with autocompletion
- Product listing with detailed information display
- Sorting and filtering capabilities

Key data structure fields:
```json
{
  "id": "string",
  "name": "string",
  "price": number,
  "brand": "string",
  "actives": ["string"],
  "form": "string",
  "strength": "string",
  "pack_size": number,
  "aliases": ["string"],
  "lab": "string",
  "stock": "string"
}
```

## Development Patterns

1. **Data Processing**:
   - Always validate and clean input data using utility functions (`to_array`, `to_int`, `stock_bool`)
   - Handle missing values with sensible defaults
   - Preserve UTF-8 encoding for Spanish text

2. **Front-end Development**:
   - Use CSS custom properties for consistent styling (`--gap`, `--radius`, `--shadow`)
   - Follow mobile-first responsive design patterns
   - Maintain semantic HTML structure for accessibility

## Integration Points

- The Python script outputs `products.json` which is consumed by the web interface
- The web interface loads product data via client-side JSON fetching
- Browser local storage is used for persisting user preferences

Please reference existing files when making changes to maintain consistency in data processing and presentation patterns.