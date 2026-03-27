import math
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import IntegrityError

from db.database import SessionLocal
from mappings.msl_list_column_map import EXCEL_TO_DB_MAP
from models.msl_list import MSLList

SHEET_NAME = "MSL List"
HEADER_ROW_INDEX = 0

NUMERIC_INT_FIELDS = {
    "warehouse",
    "hyper_a",
    "hyper_b",
    "super_a",
    "super_b",
    "minimart_a",
    "minimart_b",
    "grocery_a",
    "grocery_b",
    "grocery_c",
    "ecom_a",
    "ecom_b",
    "petrol_pumps_a",
    "petrol_pumps_b",
    "petrol_pumps_c",
    "pharmacy_a",
    "pharmacy_b",
    "pharmacy_c",
    "wholesale",
    "horeca",
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

    return str(value).strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_msl_list_excel.py <excel_file_path>")
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

            try:
                msl_item = MSLList(**row_dict)
                db.add(msl_item)
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

    print(f"\nInserted: {inserted}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
