import os
from jira import JIRA
from github import Github

# Retrieve environment variables
jira_server = os.getenv('JIRA_BASE_URL')
jira_email = os.getenv('JIRA_EMAIL')
jira_api_token = os.getenv('JIRA_API_TOKEN')
github_token = os.getenv('GITHUB_TOKEN')
github_repo_name = os.getenv('GITHUB_REPOSITORY')
github_project_id = os.getenv('GITHUB_PROJECT_ID')
jira_parent_issue_id = 'CS4067-1'  # Replace with your Jira parent issue ID

# Initialize Jira client
jira_options = {'server': jira_server}
jira = JIRA(options=jira_options, basic_auth=(jira_email, jira_api_token))

# Initialize GitHub client
github = Github(github_token)
repo = github.get_repo(github_repo_name)
project = github.get_project(int(github_project_id))

def create_github_issue(title):
    """Create a new GitHub issue with the given title."""
    issue = repo.create_issue(title=title)
    return issue

def add_issue_to_project(issue):
    """Add the created GitHub issue to the specified GitHub project."""
    project.add_to_columns(issue)

def process_jira_issues(issue_id):
    """Recursively process Jira issues and create corresponding GitHub issues."""
    issue = jira.issue(issue_id)
    title = f'[{issue.key}] {issue.fields.summary}'

    # Create GitHub issue
    github_issue = create_github_issue(title)
    add_issue_to_project(github_issue)

    # Process subtasks
    for subtask in issue.fields.subtasks:
        process_jira_issues(subtask.key)

# Start processing from the main parent issue
process_jira_issues(jira_parent_issue_id)
