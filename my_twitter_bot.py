import tweepy
import time


CONSUMER_KEY = '##################'
CONSUMER_SECRET = '##################'
ACCESS_KEY = '##################'
ACCESS_SECRET = '##################'
print('This is my twitter bot')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
DMS = api.direct_messages(count=50)

FILE_NAME = 'last_seen_id.txt'
DM_FILE_NAME = 'Last_seen_dm_id.txt'
INDICES_FILE_NAME = 'Last_seen_indices.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = f_read.read().strip()
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_dms():
    print('Retrieving and replying to direct messages', flush = True)
    # Sender_id: 1059343017998516224
    Last_seen_dm_id = retrieve_last_seen_id(DM_FILE_NAME)
    Last_seen_indices = retrieve_last_seen_id(INDICES_FILE_NAME)
    models = {
        "iphone 5": "$55",
        "iphone 5s": "$55",
        "iphone 5c": "$55",
        "iphone 6": "$65",
        "iphone 6 Plus": "$65",
        "iphone6s": "$70",
        "iphone6s Plus": "$70",
        "iphone 7": "$80",
        "iphone 7 Plus": "$85",
        "iphone 8": "$90",
        "iphone 8 Plus": "$95"
    }
    DMS = api.direct_messages(count=50)
    for DM in reversed(DMS):
        LengthOfDm= len(DM.events)
        print(LengthOfDm, flush = True)
        for i in range(int(Last_seen_indices), LengthOfDm -1):
            Message_Data = DM.events[i]['message_create']['message_data']
            recipient_id = DM.events[i]['message_create']['target']['recipient_id']
            Sender_ID = DM.events[i]['message_create']['sender_id']
            DM_ID = DM.events[i]['id']
            if Sender_ID != '1059343017998516224' and int(DM_ID) > int(Last_seen_dm_id):
                for k,v in models.items():
                    if k in Message_Data['text'].lower():
                        print(Message_Data['text'] + 'Right here right here2 ' +  Sender_ID + ' ' + DM_ID , flush = True)
                        text_string =  ' The Cost of repairing an ' + k + " is " + v
                        event = {
                          "event": {
                            "type": "message_create",
                            "message_create": {
                              "target": {
                                "recipient_id": Sender_ID
                              },
                              "message_data": {
                                "text": str(text_string)
                              }
                            }
                          }
                        }
                        api.send_direct_message_new(event)
        Last_seen_dm_id = DM.events[LengthOfDm - 1]['id']
        store_last_seen_id(Last_seen_dm_id, DM_FILE_NAME)
        store_last_seen_id(LengthOfDm-1, INDICES_FILE_NAME)

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    models = {
        "iphone 5": "$55",
        "iphone 5s": "$55",
        "iphone 5c": "$55",
        "iphone 6": "$65",
        "iphone 6 Plus": "$65",
        "iphone6s": "$70",
        "iphone6s Plus": "$70",
        "iphone 7": "$80",
        "iphone 7 Plus": "$85",
        "iphone 8": "$90",
        "iphone 8 Plus": "$95"
    }
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name +
                    '#HelloWorld back to you!', mention.id)
        for k,v in models.items():
            print(str(mention.id) + ' - ' + mention.full_text, flush=True)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
            if k in mention.full_text.lower():
                print('keywords', flush=True)
                print('responding back...', flush=True)
                api.update_status('@' + mention.user.screen_name +
                    ' The Cost of repairing an ' + k + " is " + v , mention.id)

while True:
    reply_to_tweets()
    reply_to_dms()
    time.sleep(300)
