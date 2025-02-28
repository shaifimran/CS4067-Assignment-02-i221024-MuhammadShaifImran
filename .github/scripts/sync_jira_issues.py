import os
import requests

# Jira API credentials
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PARENT_ISSUE_ID = "YOUR_PARENT_ISSUE_ID"  # Update this manually

# GitHub credentials
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # owner/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_PROJECT_NAME = os.getenv("GITHUB_PROJECT_NAME")

# Headers for Jira and GitHub
JIRA_HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Basic {os.getenv('JIRA_USERNAME')}:{JIRA_API_TOKEN}"
}

GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_jira_issue(issue_id):
    """Fetch a Jira issue along with its child issues."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_id}?expand=subtasks"
    response = requests.get(url, headers=JIRA_HEADERS)
    return response.json() if response.status_code == 200 else None


def create_github_issue(title):
    """Create a new GitHub issue with only the title."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    data = {"title": title}
    response = requests.post(url, json=data, headers=GITHUB_HEADERS)
    if response.status_code == 201:
        return response.json()["id"], response.json()["node_id"]
    return None, None


def get_project_id():
    """Retrieve the project ID based on the project name."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/projects"
    response = requests.get(url, headers=GITHUB_HEADERS)
    
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project["name"] == GITHUB_PROJECT_NAME:
                return project["id"]
    return None


def get_todo_column_id(project_id):
    """Find the 'To Do' column ID in the GitHub project."""
    url = f"https://api.github.com/projects/{project_id}/columns"
    response = requests.get(url, headers=GITHUB_HEADERS)
    
    if response.status_code == 200:
        columns = response.json()
        for column in columns:
            if column["name"].lower() == "to do":
                return column["id"]
    return None


def add_issue_to_project(column_id, issue_node_id):
    """Add the GitHub issue to the project's 'To Do' column."""
    url = f"https://api.github.com/projects/columns/{column_id}/cards"
    data = {"content_id": issue_node_id, "content_type": "Issue"}
    response = requests.post(url, json=data, headers=GITHUB_HEADERS)
    return response.status_code == 201


def process_jira_issues(issue_id, column_id):
    """Recursively process Jira issues and create corresponding GitHub issues."""
    issue = get_jira_issue(issue_id)
    if not issue:
        print(f"Failed to fetch Jira issue {issue_id}")
        return

    issue_key = issue["key"]
    title = issue["fields"]["summary"]

    # Format title as "[Issue Key] Title"
    formatted_title = f"[{issue_key}] {title}"

    # Create GitHub issue
    github_issue_id, github_issue_node_id = create_github_issue(formatted_title)
    if github_issue_id and github_issue_node_id:
        add_issue_to_project(column_id, github_issue_node_id)

    # Process all levels of child issues
    if "fields" in issue and "subtasks" in issue["fields"]:
        for child in issue["fields"]["subtasks"]:
            process_jira_issues(child["key"], column_id)  # Recursively process child issues


# Get the GitHub project ID
project_id = get_project_id()
if project_id:
    todo_column_id = get_todo_column_id(project_id)
    if todo_column_id:
        # Start processing from the main parent issue
        process_jira_issues(JIRA_PARENT_ISSUE_ID, todo_column_id)
    else:
        print("Failed to find 'To Do' column in the GitHub project.")
else:
    print("Failed to find the GitHub project.")
