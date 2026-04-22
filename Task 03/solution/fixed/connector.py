"""
GitHub Issues connector - fixed version.

Bugs fixed vs. the original code.py:

1. Pagination never ran. `url = self._parse_next_link(...)` and the
   `return records` were both inside the per-item for-loop (return was
   one level up, but still inside the while). Result: only the first
   page was ever fetched, and next-link parsing happened per item.
   Now: next-link is read once per page, after the for-loop finishes,
   and return is after the while-loop terminates.

2. Rate-limit retries did not retry. After sleeping on 429/403 the code
   fell through and hit `resp.raise_for_status()`, which raises on
   4xx - so a rate-limit response was slept-through exactly once and
   then thrown. Added an explicit `continue`.

3. 403 handling was indiscriminate. GitHub uses 403 for BOTH "you hit
   the secondary rate limit" and "your token can't see this resource".
   Retrying the latter forever is wrong. Now we treat 403 as
   rate-limited only when `x-ratelimit-remaining: 0` is present;
   otherwise it's a real permission error and we raise.

4. Sleep and time are injectable, so tests don't actually sleep.

5. `_normalize` tolerated `item["user"] = None` (the original
   `item.get("user", {}).get("login")` crashes when `user` is present
   but None).
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
import time
import requests


@dataclass
class NormalizedRecord:
    source: str
    external_id: str
    type: str
    timestamp: str
    data: Dict[str, Any]


class RateLimitError(Exception):
    """Raised when retries are exhausted on rate-limit responses."""


class GitHubIssuesConnector:
    BASE_URL = "https://api.github.com"
    MAX_RETRIES = 5
    DEFAULT_RATE_LIMIT_WAIT = 60  # seconds, when no headers tell us

    def __init__(
        self,
        token: str,
        session: Optional[requests.Session] = None,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.time,
    ) -> None:
        self.token = token
        self.session = session or requests.Session()
        self._sleep = sleep
        self._now = now

    # ---------- HTTP ----------

    def _request(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }

        for attempt in range(self.MAX_RETRIES):
            resp = self.session.get(
                url, headers=headers, params=params, timeout=10
            )

            if self._is_rate_limited(resp):
                self._sleep(self._rate_limit_wait(resp.headers))
                continue  # <-- the missing continue

            if 500 <= resp.status_code < 600:
                self._sleep(2 ** attempt)
                continue

            resp.raise_for_status()
            return resp

        raise RateLimitError(
            f"Request failed after {self.MAX_RETRIES} retries: {url}"
        )

    @staticmethod
    def _is_rate_limited(resp: requests.Response) -> bool:
        if resp.status_code == 429:
            return True
        if resp.status_code == 403:
            # Distinguish rate-limit 403 from permission 403.
            return resp.headers.get("x-ratelimit-remaining") == "0"
        return False

    def _rate_limit_wait(self, headers: Any) -> int:
        retry_after = headers.get("Retry-After")
        if retry_after is not None:
            try:
                return max(1, int(retry_after))
            except (TypeError, ValueError):
                pass
        reset_at = headers.get("x-ratelimit-reset")
        if reset_at is not None:
            try:
                return max(1, int(reset_at) - int(self._now()))
            except (TypeError, ValueError):
                pass
        return self.DEFAULT_RATE_LIMIT_WAIT

    # ---------- Pagination ----------

    @staticmethod
    def _parse_next_link(link_header: Optional[str]) -> Optional[str]:
        if not link_header:
            return None
        for part in (p.strip() for p in link_header.split(",")):
            if 'rel="next"' in part:
                start = part.find("<") + 1
                end = part.find(">")
                if start > 0 and end > start:
                    return part[start:end]
        return None

    # ---------- Normalization ----------

    @staticmethod
    def _normalize(item: Dict[str, Any]) -> NormalizedRecord:
        user = item.get("user") or {}
        author = user.get("login") if isinstance(user, dict) else None
        return NormalizedRecord(
            source="github",
            external_id=str(item["number"]),
            type="issue",
            timestamp=item["created_at"],
            data={
                "number": item["number"],
                "title": item["title"],
                "state": item["state"],
                "body": item.get("body"),
                "comments": item.get("comments", 0),
                "author_login": author,
            },
        )

    # ---------- Public API ----------

    def list_issues(
        self, owner: str, repo: str, state: str = "open"
    ) -> List[NormalizedRecord]:
        url: Optional[str] = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        params: Optional[Dict[str, Any]] = {"state": state, "per_page": 100}
        records: List[NormalizedRecord] = []

        while url:
            resp = self._request(url, params=params)
            for item in resp.json():
                if "pull_request" in item:       # filter PRs
                    continue
                records.append(self._normalize(item))
            url = self._parse_next_link(resp.headers.get("Link"))
            params = None                        # only on first page

        return records
