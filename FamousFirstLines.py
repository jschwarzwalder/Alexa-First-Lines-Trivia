"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}

def check_answer(response_title, response_author, session):

    correct_title = session['attributes']['correct_title']
    correct_author = session['attributes']['correct_author']
    
    title_is_correct = correct_title == response_title
    author_is_correct = correct_author == response_author
    
    session_speech_output = ""
    
    if title_is_correct:
        session_speech_output = "You guessed it was from " + response_title + ". Congratulations, that is correct".
    elif response_title != None:
        session_speech_output = "You guessed it was from " + response_title + ", but the first line was actually from " + correct_title + ". "
    else:
        session_speech_output = "This line was from " + correct_title + ". "
        
    if author_is_correct:
        session_speech_output = "You guessed the author was " + response_author + ". Congratulations, that is correct".
    elif response_author != None:
        session_speech_output = "You guessed the author was " + response_author + ", but actually " + correct_author + " wrote " + correct_title + "."
    else:
        session_speech_output = "This line was from " + correct_title + " by " + correct_author + ". "
        
    return session_speech_output

def answer_question(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    response_title = session['attributes']['response_title']
    response_author = session['attributes']['response_author']
    if 'Title' in intent['slots']:
        response_title = intent['slots']['Title']['value']
        
    if 'Author' in intent['slots']:
        response_author = intent['slots']['Author']['value']
    
    
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
                        
    
    # No author or title
    if response_title == None and response_author == None:
        speech_output = "I did not hear your response. " \
                        "Please say my answer is the Title, by the Author."
        reprompt_text = "I'm sorry, I still can't hear you. " \
                        "Please say my answer is the Title, by the Author."
    # Author, but no title
    elif response_title == None:
        speech_output = "You said this was from a book by " + response_author + \
                        "Please say the title is Title"
        reprompt_text = "If you know the title please say " \
                        "The title is Title, if not, say I don't know"
    # Title, but no author
    elif response_author == None:
        speech_output = "You said this was from " + response_title + \
                        "Please say it is by Author."
        reprompt_text = "If you know the author please say " \
                        "The author is author, if not, say I don't know."
    # Title and author
    else:
        speech_output = "You said this was from " + response_title + \
                        " by " + response_author ". "
        speech_output += check_answer(response_title, response_author, session)
        should_end_session = True
                        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AnswerIntent":
        return answer_question(intent, session)
    elif intent_name == "RepeatIntent":
        return repeat_question(intent, session)
    elif intent_name == "DontKnowIntent":
        return dont_know(intent, session)
    elif intent_name == "StartOverIntent":
        return start_over(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
