"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'Famous First Lines',
            'content': output
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

def select_question( list_of_questions ):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    
    # select random question
    # save text, title, author to session
    
    question_index = random.randint(0, len(list_of_questions)-1 )
    
    session_attributes = list_of_questions[question_index]
    
        
    return session_attributes
    
   
def help_prompt():
    speech_output = "Welcome to the Famous First Lines Trivia. " \
                    "I will read you the first line from a book or poem. " \
                    "Tell me the title and author, and I'll let you know if you got it right. " \
                    "Say repeat to hear the line again, or I don't know to hear the answer. " \
                    "You can say a phrase like The title is A Cat in the Hat, or It is by Doctor Seuss. " \
                    "Or you can answer all at once with a phrase like What is The Little Mermaid by Hans Christian Anderson"
                        
    return speech_output


def next_question(speech_output):

    list_of_questions = [
        {
            "first_line": "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair... ",
            "correct_title": "A Tale of 2 cities",
            "correct_author": "Charles Dickens",
        }, 
        {
            "first_line": "A squat grey building of only 39 floors",
            "correct_title": "Brave New World",
            "correct_author": "Aldous Huxley",
        },
        {
            "first_line": "I felt a Funeral, in my Brain",
            "correct_title": "I felt a Funeral, in my Brain",
            "correct_author": "EMILY DICKINSON",
        },
        {
            "first_line": "Two roads diverged in a yellow wood",
            "correct_title": "The Road Not Taken",
            "correct_author": "ROBERT FROST",
        },
        {
            "first_line": "Mr. and Mrs. Dursley of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much.",
            "correct_title": "Harry Potter and the Sorcerer's Stone",
            "correct_author": "J K Rowling",
        },
        {
            "first_line": "The outlook wasn't brilliant for the Mudville nine that day",
            "correct_title": "Casey at the Bat",
            "correct_author": "Ernest Thayer",
        },
        {
            "first_line": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
            "correct_title": "Pride and Prejudice",
            "correct_author": "Jane Austen",
        },
        {
            "first_line": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. Whenever you feel like criticising any one, he told me, just remember that all the people in this world haven't had the advantages taht you've had.",
            "correct_title": "The Great Gatsby",
            "correct_author": "F Scott Fitzgerald",
        },
        {
            "first_line": "All children, except one, grow up",
            "correct_title": "Peter Pan",
            "correct_author": "J M Barrie",
        },
        {
            "first_line": "Call me Ishmael",
            "correct_title": "Moby Dick",
            "correct_author": "Herman Melville",
        },
        {
            "first_line": "All happy families are alike; each unhappy family is unhappy in its own way",
            "correct_title": "Anna Karenina",
            "correct_author": "Leo Tolstoy",
        },
        {
            "first_line": "It was a bright cold day in April, and the clock were striking thirteen",
            "correct_title": "1984",
            "correct_author": "George Orwell",
        },
        {
            "first_line": "Two households, both alike in dignity, In fair Verona, where we lay our scene, From ancient grudge break to new mutiny, Where civil blood makes civil hands unclean.",
            "correct_title": "Romeo and Juliet",
            "correct_author": "William Shakespeare",
        },
    ]
    
    session_attributes = select_question(list_of_questions)
    should_end_session = False
    
    # read first line text
    speech_output += session_attributes['first_line']
    
    reprompt_text = "What is this from, and who is the author?"
     
    
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
    
def start_over(session, intent):
    return next_question("")
    
def handle_session_end_request():
    speech_output = "Thank you for playing Famous First Lines. " \
                    "We hope that you have a good day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}

def check_answer(response_title, response_author, session):

    correct_title = session['attributes']['correct_title']
    correct_author = session['attributes']['correct_author']
    
    title_is_correct = False
    author_is_correct = False
    
    
    if response_title != None: 
        title_is_correct = correct_title.lower() == response_title.lower()
    if response_author != None:
        author_is_correct = correct_author.lower() == response_author.lower()
    
    session_speech_output = ""
    
    if title_is_correct:
        session_speech_output = "You guessed it was from " + response_title + ". Congratulations, that is correct. "
    elif response_title != None:
        session_speech_output = "You guessed it was from " + response_title + ", but the first line was actually from " + correct_title + ". "
    else:
        session_speech_output = "This line was from " + correct_title + ". "
        
    if author_is_correct:
        session_speech_output += "You guessed the author was " + response_author + ". Congratulations, that is correct. "
    elif response_author != None:
        session_speech_output += "You guessed the author was " + response_author + ", but actually " + correct_author + " wrote " + correct_title + "."
    else:
        session_speech_output += "This line was from " + correct_title + " by " + correct_author + ". "
        
    return session_speech_output
    
def dont_know(intent, session):

    session_attributes = session['attributes']


    response_title = session['attributes'].get('response_title', None)
    response_author = session['attributes'].get('response_author', None)
    
    speech_output = check_answer(response_title, response_author, session)
    should_end_session = True
    reprompt_text = "Say next to get a new line"
                        
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))

    
def repeat_question(intent, session):

    session_attributes = session['attributes']
    should_end_session = False
    
    
    # Repeat first line text if RepeatIntent
    speech_output = session['attributes']['first_line']
    
    reprompt_text = "What is this from, and who is the author?"
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
def help_intent(intent, session):

    session_attributes = session['attributes']
    should_end_session = False
    
    
    # Read help text to user
    speech_output = help_prompt()
    
    if 'first_line' in session_attributes:
        reprompt_text = session_attributes['first_line']
    else:
        reprompt_text = "Say new game to begin playing."
    
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))
        
           

def answer_question(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = session['attributes']
    should_end_session = False

    response_title = session['attributes'].get('response_title', None)
    response_author = session['attributes'].get('response_author', None)
    if 'value' in intent['slots']['Title']:
        response_title = intent['slots']['Title']['value']
        
    if 'value' in intent['slots']['Author']:
        response_author = intent['slots']['Author']['value']
    
    session_attributes['response_title'] = response_title
    session_attributes['response_author'] = response_author
    
    # No author or title
    if response_title == None and response_author == None:
        speech_output = "I did not hear your response. " \
                        "Please say my answer is the Title, by the Author. "
        reprompt_text = "I'm sorry, I still can't hear you. " \
                        "Please say my answer is the Title, by the Author."
    # Author, but no title
    elif response_title == None:
        speech_output = "You said this was from a book by " + response_author + \
                        ". Please say the title is Title."
        reprompt_text = "If you know the title please say " \
                        "The title is Title, if not, say I don't know"
    # Title, but no author
    elif response_author == None:
        speech_output = "You said this was from " + response_title + \
                        ". Please say it is by Author."
        reprompt_text = "If you know the author please say " \
                        "The author is author, if not, say I don't know."
    # Title and author
    else:
        
        speech_output = check_answer(response_title, response_author, session)
        should_end_session = True
        reprompt_text = "Say next to get a new line"
                        
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))


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
    speech_output = "Welcome. I will read you the first line of a book or poem. Tell me the title and author.\n\n "
    # pull in questions
    return next_question(speech_output)

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']                                             
    
    

    # Dispatch to your skill's intent handlers
    if intent_name == "AnswerIntent":
        return answer_question(intent, session)
    elif intent_name == "AMAZON.RepeatIntent":
        return repeat_question(intent, session)
    elif intent_name == "DontKnowIntent":
        return dont_know(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return start_over(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return help_intent(intent, session)
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
    #print("event.session.application.applicationId=" +
    #      event['session']['application']['applicationId'])

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
