# Universal API Connector

## Components

1. **Ingestion** - Scan the github repo, detect api specification (OpenAPI, JSON, or something else). For each API Specification, can use a **QUEUE** for processing.[ Enqueue({spec: <spec_file>, type: "open_api" | "manifest" | "partial_docs", format: "yaml" | "json" | "other", ...`<metadata or path>`}) ]
2. **Parsing** - Parse the API Specification from queue, depending on the type of Specification - OpenAPI YAML/JSON, JSON Manifest, partial Docs.
3. **Normalization** - Convert all the parsed API Specs to a standardized format that can be used internally by connector.
4. **Registering** - Store normalized API specs with it's metadata like versioning, credentials / auth details, etc.
5. **Connector Generation** - Create a Adaptor/Connector that can read from Registered API Specs and perform relevant functions (discover, list, get, etc.)
6. **Runtime** - Executing functions like discover, authenticate, rate limits, retries etc.
7. **Observe** - Create logs for each operation, generate metrics, alerts etc.

## System Design

### 1. Ingestion

- Can create a script or something that clones or incrementally pulls API Specs from Github. Can also add a webhook or poll to watch changes in Github.
- For each API, perform following operations
  - **Detect File Type** - yaml => OPENAPI, json => Manifest, .md / other => Partial Docs etc.
  - **Detect Changes in a File** - create hash of file to detect if there are any changes in file. If hash do not match then re-process
  - Push the File to Queue for processing / parsing. Can use a Cloud based Queue, Redis or kafka for continuos processing.
  - Depending on the scale or number of file can implement batch / bulk processing of Files to incrementally process / ingest at scale.

### 2. Parser

- We need mainly 3 type of parsers that will read items from queue and process:
  - OPENAPI
    - Can create custom parser or use existing parser like `swagger-parser` to parse OPENAPI Specs and also use a validation lib like `zod` to ensure consistent parsing.
  - JSON Manifest,
    - Can create a custom script to extract keys/values with validator to parse JSON manifest.
  - Partial Docs
    - Can extract by reading and using keyword based matching to extract api specs. If not able to extract then can add a custom form to enter fields.

- Can scale horizontally for parallel processing

### 3. Normalization

- All the parsed Specs should be normalized into a standardized schema
- Can parse it into following structure
  - provider - string identifier
  - base_url - root endpoint
  - auth - auth config (JSON) / null
  - pagination - pagination config (JSON) / null
  - resources[] - array of {name: <name of resource>, path: <path>, primary_key: <pk>, ....}
  - version: <version_number>
  - confidence: <parsing confidence>
  - rate_limit: <rate limit config> (JSON)
    ...

### 4. Classification

- After normalization we can classify APIs based on classification score during parsing phase as:
  - Full (Auto Generated Connector)
  - Partial (Can use as Connector (unstable))
  - Minimal / Unsafe (need review or user intervention)

### 5. Registry and Connector Generator

- Take the Normalized, Classified Specs as input and generate Instance of Connector Class that implement functionalities like discover, auth etc.provided in task.
- Based on Classification may or may not support all features
- Can store the Specs in Postgres which will act as a Registry with following metadata - connector_id, created_at, updated_at, version, status, ...
- Based on this we can create REST API to expose the connector related information mentioned in Task Description

### 6. Runtime Auth, Pagination, Retries, & Rate Limit

- Can create common interfaces to handle authentication, pagination, retries and rate limits based on the extracted specs and configurations.
- Can also support common standards like OAuth2, API Key, Bearer Token etc. for Auth
