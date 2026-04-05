# AWS Data Engineering Projects

A collection of end-to-end data engineering projects built on AWS, covering batch ingestion, real-time streaming, CDC, and CI/CD pipeline automation. Each project is self-contained with its own infrastructure, code, and documentation.

---

## Repository Structure

```
aws-data-engineering-projects/
├── pharma-vendor-file-pipeline/
├── clickstream-realtime-pipeline/
├── aurora-cdc-logical-replication/
└── lambda-cicd-codepipeline/
```

---

## Projects

### 1. `pharma-vendor-file-pipeline/`

**Purpose:** Batch ingestion pipeline that processes multi-format vendor files (CSV, PDF, XML) from pharmaceutical vendors and loads them into Aurora PostgreSQL as structured key-value records.

**AWS Services Used:**
`S3` · `SQS` · `Lambda` · `AWS Glue (Python Shell)` · `Aurora PostgreSQL` · `RDS Proxy` · `CloudWatch`

**Process Flow:**

```
Vendor File Upload (S3)
        │
        ▼
S3 Event Notification
        │
        ▼
SQS Queue 1 (Dispatch Queue)
        │
        ▼
Lambda (File Router)
  ├── Parses file type (CSV / PDF / XML)
  ├── Extracts metadata and sample_id
  └── Writes audit stage 1–4 to Aurora via RDS Proxy
        │
        ▼
SQS Queue 2 (Glue Trigger Queue)
        │
        ▼
AWS Glue Python Shell Job
  ├── Reads file from S3
  ├── Transforms rows → key-value pairs (pandas melt)
  ├── Upserts into Aurora PostgreSQL (psycopg2, chunked batch inserts)
  └── Writes audit stages 5–8 to Aurora via RDS Proxy
```

**Key Design Decisions:**
- Two-queue SQS architecture separates routing logic from heavy processing
- Glue Python Shell chosen over Spark to avoid cold start overhead
- RDS Proxy prevents connection storms during concurrent Glue job runs
- 8 audit stages tracked inline across Lambda and Glue for full observability
- Idempotent upserts using `ON CONFLICT DO UPDATE` for safe re-processing

---

### 2. `clickstream-realtime-pipeline/`

**Purpose:** Real-time streaming pipeline that ingests clickstream events (page views, user actions) from a web application, processes them through Kinesis, and makes them queryable via Athena on S3.

**AWS Services Used:**
`Kinesis Data Streams` · `Lambda` · `S3` · `AWS Glue Crawler` · `Amazon Athena` · `CloudWatch`

**Process Flow:**

```
Clickstream Events (Web App / Producer Script)
        │
        ▼
Kinesis Data Stream
        │
        ▼
Lambda (Stream Consumer)
  ├── Reads records from Kinesis shard(s)
  ├── Deserializes and enriches event payload
  └── Writes partitioned JSON/Parquet files to S3
        │
        ▼
S3 (Raw Events — partitioned by date/event type)
        │
        ▼
Glue Crawler (scheduled)
  └── Infers schema → updates Glue Data Catalog
        │
        ▼
Amazon Athena
  └── Ad-hoc SQL queries on clickstream data
```

**Key Design Decisions:**
- Kinesis chosen for ordered, replayable event delivery
- Lambda consumer writes micro-batches to S3 for cost-efficient storage
- Glue Crawler automates schema evolution as event structure changes
- Athena enables serverless querying with no dedicated warehouse cost

---

### 3. `aurora-cdc-logical-replication/`

**Purpose:** Change Data Capture (CDC) implementation on Aurora PostgreSQL using native logical replication — capturing row-level INSERT, UPDATE, and DELETE changes without any external tools or services.

**AWS Services Used:**
`Aurora PostgreSQL` · `pg_cron` · `CloudWatch Logs`

**Process Flow:**

```
Aurora PostgreSQL (Source Table)
        │
    WAL (Write-Ahead Log)
        │
        ▼
Logical Replication Slot
  └── pgoutput plugin decodes WAL → change events
        │
        ▼
pg_cron Scheduled Job
  ├── Polls replication slot at defined intervals
  ├── Parses decoded change events (INSERT / UPDATE / DELETE)
  └── Writes CDC records to a change_log table in Aurora
        │
        ▼
Change Log Table (queryable within Aurora)
```

**Key Design Decisions:**
- Entirely self-contained within Aurora — no Kafka, DMS, or Debezium needed
- `pgoutput` is Aurora's native logical decoding plugin (no extensions required)
- `pg_cron` replaces external schedulers, keeping the solution serverless-friendly
- Change log table stores operation type, timestamp, old/new values per row

---

### 4. `lambda-cicd-codepipeline/`

**Purpose:** CI/CD pipeline for automated deployment of AWS Lambda functions using AWS Developer Tools — source-controlled on GitHub and deployed via CloudFormation.

**AWS Services Used:**
`AWS CodePipeline` · `AWS CodeBuild` · `AWS CodeConnections (GitHub)` · `CloudFormation` · `S3 (Artifact Store)` · `Lambda` · `IAM`

**Process Flow:**

```
Code Push to GitHub (main branch)
        │
        ▼
CodeConnections Webhook Trigger
        │
        ▼
CodePipeline
  ├── Stage 1 — Source
  │     └── Pulls source from GitHub via CodeConnections
  ├── Stage 2 — Build (CodeBuild)
  │     ├── Installs dependencies
  │     ├── Runs unit tests
  │     ├── Packages Lambda deployment artifact (ZIP)
  │     └── Uploads artifact to S3
  └── Stage 3 — Deploy (CloudFormation)
        ├── Creates/Updates CloudFormation stack
        └── Deploys packaged Lambda function
```

**Key Design Decisions:**
- Pure CloudFormation approach (no SAM) for full infrastructure control
- CodeConnections manages GitHub OAuth — no personal access tokens stored
- S3 artifact bucket serves as the handoff layer between Build and Deploy stages
- All resources (pipeline, build project, Lambda, IAM roles) defined as IaC

---

## Tech Stack Summary

| Category | Services |
|---|---|
| Storage | S3, Aurora PostgreSQL |
| Compute | Lambda, AWS Glue Python Shell |
| Messaging | SQS, Kinesis Data Streams |
| Networking / Proxy | RDS Proxy |
| CI/CD | CodePipeline, CodeBuild, CodeConnections, CloudFormation |
| Analytics | Athena, Glue Crawler, Glue Data Catalog |
| Scheduling | pg_cron |
| Observability | CloudWatch Logs & Metrics |

---

## Getting Started

Each subfolder contains its own `README.md` with:
- Architecture diagram
- Prerequisites and IAM permissions required
- Deployment instructions
- Sample data / test events

Clone the repository and navigate to any project folder to get started:

```bash
git clone https://github.com/priyanka240492/aws-data-engineering-projects.git
cd aws-data-engineering-projects/<project-folder>
```

---

## Author

**Priya** — Data Engineer  
Building AWS-native data infrastructure with a focus on reliability, observability, and clean pipeline design.
