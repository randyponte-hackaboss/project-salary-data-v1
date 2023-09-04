# 
# pip install google-api-python-client

from googleapiclient.discovery import build

api_key = 'YOUR_API_KEY_HERE'
service = build('jobs', 'v3', developerKey=api_key)


# Define search parameters
query = 'Python Developer'
location = 'New York'
radius = '50mi'

# Make API request
result = service.jobs().search(
    body={
        'query': query,
        'locationFilters': {
            'location': location,
            'distanceInMiles': radius,
        },
    }
).execute()

# Print the job listings
for job in result.get('matchingJobs', []):
    print(f"{job.get('jobTitle', 'No title available')}: {job.get('jobLocations', [])}")
