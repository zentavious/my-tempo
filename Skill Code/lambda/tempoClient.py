import base64
import requests
import json
import logging

import jiraClient

def postTempo(api_url, payload, params=None):
    base_url = "https://api.tempo.io/core/3/"

    headers = {
        "Authorization": "Bearer TKdXnm461oIv3jHzjo70Bx9yVqnJZv ",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if params == None:
        return requests.post(
            url=base_url + api_url,
            data=payload,
            headers=headers
        )
    else:
        return requests.post(
            url=base_url + api_url,
            data=payload,
            headers=headers,
            params=params
        )

def addWorklog(issueNumber, startDate, startTime, timeSpentSeconds, billableSeconds):
    payload = json.dumps({
        "issueKey": f"TT-{issueNumber}",
        "timeSpentSeconds": timeSpentSeconds,
        "billableSeconds": billableSeconds,
        "startDate": startDate,
        "startTime": startTime,
        "authorAccountId": jiraClient.getMyAccountId()
    })
    response = postTempo("worklogs", payload)
    try:
        response.json()["tempoWorklogId"]
        return True
    except:
        return response.json()

def submitTimesheet(comment=None):
    if comment == None:
        comment = "Please review my timesheet"

    payload = json.dumps({
        "comment": comment,
        "reviewerAccountId": "557058:190b17bf-8b2a-4db4-9d03-1df6797ca9bf"
    })

    params = {"from": "2021-04-01", "to": "2021-04-30"}
    return postTempo(f"timesheet-approvals/user/{jiraClient.getMyAccountId()}/submit", payload, params=params).json()

def createPlan(date, description, plannedSeconds, rule, issueNumber):
    payload = json.dumps({
        "startDate": date,
        "endDate": date,
        "description": description,
        "plannedPerDaySeconds": plannedSeconds,
        "includeNonWorkingDays": False,
        "rule": rule,
        "accountId": jiraClient.getMyAccountId(),
        "issueKey": f"TT-{issueNumber}"
    })

    return postTempo("plans", payload).json()

