# my-tempo
An Alexa Skill that integrates with Tempo/Jira

**Motivation:**
We understand that sometimes the benefits of time tracking come at the cost of the developer/employee. This means breaking focus or the zen of coding to log time/work and can be frustrating. Our goal was to create a tool that takes the hassle out of time/work tracking and management by using voice commands that feel more like a conversation. My-Tempo, a jira/tempo/alexa integration, provide users a headache free way of tracking time & logging work. The use of voice as a medium for this task is invasive when users are focusing on completing work and allows users to mulitask with a costing context switch.

We wanted to use Alexa Skill Kit for a few reasons. 
1. It was a an opportunity to learn a new tool that was well documented and mature (~6 years old).
2. The Alexa SKill Market place is a thriving ecosystem if we wanted to publish the skill.
3. By the end of 2020, Amazon held the largest market share of smart speakers [globaly](https://www.statista.com/statistics/792604/worldwide-smart-speaker-market-share/).

**Supported Scenarios**
_Jira features_
List Issues
Move Issues
Create Issues
Assign Issues
_Tempo features_
Create Worklogs
Create Planned Work
Submit Timesheets

**Sample Dialog:**

    User: Alexa open my tempo
    User: create an issue
    Alexa: What type of issue should I create?
    User: a bug
    Alexa: Can you give me a summary of the bug ?
    User: http call to dependent service is not working
    Alexa: Describe the bug for me.
    User: http request not returning a proper request format, we need to investigate the change log on our dependent service
    Alexa: I created TT-12 for you.

**How to use:**
    
    invocation name: my tempo
    
    alexa, ask my tempo ___
    
**Examples:**
                    
    "what are my issues for {date}",
    "Plan {minutes} minutes of work on issue {issueNumber} {date}
    "move issue {issueNumber} to {issueTransition}"

To see the full list of commands, check out the build.json


