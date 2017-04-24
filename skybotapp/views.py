import json
import requests
from pprint import pprint
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from wit import Wit
from django.views import generic
from django.http.response import HttpResponse
from django.template.context_processors import request
import copy
# Create your views here.

def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAASfh0TDd8cBAHBMfkWQGAexatTOup01lZCXtUJ5CF5Imr5b7MeQu30v6TnEzQmvoJF9MZBzkoZBdhLaVcCSY2BtPivUNJh7pic5vfEA13qDr3TRQLuHn8aKpKZAip4X2QHqhBTa7XQNGPnII1cqNMP46gAaRYMzHHSnZA4NZCAwZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def send(request, response):
    text = str(response['text'])
    text = text[:-1]
    text = text[2:]
    post_facebook_message(request['session_id'],text)     

def receiveAction(request):
    pprint('RECEIVED FROM USER',request['text'])



actions = {'send':send,
           'receiveAction':receiveAction
           }      

client = Wit(access_token='KVCNXSS7SD5RENA5PQ6QBS242ETDIBHC', actions=actions)




def witConnect(incoming_message):  
    try:
        resp = client.message(incoming_message)
        pprint('Yay, got Wit.ai response: ' + str(resp))
        if 'reset' in resp['entities']:
            for i in range(0,3):
                array[i] = 'j'
         
        return resp
    except:
        pprint('WIT.AI ERROR')
    
#KVCNXSS7SD5RENA5PQ6QBS242ETDIBHC
#turgut DJE4HFOBMAJO6DMIC2IEZRP5DDRQRZKS    


class SkyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '93985762':
           return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal

               
                    if message['sender']['id'] != '1884352301811482':
                        try:
                            pprint('THE MESSAGE POSTED TO WITCONNECT FUNCTION : ' + str(message))
                            resp=witConnect(message['message']['text'])
                            strResp = parseWitData(resp)
                            check = checkArray(array)
                            if check == 1:
                                client.run_actions(message['sender']['id'], message['message']['text'])
                            else:
                                post_facebook_message(message['sender']['id'],str(strResp))     
                                for i in range(0,3):
                                      array[i] = 'j'
                                
                        except:
                            pprint('hata hello')             
        return HttpResponse()

array = ['j','j','j','j']


    
def parseWitData(witOut):
        lent = 0
        if 'location' in witOut['entities']:
            lent = len(witOut['entities']['location'])
            if array[0] == 'j':
                if lent == 2:
                   array[0] = str(witOut['entities']['location'][0]['value'])
                   array[1] = str(witOut['entities']['location'][1]['value'])
                elif lent ==1:
                   array[0] = str(witOut['entities']['location'][0]['value'])
            else:
                array[1] = str(witOut['entities']['location'][0]['value'])
        if 'datetime' in witOut['entities']:
            #if 'to' in  witOut['entities']['datetime']['values'][0]:
            lent = len(witOut['entities']['datetime']['values'])
            if lent > 1:
                array[2] = str(witOut['entities']['datetime']['values'][0]['to']['value'])
                array[3] = str(witOut['entities']['datetime']['values'][0]['from']['value'])
            #elif lent ==1:
            else:
                array[2] = str(witOut['entities']['datetime']['values'][0]['value'])
        if array[0] == 'j' :
            return 'Please enter the destination and source'
        if array[1] =='j':
            return 'Please enter the destination'
        if array[2] == 'j':
            return 'Please enter the time you want to fly'
    
        return array
    
                    
                 
def checkArray(array):
    flag = 1
    for i in range(0,3):
        if array[i] != 'j':
            flag = 0
    return flag

    
    
   
    



#message['message']['text']
#resp['entities']['location'][0]['value']

def homeView(request):
    return HttpResponse('Hello')



#actions = {
#    'send': send,
#    'my_action': my_action,
#}
















