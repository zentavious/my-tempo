# my-tempo
An Alexa Skill that integrates with Tempo/Jira

With the end of every work day comes making sure you properly fill your worklog out. Now whether this was done through keeping notes on the side, or by breaking coding zens and making sure to fill out your issues/tickets as you work. It's always a hassle. I think alot of developers can relate to this issue, and so we developed myTempo. A jira-tempo-alexa integration(say that s3 times fast) to provide developers a headache free, way of tracking time & logging work. 

Sample Scenario:

    User: my tempo
    User: create issue
    Alexa: What type of issue should I create?
    User: bug
    Alexa: Can you give me a summary of the bug ?
    User: call not working
    Alexa: Describe the bug for me.
    User: http request not returning a proper request
    Alexa: I created TT-12 for you.

How to use:
    
    invocation name: my tempo
    
  samples
                    
    "what are my issues for {date}",
    "Plan {minutes} minutes of work on issue {issueNumber} {date}
    "move issue {issueNumber} to {issueTransition}"

To see the full list of commands, check out the build.json


