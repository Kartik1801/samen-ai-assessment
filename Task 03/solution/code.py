from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time
import requests


""" 
Implement a connector that:

- Authenticates with GitHub using a bearer token.
- Fetches issues from a repository.
- Follows pagination using the Link header until there are no more pages.
- Retries on transient 5xx errors.
- Handles 429 and rate-limited 403 responses intelligently.
- Filters out pull requests if present.
- Normalizes each issue into the required internal format.
- Includes tests for:
    - pagination
    - retry behavior
    - normalization
    - PR filtering
"""


@dataclass
class NormalizedRecord:
    source: str
    external_id: str
    type: str
    timestamp: str
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "external_id": self.external_id,
            "type": self.type,
            "timestamp": self.timestamp,
            "data": self.data,
        }


class RateLimitError(Exception):
    """Raised when rate limit retries are exhauseted."""


class GitHubIssuesConnector:
    BASE_URL = "https://api.github.com"
    MAX_RETRIES = 5

    def __init__(self, token: str, session: Optional[requests.Session] = None) -> None:
        self.token = token
        self.session = session or requests.Session()

    def _request(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }

        for attempt in range(self.MAX_RETRIES):
            resp = self.session.get(url, headers=headers, params=params, timeout=10)
            # Rate Limit
            if resp.status_code in (429, 403):
                if attempt == self.MAX_RETRIES - 1:
                    raise RateLimitError(
                        f"Rate limit not cleared after {self.MAX_RETRIES} attempts"
                    )

                retry_after = resp.headers.get("Retry-After")
                reset_at = resp.headers.get("x-ratelimit-reset")

                if retry_after is not None:
                    time.sleep(int(retry_after))
                elif reset_at is not None:
                    wait_seconds = max(1, int(reset_at) - int(time.time()))
                    time.sleep(wait_seconds)
                else:
                    # default retry timer
                    time.sleep(60)

            if resp.status_code >= 500:
                if attempt == self.MAX_RETRIES - 1:
                    resp.raise_for_status()

                time.sleep(2**attempt)
                continue

            resp.raise_for_status()
            return resp

        raise RuntimeError(f"Request failed after retries: {url}")

    def _parse_next_link(self, link_header: Optional[str]) -> Optional[str]:
        if not link_header:
            return None

        parts = [p.strip() for p in link_header.split(",")]

        for part in parts:
            if 'rel="next"' in part:
                start = part.find("<") + 1
                end = part.find(">")
                if start > 0 and end > start:
                    return part[start:end]
        return None

    @staticmethod
    def _normalize(item: Dict[str, Any]) -> NormalizedRecord:
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
                "author_login": item.get("user", {}).get("login"),
            },
        )

    def list_issues(
        self, owner: str, repo: str, state: str = "open"
    ) -> List[NormalizedRecord]:
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": 100}
        records: List[NormalizedRecord] = []

        while url:
            resp = self._request(url, params=params)
            payload = resp.json()

            for item in payload:
                if "pull_request" in item:
                    continue
                records.append(self._normalize(item))

                url = self._parse_next_link(resp.headers.get("Link"))
                params = None

            return records


test_connector = GitHubIssuesConnector("<your_token>")

print(test_connector.list_issues("microsoft", "vscode", state="open")[0])
