import base64
import requests
import json

def getProjectKey():
    return "TT"

def getMyAccountId():
    return sendGet("api/3/myself").json()["accountId"]

def getIssueId(issueType):
    retVal = 0
    if issueType.lower() == "bug" :
        retVal = 10005
    elif issueType.lower() == "bug":
        retVal = 10004
    elif issueType.lower() == "improvement":
        retVal = 10001
    elif issueType.lower() == "epic":
        retVal = 10000
    elif issueType.lower() == "task":
        retVal = 10002
    
    return retVal

def getTransitionId(issueNumber, transitionName):
    response = sendGet(f"api/3/issue/DOG-{issueNumber}/transitions").json()
    for t in response["transitions"]:
        if t["name"].lower() == transitionName:
            return t["id"]
    return -1

def sendPost(api_url, payload):
    base_url = "https://fivestack.atlassian.net/rest/"

    auth = 'askjira@tutanota.com:OaWlwFsvazOq3KeqcLNbBB62'.encode('ascii')
    
    headers = {
        "Authorization": f"Basic {base64.b64encode(auth).decode('ascii')}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    return requests.post(
        url=base_url + api_url,
        data=payload,
        headers=headers
    )

def sendGet(api_url, query = None):
    base_url = "https://fivestack.atlassian.net/rest/"

    auth = 'askjira@tutanota.com:OaWlwFsvazOq3KeqcLNbBB62'.encode('ascii')
    
    headers = {
        "Authorization" : f"Basic {base64.b64encode(auth).decode('ascii')}"
    }
    if query == None:
        return requests.request("GET", base_url+api_url, headers=headers)
    else:
        return requests.request("GET", base_url+api_url, headers=headers, params=query)

def getMyIssues(date = None):
    api_url = "api/3/search"
    if date == None:
        jql = {"jql": "assignee=CurrentUser() AND project="+getProjectKey(), "fields":"summary, duedate, issuetype"}
    else:
        jql = {"jql": "assignee=CurrentUser() AND project="+getProjectKey()+" AND due>startOfWeek() AND due<endOfWeek()", "fields":"summary, duedate, issuetype"}
    jiraResponse = sendGet(api_url, jql)
    issues = json.loads(jiraResponse.content)
    return issues['issues']


def getMyNumberOfIssues(date = None):
    api_url = "api/3/search"
    if date == None:
        jql = {"jql": "assignee=CurrentUser() AND project="+getProjectKey(), "fields":"summary, duedate"}
    else:
        jql = {"jql": "assignee=CurrentUser() AND project="+getProjectKey()+" AND due>startOfWeek() AND due<endOfWeek()", "fields":"summary, duedate"}
    jiraResponse = sendGet(api_url, jql)
    data = json.loads(jiraResponse.content)
    return data["total"]

def createIssue(projectKey, issueType, summary, description):
    payload = json.dumps({
        "update": {},
        "fields": {
            "summary": summary,
            "issuetype": {
                "id": getIssueId(issueType)
            },
            "project": {
                "key": projectKey
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": description,
                                    "type": "text"
                                }
                            ]
                        }
                ]
            }
        }
    })
    
    jiraResponse = sendPost("api/3/issue", payload)
    
    return jiraResponse.json()['key']


def createMeIssue(projectKey, issueType, summary, description):
    payload = json.dumps({
        "update": {},
        "fields": {
            "summary": summary,
            "issuetype": {
                "id": getIssueId(issueType)
            },
            "project": {
                "key": projectKey
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": description,
                                    "type": "text"
                                }
                            ]
                        }
                ]
            },
            "assignee": {
              "id": getMyAccountId()
            }
        }
    })
    
    jiraResponse = sendPost("api/3/issue", payload)
    
    return jiraResponse.json()['key']


def transitionIssue(issueNumber, issueTransition):
    tId = getTransitionId(issueNumber, issueTransition)

    payload = json.dumps({
        "transition": {
            "id": tId
        }
    })

    if tId != -1:
        jiraResponse = sendPost(
            f"/api/3/issue/DOG-{issueNumber}/transitions", payload)
        return True
    else:
        return False
