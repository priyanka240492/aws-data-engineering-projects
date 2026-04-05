# AWS Data Engineering Projects

A collection of end-to-end data engineering projects built on AWS, covering real-time streaming and CI/CD pipeline automation. Each project is self-contained with its own infrastructure, code, and documentation.

---

## Repository Structure

```
aws-data-engineering-projects/
├── aws-real-time-data-streaming-prj/
└── aws-cicd-deployment-prj/
```

---

## Projects

### 1. `aws-real-time-data-streaming-prj/`

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

### 2. `aws-cicd-deployment-prj/`

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
| Storage | S3 |
| Compute | Lambda |
| Messaging | Kinesis Data Streams |
| CI/CD | CodePipeline, CodeBuild, CodeConnections, CloudFormation |
| Analytics | Athena, Glue Crawler, Glue Data Catalog |
| Observability | CloudWatch Logs & Metrics |

---

## Getting Started

Each subfolder contains its own `README.md` with:
- Architecture diagram
- Prerequisites
- Deployment instructions

Clone the repository and navigate to any project folder to get started:

```bash
git clone https://github.com/priyanka240492/aws-data-engineering-projects.git
cd aws-data-engineering-projects/<project-folder>
```

---

## Author

**Lakshmi Priyanka K** — Lead Data Engineer  
Building AWS-native data infrastructure with a focus on reliability, observability, and clean pipeline design.
