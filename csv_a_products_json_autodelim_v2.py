#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
csv_a_products_json_v3.py
Convierte un CSV a JSON, manejando nuevas columnas para alternativas.
- alts: Alternativas fuera de convenio (separadas por ';')
- is_alt: '1' si el producto es una alternativa oculta, '0' si no.
- alt_cb: Equivalentes dentro del convenio Cenabast (separados por ';')

Uso:
    python3 csv_a_products_json_v3.py productos.csv products.json
"""

import sys, csv, json, re, io

def to_array(s):
    """Convierte un string separado por ; en un arreglo de strings."""
    if s is None:
        return []
    s = str(s).strip()
    if not s:
        return []
    return [x.strip() for x in s.split(';') if x.strip()]

def to_int(s):
    """Limpia un string y lo convierte a entero."""
    if s is None:
        return None
    s = re.sub(r"[^\d]", "", str(s))
    return int(s) if s else None

def sniff_delimiter(sample):
    """Auto-detecta el delimitador del CSV (',' o ';')."""
    first_line = sample.splitlines()[0] if sample else ""
    if first_line.lower().startswith("sep=") and len(first_line) >= 5:
        sep = first_line[4]
        if sep in (',',';'):
            return sep, True
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample, delimiters=[',',';'])
        return dialect.delimiter, False
    except csv.Error:
        return ',', False

def stock_bool(s):
    """Convierte un texto de stock a booleano (true/false)."""
    if s is None:
        return None
    t = str(s).strip().lower()
    if t in ('1','true','verdadero','sí','si','con stock','con','disponible','hay'):
        return True
    if t in ('0','false','falso','no','sin stock','sin','agotado'):
        return False
    return None

def is_alt_bool(s):
    """Convierte la columna 'is_alt' (1/0) a booleano (true/false)."""
    if s is None:
        # Por defecto, un producto no es una alternativa.
        return False
    # Si el valor es '1', es una alternativa. Cualquier otra cosa es 'false'.
    return str(s).strip() == '1'

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 csv_a_products_json_v3.py productos.csv products.json")
        sys.exit(1)
    csv_path, json_path = sys.argv[1], sys.argv[2]

    try:
        with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de entrada: {csv_path}")
        sys.exit(1)

    delimiter, skip_first = sniff_delimiter(raw)
    if skip_first:
        raw = "\n".join(raw.splitlines()[1:])

    reader = csv.DictReader(io.StringIO(raw), delimiter=delimiter)
    rows = []
    for row in reader:
        # Ignora filas si no tienen un nombre de producto
        if not (row.get("name") or "").strip():
            continue

        item = {
            "id": (row.get("id") or "").strip(),
            "name": (row.get("name") or "").strip(),
            "price": to_int(row.get("price")) or 0,
            "brand": (row.get("brand") or "").strip() or None,
            "actives": to_array(row.get("actives")),
            "form": (row.get("form") or "").strip() or None,
            "strength": (row.get("strength") or "").strip() or None,
            "pack_size": to_int(row.get("pack_size")),
            "aliases": to_array(row.get("aliases")),
            "lab": (row.get("lab") or "").strip() or None,
            "stock": (row.get("stock") or "").strip() or None,
            "in_stock": stock_bool(row.get("stock")),
            # --- NUEVOS CAMPOS AÑADIDOS ---
            "alternatives": to_array(row.get("alts")),
            "is_alternative": is_alt_bool(row.get("is_alt")),
            "cenabast_equivalents": to_array(row.get("alt_cb")),
        }
        rows.append(item)

    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(rows, out, ensure_ascii=False, indent=2)

    print(f"OK: {len(rows)} productos procesados → {json_path} (delimitador: '{delimiter}')")
    print("Se incluyeron los campos: alternatives, is_alternative, cenabast_equivalents.")

if __name__ == "__main__":
    main()