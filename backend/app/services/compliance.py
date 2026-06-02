import csv
from pathlib import Path
from typing import Optional

from rapidfuzz import fuzz


class ComplianceScreener:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.entity_list: list[dict] = []
        self._load_entity_list()

    def _load_entity_list(self):
        path = self.data_dir / "consolidated_screening_list.csv"
        if path.exists():
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.entity_list = list(reader)

    def screen_name(self, name: str, threshold: int = 80) -> list[dict]:
        results = []
        for entity in self.entity_list:
            match = fuzz.token_sort_ratio(name.lower(), entity.get("name", "").lower())
            if match >= threshold:
                results.append({
                    "entity_name": entity["name"],
                    "match_score": match,
                    "list_source": entity.get("list_source", ""),
                    "country": entity.get("country", ""),
                    "restriction_type": entity.get("restriction_type", ""),
                })
        return sorted(results, key=lambda r: r["match_score"], reverse=True)

    def screen_bom_suppliers(self, bom_items: list[dict]) -> list[dict]:
        results = []
        seen = set()
        for item in bom_items:
            name = item.get("manufacturer") or item.get("raw_part_number", "")
            if not name or name in seen:
                continue
            seen.add(name)
            matches = self.screen_name(name)
            results.extend(matches)
        return results
