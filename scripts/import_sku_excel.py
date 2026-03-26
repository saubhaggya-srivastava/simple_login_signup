import math
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import IntegrityError

from db.database import SessionLocal
from mappings.sku_column_map import EXCEL_TO_DB_MAP
from models.sku import SKU

SHEET_NAME = "SKU Master"
HEADER_ROW_INDEX = 1


NUMERIC_INT_FIELDS = {"shelf_life_days", "outer_per_case", "units_per_outer"}
NUMERIC_FLOAT_FIELDS = {
    "case_length_cm", "case_width_cm", "case_height_cm", "case_cbm",
    "outer_length_cm", "outer_width_cm", "outer_height_cm", "outer_cbm",
    "unit_length_cm", "unit_width_cm", "unit_height_cm", "unit_cbm",
    "unit_weight_gm", "case_weight_kg",
    "case_cost", "case_price", "outer_price", "unit_price", "unit_rsp",
}


def to_none_if_empty(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def normalize_value(field, value):
    value = to_none_if_empty(value)
    if value is None:
        return None

    if field in NUMERIC_INT_FIELDS:
        return int(float(value))
    if field in NUMERIC_FLOAT_FIELDS:
        return float(value)

    return str(value).strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_sku_excel.py <excel_file_path>")
        sys.exit(1)

    excel_path = Path(sys.argv[1])
    if not excel_path.exists():
        print(f"File not found: {excel_path}")
        sys.exit(1)

    df = pd.read_excel(
        excel_path,
        sheet_name=SHEET_NAME,
        engine="pyxlsb",
        header=HEADER_ROW_INDEX,
    )
    df.columns = [str(col).strip() for col in df.columns]

    available_cols = [col for col in df.columns if col in EXCEL_TO_DB_MAP]
    df = df[available_cols].rename(columns=EXCEL_TO_DB_MAP)

    if "sku_code" not in df.columns:
        print("ERROR: 'SKU Code' column is required.")
        sys.exit(1)

    inserted = 0
    skipped = 0
    failed = 0

    db = SessionLocal()
    try:
        for idx, row in df.iterrows():
            excel_row_number = idx + HEADER_ROW_INDEX + 2
            row_dict = {k: normalize_value(k, v) for k, v in row.to_dict().items()}

            if not row_dict.get("sku_code"):
                skipped += 1
                print(f"Row {excel_row_number}: skipped (missing SKU Code)")
                continue

            existing = db.query(SKU).filter(SKU.sku_code == row_dict["sku_code"]).first()
            if existing:
                skipped += 1
                print(
                    f"Row {excel_row_number}: skipped "
                    f"(duplicate sku_code={row_dict['sku_code']})"
                )
                continue

            try:
                sku = SKU(**row_dict)
                db.add(sku)
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()
                skipped += 1
                print(f"Row {excel_row_number}: skipped (integrity error)")
            except Exception as e:
                db.rollback()
                failed += 1
                print(f"Row {excel_row_number}: failed ({e})")
    finally:
        db.close()

    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()