# gcp-team-cost-reporter
Report on costs in Google Cloud

We have our GCP dev teams broken down by folder, and export the cost data to BiqQuery (https://cloud.google.com/billing/docs/how-to/export-data-bigquery)
This tool will collate that data based on the folder ID and email the individual teams.