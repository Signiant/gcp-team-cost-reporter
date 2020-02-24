import json
import mail
import datetime
import os


def getToAddr(team_name, config_map):
    to_addr = ""
    # Find our team info in the config file
    for team in config_map['teams']:
        if team['name'] == team_name:
            to_addr = team['email']
    return to_addr


def getEndDate(config_map):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def getStartDate(config_map):
    number_of_days = config_map['global']['days_to_report']
    now = datetime.datetime.now()
    n_days_ago = now - datetime.timedelta(days=number_of_days)
    return n_days_ago.strftime("%Y-%m-%d")


def writeTeamCosts(team_name, config_map, team_results, debug):
    output_folder = "/output/"
    output_filename = output_folder + team_name + ".json"
    # Add the start and end dates to the raw output
    stored_results = {}
    stored_results['team'] = team_name
    stored_results['cost'] = team_results
    stored_results['start'] = getStartDate(config_map)
    stored_results['end'] = getEndDate(config_map)
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    # Write the file
    if debug:
        print("Writing raw team costs to %s for team %s" % (output_filename, team_name))
    target = open(output_filename, 'w')
    json.dump(stored_results, target)
    target.close()


def outputResults(team_name, config_map, team_results, debug):
    # Get the SMTP config
    smtp_server = config_map['global']['smtp']['server']
    smtp_tls = config_map['global']['smtp']['tls']
    smtp_port = config_map['global']['smtp']['port']
    smtp_user = config_map['global']['smtp']['user']
    smtp_pass = config_map['global']['smtp']['password']
    smtp_from = config_map['global']['smtp']['from_addr']
    smtp_cc = config_map['global']['smtp']['cc_addrs']
    email_template_file = config_map['global']['smtp']['template']
    email_to_addr = getToAddr(team_name, config_map)
    email_subject = "Team %s GCP Cost Report for %s to %s" % (team_name, getStartDate(config_map), getEndDate(config_map))
    if debug:
        print("Sending email to %s for team %s" % (email_to_addr, team_name))
    values = {}
    values['teamName'] = team_name
    values['startDate'] = getStartDate(config_map)
    values['endDate'] = getEndDate(config_map)
    values['reportGenerationDate'] = datetime.datetime.now().strftime("%Y-%m-%d")
    values['totalCost'] = "{0:.2f}".format(team_results)
    template = mail.EmailTemplate(template_name=email_template_file, values=values)
    server = mail.MailServer(server_name=smtp_server, username=smtp_user, password=smtp_pass, port=smtp_port, require_starttls=smtp_tls)
    msg = mail.MailMessage(from_email=smtp_from, to_emails=[email_to_addr], cc_emails=smtp_cc, subject=email_subject, template=template)
    mail.send(mail_msg=msg, mail_server=server)
    # Write the output to disk so other scripts can use it
    writeTeamCosts(team_name, config_map, team_results, debug)
