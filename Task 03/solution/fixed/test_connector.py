"""
Tests for the GitHub issues connector.

Fixes vs. the original test.py:
  - `id: 1` (using the builtin `id` function as a dict key) → "id": 1.
  - `record["field"]` access replaced with proper dataclass access
    (NormalizedRecord is not subscriptable).
  - `external_id == 12234` fixed: external_id is a str ("12234").
  - test_missing_body checks `record.data["body"]`, not `record["data"]`.
  - test_missing_user no longer crashes; _normalize now tolerates None.
  - make_response uses spec=requests.Response (not Request) and
    raise_for_status actually raises on >= 400.
  - Added the tests the task asked for but weren't there:
      * pagination follows Link header across multiple pages
      * retries on 5xx then succeeds
      * 429 with Retry-After is retried
      * 403 with x-ratelimit-remaining=0 is retried
      * 403 without rate-limit headers is NOT retried (permission error)
      * sleep() is mocked so tests run in <1s

Run: pytest test_connector.py -v
"""

import pytest
from unittest.mock import MagicMock

import requests

from connector import (
    GitHubIssuesConnector,
    NormalizedRecord,
    RateLimitError,
)


SAMPLE_ISSUE = {
    "id": 1,
    "node_id": "node_123",
    "number": 12234,
    "title": "ISSUE",
    "body": "Test",
    "state": "open",
    "locked": False,
    "comments": 0,
    "created_at": "2011-04-10T20:09:31Z",
    "updated_at": "2014-03-03T18:58:10Z",
    "user": {"login": "octocat", "id": 1},
}

SAMPLE_PR = {
    "id": 2,
    "number": 1224,
    "title": "PR",
    "state": "open",
    "created_at": "2011-04-10T20:09:31Z",
    "user": {"login": "octocat", "id": 1},
    "pull_request": {
        "url": "https://api.github.com/repos/octocat/Hello-World/pulls/1"
    },
}


def make_response(json_data=None, status_code=200, headers=None):
    """Build a MagicMock that behaves like requests.Response for our needs."""
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.headers = headers or {}
    resp.json.return_value = json_data if json_data is not None else []

    def _raise():
        if status_code >= 400:
            err = requests.HTTPError(f"{status_code}")
            err.response = resp
            raise err

    resp.raise_for_status = MagicMock(side_effect=_raise)
    return resp


def make_connector():
    session = MagicMock(spec=requests.Session)
    conn = GitHubIssuesConnector(
        token="test",
        session=session,
        sleep=MagicMock(),          # no real sleeping
        now=lambda: 1_000_000,
    )
    return conn, session


# --------------------------- Normalization ---------------------------


class TestNormalization:
    def test_shape(self):
        r = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert isinstance(r, NormalizedRecord)
        assert r.source == "github"
        assert r.external_id == "12234"
        assert r.type == "issue"
        assert r.timestamp == "2011-04-10T20:09:31Z"

    def test_data_fields(self):
        r = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert r.data["number"] == 12234
        assert r.data["title"] == "ISSUE"
        assert r.data["state"] == "open"
        assert r.data["body"] == "Test"
        assert r.data["comments"] == 0
        assert r.data["author_login"] == "octocat"

    def test_external_id_is_string(self):
        r = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert isinstance(r.external_id, str)

    def test_missing_body_is_none(self):
        item = {k: v for k, v in SAMPLE_ISSUE.items() if k != "body"}
        r = GitHubIssuesConnector._normalize(item)
        assert r.data["body"] is None

    def test_user_none_yields_none_author(self):
        item = {**SAMPLE_ISSUE, "user": None}
        r = GitHubIssuesConnector._normalize(item)
        assert r.data["author_login"] is None

    def test_missing_comments_defaults_zero(self):
        item = {k: v for k, v in SAMPLE_ISSUE.items() if k != "comments"}
        r = GitHubIssuesConnector._normalize(item)
        assert r.data["comments"] == 0


# ----------------------------- PR filter -----------------------------


class TestPRFilter:
    def test_pull_requests_are_filtered(self):
        conn, session = make_connector()
        session.get.return_value = make_response(
            json_data=[SAMPLE_ISSUE, SAMPLE_PR], status_code=200
        )
        records = conn.list_issues("o", "r")
        assert len(records) == 1
        assert records[0].external_id == "12234"


# ----------------------------- Pagination -----------------------------


