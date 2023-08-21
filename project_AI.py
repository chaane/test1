from cgi import print_directory
from multiprocessing.connection import Listener
from re import T
from unittest import result
from urllib import response
import webbrowser
from datetime import datetime
from logging.config import listen
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha

#configure browser
#QQQAAALLAA
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))

#speech engine installation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)#0=male,1=female
activationWord ='Computer' #single word 
#WOLFRAM ALPHA CONFIGUE
appID='APLETX-5PP9YKVYA5'
wolframclient=wolframalpha.Client(appID)

def speak(text, rate=140):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

#navigating to a website

def parseCommand():
    listener = sr.Recognizer()
    print('Awaiting Command')
    with sr.Microphone() as source:
        listener.pause_threshold=1
        input_speech= listener.listen(source)
    try:
        print('Recognizing speech...')
        query=listener.recognize_google(input_speech,language='en_gb')
        print(f'The input speech was:{query}')
    except Exception as exception:
        print('i do not undertsand')
        speak('i do not understand')
        print(exception)
        return'None'
    return query


def search_wikipedia(query=''):
    searchResults =wikipedia.search(query)
    if not searchResults:
        print('No wiki results')
        return'no results retrieved'
    try:
        wikiPage=wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage =wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary= str(wikiPage.summary)
    return wikiSummary


def listOrDict(var):
    if isinstance(var,list):
        return var[0]['plaintext'] 
    else:
        return var['plainext']  
    
    
def search_wolframalpha(query=''):
    response = wolframclient.query(query)
    if response['@success']=='false':
        return'could not compute'
    else:
        result=''
        #Question
        pod0=response['pod'][0]
        pod1=response['pod'][1]
        # May contain the answer has the higheest confidence value 
        #if its primary or has the title of result or definition then it is the offical result
    if (('result')in pod1['@title'].lower()) or (pod1.get('@primary','false')=='true') or ('definition'in pod1['@title'.lower()]):
        #get result
        result = listOrDict(pod1['subpod'])
        # remove the bracketed section
        return result.split('(')[0]
    else:
        question = listOrDict(pod0['subpod'])
        return question.split('(')[0]
                
    
# main loop 
if __name__=='__main__':
    speak('Good Evening Top G, how may i be of service today.')
    while True:
        #parse Command as list
        query= parseCommand().lower().split()
        if query[0]==activationWord:
            query.pop(0)
            #list command
            if query[0]=='say':
                if 'hello' in query:
                    speak('Greetings top G you look handsom today.')
                else:
                    query.pop(0)#Remove Say
                    speech =' '.join(query)
                    speak(speech)
                    
            # Navigation
            if query[0] == 'go' and query[1]=='to':
                speak('ok top G i got you opening...')
                query=' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
                
            #Wikipedia
            if query[0]=='wikipedia':
                query=' '.join(query[1:])
                speak('Querying the universal databank')
                result = search_wikipedia(query)  
                speak(result)  
            #Wolfram Alpha 
            if query[0]=='compute'or query[0]=='computer':
                query=' '.join(query[1:])
                speak('computing')
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('unable to compute')
        