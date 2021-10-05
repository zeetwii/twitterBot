import time # needed for sleep

import tweepy # needed for twitter API
import yaml # needed for config


class ReplyBot:
    """
    Simple python bot to listen to and auto reply to twitter events
    """
    
    def __init__(self, apiKey, apiSecret, accessToken, accessTokenSecret):
        """
        Init method

        Args:
            apiKey ([type]): The API Key to use
            apiSecret ([type]): The API secret to use
            accessToken ([type]): The access token to use
            accessTokenSecret ([type]): The access token secret to use
        """
                 
        self.auth = tweepy.OAuthHandler(apiKey, apiSecret)
        self.auth.set_access_token(accessToken, accessTokenSecret)

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

        self.prevMsgs = []

        try:
            self.api.verify_credentials()
            self.id = str(self.api.verify_credentials().id)
            self.name = self.api.verify_credentials().name
            print(f"Credentials loaded, running as: {self.name}")
        except:
            print("Error, credentials not valid")

    def dmThread(self):
        print("Starting DM Reader Thread, press Ctrl + C to exit")

        while True:
            try:
                print('Scanning...')
                self.dmRead()
                time.sleep(60)
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                break


    def dmRead(self):

        messageList = self.api.get_direct_messages()
        newIDs = []
        repeatCount = 0

        print("")
        print(f"{str(len(messageList))} messages recieved since last scan:")

        for msg in messageList:
            print('')
            newIDs.append(msg.id)
            #print(str(msg.message_create))
            #self.api.delete_direct_message(msg.id)
            time.sleep(1)
            if msg.id not in self.prevMsgs:
                if msg.message_create['sender_id'] == self.id : # check to see if DM is from us
                    print("its me")
                    # Go ahead and delete the message, we don't care about our messages  
                else:
                    print("not me")
                    #print(str(msg.message_create))
                    try:
                        print(str(msg.message_create['message_data']['quick_reply_response']['metadata']))
                        self.api.send_direct_message(msg.message_create['sender_id'], f"Thank you for selecting option {str(msg.message_create['message_data']['quick_reply_response']['metadata'])}")
                        time.sleep(1)
                    except KeyError:
                        print("not a quick repsonse, sending starting message")

                        options = [
                            {
                            "label": "I'm good",
                            "description": "It means you're doing good",
                            "metadata": "1"
                            },
                            {
                            "label": "Not so good",
                            "description": "It means you're not doing good",
                            "metadata": "2"
                            }
                        ]
                        
                        self.api.send_direct_message(msg.message_create['sender_id'], "Quick reply Test", quick_reply_options=options)
                        time.sleep(1)
                self.api.delete_direct_message(msg.id)
                time.sleep(1)
            else:
                repeatCount = repeatCount + 1
            
        self.prevMsgs = newIDs
        print(f"{str(repeatCount)} messages repeated")

if __name__ == "__main__":
    
    print("Welcome to ReplyBot, a simple twitter bot to monitor an account and auto reply")
    
    with open("config.yml", "r") as ymlfile:
        CFG = yaml.safe_load(ymlfile)
        apiKey = CFG["twitter"]["API_key"]
        apiSecret = CFG["twitter"]["API_secret"]
        accessToken = CFG["twitter"]["access_token"]
        accessTokenSecret = CFG["twitter"]["access_token_secret"] 
    
    replyBot = ReplyBot(apiKey, apiSecret, accessToken, accessTokenSecret)
        
    replyBot.dmThread()