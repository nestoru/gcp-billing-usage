import argparse
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

def query_billing_data(start_date, end_date, key_file, project_id, dataset_name, table_name):
    credentials = service_account.Credentials.from_service_account_file(key_file)
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = f"""
    SELECT
      project.id as project_id,
      service.description as service,
      SUM(cost) as amount,
      currency
    FROM `{project_id}.{dataset_name}.{table_name}`
    WHERE DATE(usage_start_time) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
    GROUP BY project_id, service, currency
    ORDER BY amount DESC
    """

    query_job = client.query(query)
    results = query_job.result()

    return results

def main():
    parser = argparse.ArgumentParser(description='Fetch GCP billing data from BigQuery.')
    parser.add_argument('from_date', type=str, help='The start date for the billing retrieval in YYYY-MM-DD format.')
    parser.add_argument('to_date', type=str, help='The end date for the billing retrieval in YYYY-MM-DD format.')
    parser.add_argument('billing_account', type=str, help='The GCP billing account ID in the format billingAccounts/ACCOUNT_ID')
    parser.add_argument('project_id', type=str, help='The GCP project ID where the billing data is stored.')
    parser.add_argument('dataset_name', type=str, help='The name of the BigQuery dataset where billing data is stored.')
    parser.add_argument('table_name', type=str, help='The name of the BigQuery table where billing data is stored.')
    parser.add_argument('--key-file', type=str, required=True, help='Path to the Google Cloud service account JSON key file.')

    args = parser.parse_args()

    try:
        # Validate date format
        start_date = datetime.strptime(args.from_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.to_date, '%Y-%m-%d')

        results = query_billing_data(args.from_date, args.to_date, args.key_file, args.project_id, args.dataset_name, args.table_name)
        
        total_cost = 0.0
        currency = "USD"  # Default unit, assuming all costs are in the same unit

        if results.total_rows > 0:
            print("GCP Projects, Services, and their costs for the specified date range:")
            for row in results:
                print(f"Project ID: {row['project_id']}, Service: {row['service']}, Cost: {row['amount']:.2f} {row['currency']}")
                total_cost += row['amount']
                currency = row['currency']
            
            print(f"Total cost: {total_cost:.2f} {currency}")
        else:
            print("No cost data available for the specified period.")

    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

