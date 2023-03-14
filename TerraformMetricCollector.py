import TerraformMetrics as tfcloud

ORGANIZATION = ""
json_file = "data.json"
workspaces_names = "workspaces.txt"

total_pages = tfcloud.TotalNumberOfPages(ORGANIZATION)
tfcloud.ListWorkspaces(ORGANIZATION, total_pages, json_file)
tfcloud.GetWorkspacesName(total_pages, json_file, workspaces_names)
tfcloud.GetTerraformWorkspacesMetrics(ORGANIZATION, workspaces_names)
