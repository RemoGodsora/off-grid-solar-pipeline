```mermaid
flowchart TD
    subgraph Edge["Edge Layer"]
        A["Edge Telemetry Simulator<br/><code>Python (IoT Telemetry)</code>"]
    end

    subgraph Streaming["Real-Time Streaming & Compute"]
        B["Message Broker<br/><code>Apache Kafka (solar_telemetry)</code>"]
        C["Distributed Compute<br/><code>PySpark (In-Memory Filter > 50V)</code>"]
    end

    subgraph Storage["Storage & Orchestration"]
        D[("Operational Store (Bronze)<br/><code>PostgreSQL Container</code>")]
        E["Orchestration Engine<br/><code>Mage AI (Enrichment DAG)</code>"]
        F[("Cloud Data Warehouse (Gold)<br/><code>Snowflake (TELEMETRY_WH)</code>")]
    end

    subgraph Observability["Monitoring"]
        G["SCADA Dashboard<br/><code>Grafana (Time-Series Metrics)</code>"]
    end

    A -->|Raw Stream| B
    B -->|Micro-Batch| C
    C -->|Persist Anomaly| D
    D -->|Real-Time Telemetry| G
    D -->|Batch Extraction| E
    E -->|TLS Egress / Idempotent Write| F

    classDef default fill:#1e1e24,stroke:#4f46e5,stroke-width:2px,color:#fff;
    classDef cloud fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#fff;
    class F cloud;



### Option 2: Copy-Paste Layout for Excalidraw / Draw.io

If you prefer an image file (`docs/architecture.png`) matching your previous canvas, arrange your blocks following this mapping:

| Layer | Node Label | Subtitle / Technology | Directed Arrows To |
| :--- | :--- | :--- | :--- |
| **1. Edge** | **Edge Simulator** | `Python (High-Frequency Telemetry)` | ──► **Message Broker** |
| **2. Broker** | **Message Broker** | `Apache Kafka (solar_telemetry)` | ──► **Distributed Compute** |
| **3. Compute** | **Distributed Compute** | `PySpark (In-Memory Anomaly Filter)` | ──► **Relational Store** |
| **4. Storage** | **Operational Store** | `PostgreSQL (Bronze Layer)` | ──► **SCADA Monitor**<br/>──► **Orchestration** |
| **5. Orchestrator**| **Orchestration** | `Mage AI (DAG: Power & Severity)` | ──► **Cloud Warehouse** |
| **6. Cloud Sink** | **Cloud Warehouse** | `Snowflake (Gold Layer: SOLAR_TELEMETRY)` | *(Terminal Node)* |
| **7. Monitor** | **SCADA Dashboard** | `Grafana (Real-Time Inverter Metrics)` | *(Terminal Node)* |

Export the canvas as `docs/architecture.png`, stage it with `git add docs/architecture.png`, and push.








# Autonomous IoT Solar Telemetry Pipeline

## System Architecture
An end-to-end Extract, Load, and Transform (ELT) pipeline designed to ingest, buffer, and analyze simulated edge hardware telemetry. 

* **Edge/Streaming Buffer:** Python Edge Simulator -> Apache Kafka
* **Orchestration & Compute:** Mage.ai (Containerized via Docker)
* **Storage & Data Warehouse:** Google BigQuery (Provisioned via Terraform)
* **Transformations & Analytics:** dbt (Data Build Tool)
* **System Telemetry & Alerting:** Discord Webhooks

## Execution Instructions
1. Clone the repository to your local compute environment.
2. Provision a Google Cloud Service Account with BigQuery Admin privileges. Save the credential file as `gcp_keys.json` in the root directory.
3. Initialize the orchestrator: `docker-compose up -d`
4. Ignite the edge simulator to begin the Kafka telemetry stream: `python solar_simulator.py`
5. Navigate to `localhost:6789` to monitor the pipeline DAG and autonomous dbt compilations.

## Certifications
* **[dbt Fundamentals Certification](https://credentials.getdbt.com/a3c1b121-55d5-4acb-91f6-425e37ec5bfa)** - Issued by dbt Labs
*This project utilizes dbt best practices (modular SQL, version control, and testing) validated by the official dbt Fundamentals credential.*

## System Telemetry Monitor
Below is the live Looker Studio dashboard connected to the BigQuery data warehouse, monitoring the daily AC power aggregations and hardware faults of the simulated off-grid solar array.

![Off-Grid Solar Telemetry Dashboard](dashboard.png)

Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
