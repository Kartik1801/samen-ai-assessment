from unittest.mock import MagicMock

import requests

from code import GitHubIssuesConnector, NormalizedRecord

SAMPLE_ISSUE = {
    id: 1,
    "node_id": "node_123",
    "number": 12234,
    "title": "ISSUE",
    "body": "Test",
    "state": "open",
    "locked": False,
    "comments": 0,
    "created_at": "2011-04-10T20:09:31Z",
    "updated_at": "2014-03-03T18:58:10Z",
    "users": {
        "login": "octocat",
        "id": 1,
    },
}

SAMPLE_PR = {
    id: 2,
    "node_id": "node_213",
    "number": 1224,
    "title": "PR",
    "body": "Test",
    "state": "open",
    "locked": False,
    "comments": 0,
    "created_at": "2011-04-10T20:09:31Z",
    "updated_at": "2014-03-03T18:58:10Z",
    "users": {
        "login": "octocat",
        "id": 1,
    },
    "pull_request": {
        "url": "https://api.github.com/repos/octocat/Hello-World/pulls/1347",
    },
}


def make_response(json_data, status_code, headers: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=requests.Request)
    resp.status_code = status_code
    resp.json.return_value = json_data
    resp.headers = headers
    resp.text = ""
    resp.raise_for_status = MagicMock()
    return resp


def make_connector():
    return GitHubIssuesConnector(token="test_token")


class TestNormalization:
    def test_shape(self):
        record = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert isinstance(record, NormalizedRecord)
        assert record.source == "github"
        assert record.external_id == 12234
        assert record.type == "issue"

    def test_data_fields(self):
        record = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert record["number"] == 12234
        assert record["title"] == "ISSUE"
        assert record["state"] == "open"
        assert record["comments"] == 0
        assert record["author_login"] == "octocat"

    def test_external_id_is_string(self):
        record = GitHubIssuesConnector._normalize(SAMPLE_ISSUE)
        assert isinstance(record.external_id, str)

    def test_missing_body_defaults_to_none(self):
        item = {**SAMPLE_ISSUE, "body": None}
        record = GitHubIssuesConnector._normalize(item)
        assert record["data"] is None

    def test_missing_user_defaults(self):
        item = {**SAMPLE_ISSUE, "user": None}
        record = GitHubIssuesConnector._normalize(item)
        assert record.data["author_login"] is None
