import logging

from github import Github
from github import Auth

from .env import config as env

ACCESS_TOKEN = env["GITHUB_ACCESS_TOKEN"]
REPOSITORY = env["GITHUB_REPOSITORY"]

auth = Auth.Token(ACCESS_TOKEN)

# Public Web Github
g = Github(auth=auth)

def create_issue(message: str):
    repo = g.get_repo(REPOSITORY)
    issue = repo.create_issue(
        title="Failed to renew API secret",
        body=message,
    )
    logging.info(f"Successfully created issue: {issue.html_url}")