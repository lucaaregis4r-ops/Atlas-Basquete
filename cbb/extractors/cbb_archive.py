"""
Extractor for CBB Archive official endpoints (cbbarchive.online).
"""
import urllib.request
import json
from pathlib import Path
from typing import Dict, List, Any
import hashlib
from cbb.config import CBB_ARCHIVE_URL, DATA_DIR

class CBBArchiveExtractor:
    def __init__(self, base_url: str = CBB_ARCHIVE_URL, cache_dir: Path = DATA_DIR / "raw" / "cbb_archive"):
        self.base_url = base_url
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Basquete-Atlas/1.0"}

    def _fetch_json(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8")
            # Cache raw response
            cache_name = path.strip("/").replace("/", "_").replace("?", "_").replace("&", "_") + ".json"
            (self.cache_dir / cache_name).write_text(content, encoding="utf-8")
            return json.loads(content)

    def fetch_teams(self) -> List[Dict[str, Any]]:
        try:
            return self._fetch_json("/api/times")
        except Exception as e:
            print(f"Warning: Failed to fetch /api/times: {e}")
            return []

    def fetch_hall_athletes(self) -> List[Dict[str, Any]]:
        try:
            return self._fetch_json("/api/atletas-hall")
        except Exception as e:
            print(f"Warning: Failed to fetch /api/atletas-hall: {e}")
            return []

    def fetch_rankings(self, naipe: str = "masculino", fundamento: str = "pontos", tipo_metrica: str = "media") -> List[Dict[str, Any]]:
        try:
            path = f"/api/rankings-historicos?naipe={naipe}&fundamento={fundamento}&tipo_metrica={tipo_metrica}"
            return self._fetch_json(path)
        except Exception as e:
            print(f"Warning: Failed to fetch rankings {fundamento}: {e}")
            return []
