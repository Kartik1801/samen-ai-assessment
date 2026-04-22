# Test 2: Architecture Design for a Universal API Connector

## Goal

Design a platform that can connect to many APIs using one reusable connector system.

## Scenario

You are given a GitHub repository with thousands of API definitions. Some are OpenAPI specs, some are JSON manifests, and some are only partially documented. We want a platform that can ingest them, normalize them, and produce working connectors.

## Your task

Design the system end to end.

## You should cover

1. How the repository is ingested.
2. How APIs are classified and normalized.
3. How connectors are generated or loaded.
4. How auth, pagination, retries, and rate limiting work.
5. How schemas are validated and versioned.
6. How new APIs are onboarded.
7. How unsafe or malformed specs are handled.

## Example API manifest

```json
{
  "provider": "github",
  "base_url": "https://api.github.com",
  "auth": { "type": "oauth2" },
  "pagination": { "type": "link_header" },
  "rate_limit": { "strategy": "server_driven" },
  "objects": [
    { "name": "repos", "path": "/user/repos", "primary_key": "id" },
    {
      "name": "issues",
      "path": "/repos/{owner}/{repo}/issues",
      "primary_key": "id"
    }
  ]
}
```

## Desired connector interface

```typescript
interface Connector {
  discover(): Promise<ResourceSpec[]>;
  authenticate(): Promise<void>;
  list(
    resource: string,
    cursor?: string,
  ): Promise<{ items: any[]; nextCursor?: string }>;
  get(resource: string, id: string): Promise<any>;
  normalize(raw: any): NormalizedRecord;
}
```

## Suggested platform API

```plain
POST /v1/connectors
POST /v1/connectors/{id}/validate
POST /v1/connectors/{id}/sync
GET /v1/connectors/{id}/status
GET /v1/catalog/apis
```

## What your design should include

- Repo scanner for OpenAPI, manifests, and docs.
- Connector registry.
- Adapter/plugin layer.
- Auth and secret management.
- Retry/backoff for 429 and 5xx errors.
- Pagination abstraction.
- Observability: logs, metrics, traces.
- Contract testing with mocked API responses.
- A safe execution model for untrusted API definitions.

## What we are evaluating

- System design clarity.
- Modularity.
- Practicality.
- Ability to scale from one API to thousands.
- Ability to reason about real-world API failure modes.

## Deliverable after 1 hour

- A short architecture document or diagram.
- Key components and their responsibilities.
- Main data flow from GitHub repo to working connector.
- Tradeoffs and risks.

## Strong signals

- Separates ingestion, normalization, runtime, and validation.
- Does not hard-code provider behavior.
- Mentions schema drift, rate limits, auth refresh, and observability.
- Gives a credible path from “repo of thousands of APIs” to “usable connector.”

Use: <https://github.com/APIs-guru/openapi-directory>