class TestPagination:
    def test_follows_link_header(self):
        conn, session = make_connector()
        page1 = make_response(
            json_data=[SAMPLE_ISSUE],
            status_code=200,
            headers={"Link": '<https://api.github.com/page2>; rel="next"'},
        )
        page2 = make_response(
            json_data=[{**SAMPLE_ISSUE, "number": 99999}],
            status_code=200,
            headers={},
        )
        session.get.side_effect = [page1, page2]

        records = conn.list_issues("o", "r")

        assert session.get.call_count == 2
        assert {r.external_id for r in records} == {"12234", "99999"}
        # second call must target the URL from the Link header
        second_call_url = session.get.call_args_list[1][0][0]
        assert second_call_url == "https://api.github.com/page2"
        # and must NOT resend per_page=100 (params=None after page 1)
        assert session.get.call_args_list[1][1]["params"] is None

    def test_single_page_no_next(self):
        conn, session = make_connector()
        session.get.return_value = make_response(
            json_data=[SAMPLE_ISSUE], status_code=200, headers={}
        )
        records = conn.list_issues("o", "r")
        assert len(records) == 1
        assert session.get.call_count == 1

    def test_three_pages(self):
        conn, session = make_connector()
        session.get.side_effect = [
            make_response(
                json_data=[{**SAMPLE_ISSUE, "number": n} for n in (1, 2)],
                status_code=200,
                headers={"Link": '<https://api.github.com/p2>; rel="next"'},
            ),
            make_response(
                json_data=[{**SAMPLE_ISSUE, "number": n} for n in (3, 4)],
                status_code=200,
                headers={"Link": '<https://api.github.com/p3>; rel="next"'},
            ),
            make_response(
                json_data=[{**SAMPLE_ISSUE, "number": 5}],
                status_code=200,
                headers={},
            ),
        ]
        records = conn.list_issues("o", "r")
        assert [r.external_id for r in records] == ["1", "2", "3", "4", "5"]


# ------------------------------ Retries ------------------------------


class TestRetries:
    def test_retries_on_5xx_then_succeeds(self):
        conn, session = make_connector()
        session.get.side_effect = [
            make_response(status_code=500),
            make_response(status_code=502),
            make_response(json_data=[SAMPLE_ISSUE], status_code=200),
        ]
        records = conn.list_issues("o", "r")
        assert len(records) == 1
        assert session.get.call_count == 3

    def test_rate_limit_429_retry_after(self):
        conn, session = make_connector()
        session.get.side_effect = [
            make_response(status_code=429, headers={"Retry-After": "2"}),
            make_response(json_data=[SAMPLE_ISSUE], status_code=200),
        ]
        records = conn.list_issues("o", "r")
        assert len(records) == 1
        conn._sleep.assert_any_call(2)

    def test_rate_limit_403_with_remaining_zero(self):
        conn, session = make_connector()
        session.get.side_effect = [
            make_response(
                status_code=403,
                headers={
                    "x-ratelimit-remaining": "0",
                    "x-ratelimit-reset": str(1_000_030),  # +30s from now
                },
            ),
            make_response(json_data=[SAMPLE_ISSUE], status_code=200),
        ]
        records = conn.list_issues("o", "r")
        assert len(records) == 1
        conn._sleep.assert_any_call(30)

    def test_permission_403_is_raised_not_retried(self):
        conn, session = make_connector()
        # 403 with no rate-limit signal = real permission error
        session.get.return_value = make_response(
            status_code=403, headers={"x-ratelimit-remaining": "4999"}
        )
        with pytest.raises(requests.HTTPError):
            conn.list_issues("o", "r")
        assert session.get.call_count == 1

    def test_exhausts_retries_raises(self):
        conn, session = make_connector()
        session.get.return_value = make_response(
            status_code=429, headers={"Retry-After": "1"}
        )
        with pytest.raises(RateLimitError):
            conn.list_issues("o", "r")
        assert session.get.call_count == GitHubIssuesConnector.MAX_RETRIES


# --------------------------- Link parsing ---------------------------


class TestLinkHeader:
    def test_parse_next_present(self):
        hdr = (
            '<https://api.github.com/a?page=2>; rel="next", '
            '<https://api.github.com/a?page=5>; rel="last"'
        )
        assert (
            GitHubIssuesConnector._parse_next_link(hdr)
            == "https://api.github.com/a?page=2"
        )

    def test_parse_next_absent(self):
        hdr = '<https://api.github.com/a?page=5>; rel="last"'
        assert GitHubIssuesConnector._parse_next_link(hdr) is None

    def test_parse_none_header(self):
        assert GitHubIssuesConnector._parse_next_link(None) is None
