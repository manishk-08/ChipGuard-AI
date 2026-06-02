import io
from typing import Any

import pandas as pd


class BOMParser:
    COLUMN_ALIASES = {
        "part number": "mpn",
        "part_number": "mpn",
        "mpn": "mpn",
        "manufacturer part number": "mpn",
        "manufacturer": "manufacturer",
        "mfr": "manufacturer",
        "qty": "quantity",
        "quantity": "quantity",
        "qty.": "quantity",
        "description": "description",
        "desc": "description",
        "designator": "designator",
        "ref des": "designator",
        "reference": "designator",
        "footprint": "footprint",
        "package": "footprint",
    }

    def parse(self, content: bytes, filename: str) -> list[dict[str, Any]]:
        if filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(content), dtype=str)
        else:
            df = pd.read_csv(io.BytesIO(content), dtype=str, on_bad_lines="skip")

        df.columns = [col.strip().lower() for col in df.columns]
        df.rename(columns=self.COLUMN_ALIASES, inplace=True)

        if "mpn" not in df.columns:
            raise ValueError("Could not find a part number column in the BOM")

        rows = df.to_dict(orient="records")
        return [
            {
                "raw_part_number": str(r.get("mpn", "")).strip(),
                "manufacturer": str(r.get("manufacturer", "")).strip() if pd.notna(r.get("manufacturer")) else None,
                "quantity": int(r["quantity"]) if pd.notna(r.get("quantity")) else None,
                "description": str(r.get("description", "")).strip() if pd.notna(r.get("description")) else None,
                "designator": str(r.get("designator", "")).strip() if pd.notna(r.get("designator")) else None,
                "footprint": str(r.get("footprint", "")).strip() if pd.notna(r.get("footprint")) else None,
            }
            for r in rows
            if str(r.get("mpn", "")).strip()
        ]
