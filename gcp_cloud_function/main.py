import os
import datetime
import requests
from github import Github

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "https://hooks.slack.com/services/T12345678/B12345678/abcdefghi12345678")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your-github-access-token-secret-id")
GITHUB_ORGANIZATION = os.getenv("GITHUB_ORGANIZATION", "your_organization")
DURATION_THRESHOLD = int(os.getenv("DURATION_THRESHOLD", 3))

# Function can be invoked with any type of HTTP Method
def check_pending_reviews(request):
    # Configure your GitHub access token
    github_token = GITHUB_TOKEN
    github = Github(github_token)
    org_name = GITHUB_ORGANIZATION

    # Configure your Slack webhook URL
    slack_webhook_url = SLACK_WEBHOOK

    # Get the current time
    now = datetime.datetime.utcnow()

    # Get all open pull requests in the organization
    org = github.get_organization(org_name)
    open_pulls = org.get_pulls(state="open")

    # Check each open pull request for pending reviews
    for pull in open_pulls:
        reviews = pull.get_reviews()

        # Check each review for pending status and duration
        for review in reviews:
            if review.state == "PENDING":
                created_at = review.submitted_at

                # Calculate the duration in days
                duration = now - created_at
                if duration.days > DURATION_THRESHOLD:
                    # Send Slack notification
                    message = f":rotating_light: PR Review Alert: The PR #{pull.number} in {org_name}/{pull.base.repo.name} has been pending for more than {DURATION_THRESHOLD} days! :rotating_light:"
                    payload = {
                        "channel": "#your-channel",
                        "text": message
                    }
                    response = requests.post(slack_webhook_url, json=payload)
                    response.raise_for_status()

    return "Success"