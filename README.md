# GCP Billing
Extract GCP billing information.

## Preconditions
- Use a virtual environment
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
- (Optional) If you need to deactivate
```
deactivate
```
- If you add new dependencies
```
pip freeze > requirements.txt
```
- Enable GCP Billing Export:
* Go to the Google Cloud Console.
* Navigate to Billing > Settings.
* In the Billing export section, click on Edit settings.
* Set up the export to a BigQuery dataset.
- Have the billing account handy:
* Go to Billing / Account Management
* Copy the Billing account ID
* Your billing account is billingAccounts/${billingAccountId}
- Have your project ID handy:
* Go to Dashboard
* Click the top dropdown to select a project
* In the select resource dialog box, copy the ID
- Have the BigQuery dataset name handy
* Select your project
* Go to BigQuery / BigQuery Studio
* In the Explorer pane, expand the project ID; click the three dots of the dataset the appears below the project ID, and select "copy ID". The last token after the last dot is the dataset name
- Have the BigQuery table name handy
* Go to BigQuery / BigQuery Studio
* In the Explorer pane, expand the project ID and the dataset name; click the three dots of the table that appears below the dataset name, and select "copy ID". The last token after the last dot is the table name

## Running it
```
python gcp_billing_usage.py [-h] --key-file KEY_FILE from_date to_date billing_account project_id dataset_name table_name
```
For example, for July 2024:
```
python gcp_billing_usage.py 2024-07-01 2024-07-31 billingAccounts/1234BB-123CD4-A12B34 myproject-389419 myproject_billing gcp_billing_export_v1_1234BB_123CD4_A12B34 --key-file  /Users/nu/Downloads/myproject-123456-1a2b3c4d5e6f.json
```
