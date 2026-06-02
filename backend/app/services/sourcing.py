from typing import Optional

import httpx

from app.config import settings


class SourcingService:
    BASE_URL = "https://api.nexar.com/v1/graphql"

    def __init__(self):
        self._token: Optional[str] = None
        self._client_id = settings.octopart_api_key

    async def _get_token(self) -> str:
        if self._token:
            return self._token
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://identity.nexar.com/connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.octopart_api_key,
                    "client_secret": settings.octopart_api_key,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()
            self._token = resp.json()["access_token"]
        return self._token

    async def search_part(self, mpn: str) -> Optional[dict]:
        token = await self._get_token()
        query = """
        query($q: String!) {
          supSearch(query: $q, limit: 1) {
            results {
              part {
                mpn
                manufacturer {
                  name
                }
                category
                description
                lifecycleStatus {
                  name
                }
                datasheetUrls
                sellers {
                  company {
                    name
                  }
                  prices {
                    price
                    quantity
                  }
                  inventoryLevel
                  leadTimeDays
                }
              }
            }
          }
        }
        """
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.BASE_URL,
                json={"query": query, "variables": {"q": mpn}},
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("data", {}).get("supSearch", {}).get("results", [])
            return results[0]["part"] if results else None

    async def enrich_bom_item(self, mpn: str) -> dict:
        part = await self.search_part(mpn)
        if not part:
            return {
                "availability_score": 80,
                "lifecycle_score": 50,
                "supplier_score": 70,
                "lead_time_score": 50,
                "compliance_score": 30,
            }

        sellers = part.get("sellers", [])
        total_stock = sum(s.get("inventoryLevel", 0) or 0 for s in sellers)
        lead_times = [s.get("leadTimeDays") for s in sellers if s.get("leadTimeDays")]

        lifecycle = part.get("lifecycleStatus", {})
        lifecycle_name = lifecycle.get("name", "") if lifecycle else ""

        return {
            "availability_score": 10 if total_stock > 1000 else (50 if total_stock > 100 else 80),
            "lifecycle_score": {"Active": 10, "NRND": 50, "EOL": 80, "Obsolete": 95}.get(lifecycle_name, 30),
            "supplier_score": 10 if len(sellers) > 3 else (50 if len(sellers) > 1 else 80),
            "lead_time_score": 10 if not lead_times else (50 if max(lead_times) > 20 else 20),
            "compliance_score": 30,
        }
