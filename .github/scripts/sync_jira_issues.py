import os
import requests

# Jira API credentials
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PARENT_ISSUE_ID = "CS4067-1"  # Replace with actual Jira parent issue ID

# GitHub credentials
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # owner/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_PROJECT_ID = os.getenv("GITHUB_PROJECT_ID")  # Use new GraphQL Project ID

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


def add_issue_to_project(issue_node_id):
    """Use GraphQL to add the GitHub issue to the GitHub Project (Beta)."""
    url = "https://api.github.com/graphql"
    query = """
    mutation {
      addProjectV2ItemById(input: {projectId: "%s", contentId: "%s"}) {
        item {
          id
        }
      }
    }
    """ % (GITHUB_PROJECT_ID, issue_node_id)

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"query": query}, headers=headers)
    return response.status_code == 200


def process_jira_issues(issue_id):
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
        add_issue_to_project(github_issue_node_id)

    # Process all levels of child issues
    if "fields" in issue and "subtasks" in issue["fields"]:
        for child in issue["fields"]["subtasks"]:
            process_jira_issues(child["key"])  # Recursively process child issues


# Start processing from the main parent issue
process_jira_issues(JIRA_PARENT_ISSUE_ID)
