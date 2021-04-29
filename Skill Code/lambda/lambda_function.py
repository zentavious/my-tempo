# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
from datetime import datetime
import jiraClient
import tempoClient
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to tempo, how can I assist you today?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetMyIssuesIntentHandler(AbstractRequestHandler):
    ""'Handler for get my issues.'""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('GetMyIssuesIntent')(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        date = slots["date"].value
        issues = jiraClient.getMyIssues(date)
        speech_output = "You have "
        counter = 0
        for val in issues:
            summary = val['fields']['summary']
            key = val['key']
            issuetype = val['fields']['issuetype']['name']
            if not id:
                speech_output = "You dont have any issues due"
            else:
                if counter>=1:
                    if counter == len(issues) - 1:
                        speech_output +=". and "
                    else:
                        speech_output +="."
                speech_output += issuetype
                speech_output += f" {key}, "
                speech_output += f"{summary} "
                counter +=1
                
        speech_output += "due today"
            
        return (
            handler_input.response_builder
                .speak(speech_output)
                .response
        )

class GetNumberOfIssuesIntentHandler(AbstractRequestHandler):
    ""'Handler for retreiving # of issues.'""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('GetNumberOfIssuesIntent')(handler_input)
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        date = slots["date"].value
        speech_output = "You have "
        data = jiraClient.getMyNumberOfIssues(date)
        speech_output += f"{data} issues"
        return (
            handler_input.response_builder
                .speak(speech_output+" , if you'd like me to list the issues; please say list all issues")
                .ask("If you'd like me to list the issue names, please say: list issues")
                .response
        )

class SumbitTimeIntentHandler(AbstractRequestHandler):
    """Handler for Sumbit Time Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SubmitTimeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        user = slots["user"].value
        
        success = tempoClient.submitTimesheet()
        speak_output = f"I submitted your timesheet to {user}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CreateIssueIntentHandler(AbstractRequestHandler):
    """Handler for Create Issue Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CreateIssueIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        issueType = slots["issueType"].value
        summary = slots["summary"].value
        description = slots["description"].value
        
        issueKey = jiraClient.createIssue("TT", issueType, summary, description)
        
        speak_output = f"I created {issueKey} for you."
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CreateAssignMeIssueIntentHandler(AbstractRequestHandler):
    """Handler for Create Assign Issue Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CreateAssignMeIssueIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        issueType = slots["issueType"].value
        summary = slots["summary"].value
        description = slots["description"].value
        
        issueKey = jiraClient.createMeIssue("TT", issueType, summary, description)
        
        speak_output = f"I created {issueKey} and assigned it to you."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class TransitionIssueIntentHandler(AbstractRequestHandler):
    """Handler for Create Assign Issue Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TransitionIssueIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        issueNumber = slots["issueNumber"].value
        issueTransition = slots["issueTransition"].value
        
        if jiraClient.transitionIssue(issueNumber, issueTransition):
            speak_output = f"I moved issue {issueNumber} to {issueTransition} for you."
        else:
            speak_output = f"I was not able to move issue {issueNumber} to {issueTransition}."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CreateWorklogIntentHandler(AbstractRequestHandler):
    """Handler for Create Worklog Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CreateWorklogIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        issueNumber = slots["issueNumber"].value
        startDate = slots["startDate"].value
        paddedTime = slots["startTime"].value
        if len(paddedTime) < 5:
            paddedTime = "0" + paddedTime
        startTime = datetime.strptime(paddedTime, '%H:%M').strftime("%H:%M:%S")
        timeSeconds = int(slots["timeMinutes"].value)*60
        billableTimeSeconds = int(slots["billableTimeMinutes"].value)*60
        
        success = tempoClient.addWorklog(issueNumber, startDate, startTime, timeSeconds, billableTimeSeconds)
        if success == True:
            speak_output = f"I logged work against issue {issueNumber} for you."
        else:
            speak_output = str(success)
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CreatePlanIntentHandler(AbstractRequestHandler):
    """Handler for Create Plan Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CreatePlanIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        seconds = int(slots["minutes"].value)*60
        issueNumber = slots["issueNumber"].value
        date = slots["date"].value
        recurrence = slots["recurrence"].value
        
        ret = tempoClient.createPlan(date, "description", seconds, recurrence, issueNumber)
        speak_output = str(ret)#f"I planned that for you"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SumbitTimeIntentHandler())
sb.add_request_handler(GetNumberOfIssuesIntentHandler())
sb.add_request_handler(GetMyIssuesIntentHandler())
sb.add_request_handler(CreateIssueIntentHandler())
sb.add_request_handler(CreateAssignMeIssueIntentHandler())
sb.add_request_handler(TransitionIssueIntentHandler())
sb.add_request_handler(CreateWorklogIntentHandler())
sb.add_request_handler(CreatePlanIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers


sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
