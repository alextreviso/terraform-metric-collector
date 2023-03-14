from json import load, dump
from csv import writer
from requests import get
from datetime import datetime

PAGE_SIZE = 100
URL = "https://app.terraform.io/api/v2/organizations/"
MY_TOKEN = ""
head = {'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(MY_TOKEN)}
parameters = {'page[size]': PAGE_SIZE}


def TotalNumberOfPages(organization):
    data = get(URL + organization + "/workspaces",
               params=parameters,  headers=head)
    total_pages = data.json()['meta']['pagination']['total-pages']
    return total_pages


def ListWorkspaces(organization, total_pages, filename):
    data = []
    for i in range(total_pages):
        p = {'page[number]': i+1, 'page[size]': PAGE_SIZE}
        r = get(URL + organization + "/workspaces",
                params=p,  headers=head)
        data.append(r.json())

    with open(filename, "w") as file:
        dump(data, file)


def GetWorkspacesName(total_pages, json_file, txt_file):
    with open(json_file, 'r') as file:
        data_json = load(file)

    workspaces = ""
    for i in range(total_pages):
        for j in range(PAGE_SIZE):
            try:
                workspaces += data_json[i]['data'][j]['attributes']['name'] + "\n"
            except IndexError:
                pass
            continue

    text_file = open(txt_file, "w+")
    text_file.write(workspaces)
    text_file.close()


def GetTerraformWorkspacesMetrics(organization, txt_file):
    terraform_metrics = []

    now = datetime.now()
    currentYear = now.strftime("%Y")
    currentMonth = now.strftime("%m")
    currentDay = now.strftime("%d")
    outputName = "terraform_metrics_" + currentYear + \
        "-" + currentMonth + "-" + currentDay + "-" + ".csv"

    workspaces = open(txt_file, 'r')

    for workspace in workspaces:
        data = get(
            (URL + organization + "/workspaces/" + workspace).strip(), headers=head)
        metrics = []

        metrics.append(data.json()['data']['attributes']['name'])
        metrics.append(data.json()['data']['attributes']['working-directory'])
        metrics.append(data.json()['data']['attributes']['resource-count'])
        metrics.append(data.json()['data']
                       ['attributes']['apply-duration-average'])
        metrics.append(data.json()['data']
                       ['attributes']['plan-duration-average'])
        metrics.append(data.json()['data']['attributes']['run-failures'])

        terraform_metrics.append(metrics)

    fields = ['name', 'working_directory', 'resource_count',
              'apply_duration_average', 'plan_duration_average', 'runs_failure']

    with open("data/" + outputName, 'w') as f:
        csv_writer = writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(terraform_metrics)
