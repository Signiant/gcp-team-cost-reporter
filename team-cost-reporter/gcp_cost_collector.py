from google.cloud import bigquery
from google.oauth2 import service_account
from output import getEndDate, getStartDate


def _get_all_project_costs(service_account_file, billing_table, folder_id, start_date, end_date, debug):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
    query = "SELECT cost FROM `" + billing_table + \
            "` WHERE usage_start_time BETWEEN '" + start_date + "' AND '" + end_date + \
            "' AND project.ancestry_numbers LIKE '%" + folder_id + "%'"

    if debug:
        print(query)
    try:
        query_job = client.query(query)
    except Exception as e:
        print(e)
        return 0
    total_cost = 0
    for row in query_job:
        total_cost += row.cost
    return total_cost


def get_all_costs(config_map, debug):
    billing_table = config_map['global']['billing_table']
    service_account_file = config_map['global']['service_account_file']
    start_date = getStartDate(config_map)
    end_date = getEndDate(config_map)
    team_cost = {}

    for team in config_map['teams']:
        team_cost[team['name']] = _get_all_project_costs(service_account_file, billing_table, team['folder_id'],
                                                         start_date, end_date, debug)
    return team_cost
