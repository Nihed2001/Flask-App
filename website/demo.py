import os
import pandas as pd
from . import ga4  # Corrected import statement

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/nihed/digital_application/website/ga4_service_account.json'

property_id = '434126696'

# Update the dimensions to include 'appVersion'
lst_dimension = ['country', 'deviceCategory', 'minutesAgo', 'appVersion']

# Update the metrics as needed
lst_metrics = ['activeUsers']  # Add any additional metrics you're interested in

# Import GA4RealTimeReport from ga4 module
from .ga4 import GA4RealTimeReport

ga4_realtime = GA4RealTimeReport(property_id)

response = ga4_realtime.query_report(
    lst_dimension, lst_metrics, 10, True
)
print(response['headers'])
print(response['rows'])

# Convert the response to a DataFrame
df = pd.DataFrame(data=response['rows'], columns=response['headers'])
print(df)
