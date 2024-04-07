import logging

from github import Github
from github import Auth

import env

access_token = env.config["GITHUB_ACCESS_TOKEN"]

auth = Auth.Token(access_token)

# Public Web Github
g = Github(auth=auth)

def create_issue(message: str):
    repo = g.get_repo("42mogle/42-api-renew-log")
    issue = repo.create_issue(
        title="Failed to renew API secret",
        body=message,
    )
    logging.info(f"Successfully created issue: {issue.html_url}")