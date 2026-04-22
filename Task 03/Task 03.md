# Test 3: Build a GitHub Issues Connector

## Goal

Implement a working connector for the GitHub REST API that fetches, paginates, retries, and normalizes repository issues.

## Format

- You get this document at the start of the live session.
- You have 60 minutes.
- At the 60-minute mark, stop and send over whatever you have completed, even if unfinished.

## Scenario

You are building a connector for GitHub repository issues.

You must fetch issues from a repository, handle pagination, handle retries for transient errors and rate limits, and normalize the results into a common internal format.

### API

- Base URL: <https://api.github.com>
- Endpoint: GET /repos/{owner}/{repo}/issues
- Authentication: Authorization: Bearer `<token>`
- Pagination: Link header
- Rate limiting: 403 or 429, with x-ratelimit-reset and possibly Retry-After
- Important: this endpoint can return pull requests as well as issues, so filter out pull requests if you want issue-only records

### Example request

```plain
GET /repos/octocat/Hello-World/issues?state=open&per_page=100 Authorization: Bearer ghp_exampletoken Accept: application/vnd.github+json X-GitHub-Api-Version: 2026-03-10
```

### Example issue response

```json
[
  {
    "id": 1,
    "node_id": "MDU6SXNzdWUx",
    "number": 1347,
    "title": "Found a bug",
    "body": "I'm having a problem with this.",
    "state": "open",
    "locked": false,
    "comments": 0,
    "created_at": "2011-04-22T13:33:48Z",
    "updated_at": "2011-04-22T13:33:48Z",
    "user": { "login": "octocat", "id": 1 }
  }
]
```

### Pull request example you should exclude if filtering issues

```json
{
  "id": 2,
  "number": 100,
  "title": "Add feature",
  "pull_request": {
    "url": "https://api.github.com/repos/octocat/Hello-World/pulls/100"
  }
}
```

### Normalized record shape

Return each issue in this shape:

```json
{
  "source": "github",
  "external_id": "1347",
  "type": "issue",
  "timestamp": "2011-04-22T13:33:48Z",
  "data": {
    "number": 1347,
    "title": "Found a bug",
    "state": "open",
    "body": "I'm having a problem with this.",
    "comments": 0,
    "author_login": "octocat"
  }
}
```

## Your task

Implement a connector that:

1. Authenticates with GitHub using a bearer token.
2. Fetches issues from a repository.
3. Follows pagination using the Link header until there are no more pages.
4. Retries on transient 5xx errors.
5. Handles 429 and rate-limited 403 responses intelligently.
6. Filters out pull requests if present.
7. Normalizes each issue into the required internal format.
8. Includes tests for:
   - pagination
   - retry behavior
   - normalization
   - PR filtering

## Suggested starter code

You may use this as a starting point:

```python
from dataclasses import dataclass from typing import Any, Dict, List, Optional import time import requests @dataclass class NormalizedRecord: source: str external_id: str type: str timestamp: str data: Dict[str, Any] class GitHubIssuesConnector: def **init**(self, token: str, session: Optional[requests.Session] = None): self.base_url = "https://api.github.com" self.token = token self.session = session or requests.Session() def \_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response: headers = { "Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10", } for attempt in range(3): resp = self.session.get(url, headers=headers, params=params, timeout=10) if resp.status_code in (429, 403): retry_after = resp.headers.get("Retry-After") reset_at = resp.headers.get("x-ratelimit-reset") if retry_after is not None: time.sleep(int(retry_after)) continue if reset_at is not None: wait_seconds = max(1, int(reset_at) - int(time.time())) time.sleep(wait_seconds) continue if resp.status_code >= 500: time.sleep(2 \*\* attempt) continue resp.raise_for_status() return resp raise RuntimeError(f"Request failed after retries: {url}") def \_parse_next_link(self, link_header: Optional[str]) -> Optional[str]: if not link_header: return None parts = [p.strip() for p in link_header.split(",")] for part in parts: if 'rel="next"' in part: start = part.find("<") + 1 end = part.find(">") if start > 0 and end > start: return part[start:end] return None def list_issues(self, owner: str, repo: str, state: str = "open") -> List[NormalizedRecord]: url = f"{self.base_url}/repos/{owner}/{repo}/issues" params = {"state": state, "per_page": 100} records: List[NormalizedRecord] = [] while url: resp = self.\_request(url, params=params) payload = resp.json() for item in payload: if "pull_request" in item: continue records.append( NormalizedRecord( source="github", external_id=str(item["number"]), type="issue", timestamp=item["created_at"], data={ "number": item["number"], "title": item["title"], "state": item["state"], "body": item.get("body"), "comments": item.get("comments", 0), "author_login": item.get("user", {}).get("login"), }, ) ) url = self.\_parse_next_link(resp.headers.get("Link")) params = None return records
```

## What you should do

You do not need to use the exact starter code, but your solution should cover the same behavior.

Focus on:

- a clean implementation
- correct pagination
- correct retry logic
- good normalization
- tests that prove the behavior works

## Constraints

- Keep it practical and readable.
- You do not need to build a full production system.
- You do not need to support every GitHub endpoint.
- You only need to solve the issue-listing connector.

## What we are evaluating

- Can you build a working connector against a real API?
- Can you handle pagination correctly?
- Can you handle rate limits and retries sensibly?
- Can you write tests that validate behavior?
- Can you keep the code easy to extend later?

## Deliverable after 1 hour

Send:

- code or patch
- tests
- a short note explaining design decisions
  any incomplete parts if you run out of time

## Strong signals

- Correct use of Link header pagination
- Proper handling of 403, 429, and 5xx
- Pull requests filtered out cleanly
- Tests cover the important paths
- Clean normalization into the requested shape
