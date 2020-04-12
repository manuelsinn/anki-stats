import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# ----------------------------------------------------

deck = "Chinese" # This is my top level deck and includes several lower level ones


def get_mature_cards():
    print('Calculating amount of learned words...')
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('interval') >= 21: # A mature card is one that has an interval of 21 days or greater (https://apps.ankiweb.net/docs/manual.html#types-of-cards)
            amount += 1
    return amount

def today_reps():
    print('Calculating todays reps...')
    cards = invoke('findCards', query='rated:1')
    return len(cards)

def week_reps():
    print('Calculating this weeks reps...')
    cards = invoke('findCards', query='rated:7')
    return len(cards)

def streak():
    streak = 29
    days_ago = 29
    while len(invoke('findCards', query='rated:' + str(days_ago) + ' -rated:' + str(days_ago - 1))) > 0:     # checking if cards were seen days_ago days ago
        days_ago += 1
        streak += 1
        print(days_ago)
    return streak

# def minutes_studied_today():

# def days_studied_this_month():  


print('Calculating stats...')
learned = get_mature_cards()
today_reps = today_reps()
week_reps = week_reps()


print('Number of learned words: {}'.format(learned))
print("Today's reps: {}".format(today_reps))
print("Week's reps: {}".format(week_reps))