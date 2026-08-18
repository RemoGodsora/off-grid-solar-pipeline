terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  
  # The physical wire bypasses volatile environment variables
  credentials = file("keys.json") 
}

# 1. GCS Data Lake Bucket
resource "google_storage_bucket" "data_lake" {
  name          = var.gcs_bucket_name
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // Auto-purge raw test files after 30 days to optimize storage cost
    }
  }
}

# 2. BigQuery Data Warehouse Raw Landing Dataset
resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.region
  delete_contents_on_destroy = true
}

# 3. BigQuery Data Warehouse Analytics Dataset (dbt Output)
resource "google_bigquery_dataset" "analytics_dataset" {
  dataset_id                 = "solar_analytics"
  location                   = var.region
  delete_contents_on_destroy = true
}