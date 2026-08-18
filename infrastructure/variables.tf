variable "project_id" {
  description = "Your GCP Project ID"
  type        = string
  # Replace with your actual GCP Project ID (e.g., "de-zoomcamp-2026-502910")
  default     = "de-zoomcamp-2026-502910"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "gcs_bucket_name" {
  description = "Global unique name for the Data Lake bucket"
  type        = string
  # Bucket names must be globally unique across all GCP users
  default     = "solar-telemetry-lake-prod-2026"
}

variable "bq_dataset_name" {
  description = "BigQuery Raw Dataset Name"
  type        = string
  default     = "solar_telemetry_raw"
}