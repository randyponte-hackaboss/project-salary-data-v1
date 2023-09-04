# Import required modules
from googleapiclient.discovery import build
import datetime

# Set up the API client with your API key
api_key = 'YOUR_API_KEY_HERE'
service = build('jobs', 'v3', developerKey=api_key)

# Define search parameters
query = 'Software Engineer'
location = 'San Francisco, CA'
radius = '50mi'
company = 'Google'
employment_type = 'FULL_TIME'
language_code = 'en-US'
publish_before = datetime.datetime.now().isoformat()  # jobs published before the current time

# Make API request
result = service.jobs().search(
    body={
        'query': query,
        'locationFilters': {
            'location': location,
            'distanceInMiles': radius,
        },
        'companyName': company,
        'employmentTypes': [employment_type],
        'languageCodes': [language_code],
        'publishBefore': publish_before,
    }
).execute()

# Print the job listings
for job in result.get('matchingJobs', []):
    print(f"{job.get('jobTitle', 'No title available')}: {job.get('jobLocations', [])}")
    print(f"Company: {job.get('hiringOrganization', {}).get('name', 'No company name available')}")
    print(f"Employment type: {job.get('employmentTypes', [])}")
    print(f"Date posted: {job.get('postingCreateTime', 'No posting create time available')}")
    print(f"Description: {job.get('description', 'No description available')}")
    print('--------------------------')
