# calendar_utils also means schedule

import spacy
from datetime import date, timedelta
from word2number import w2n

model_path = "language_model/en_core_web_sm-3.5.0"
nlp = spacy.load(model_path)

def find_index(thetext):
    '''
    finds the first index of the beginning of the event
    '''
    text = thetext.split()

    for i in range(len(text)):
        print(text[i])
        if text[i] == 'add':
            return i + 1
        
    return 0

def get_numbered_date(date_text):
    '''
    convert a date, e.g march sixth or march 6, to 2023-03-06
    '''
    MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 2, 'december': 12}
    word_nums = date_text.split()
    if len(word_nums) == 2:
        month = word_nums[0]
        if month in MONTHS:
            month_num = MONTHS[month]
        day = word_nums[1]
        print(day)
        return 'day: ' + str(w2n.word_to_num(day)) + ' month: ' + str(month_num)

def parse_calendar_message(text):
    '''
    returns array where index 0 is the event name, index 1 is the date and index 2 is the time range
    '''
    doc = nlp(text)

    event = None
    the_date = None
    time_range = None

    event_and_date = []

    for i in range(len(doc)):
        if doc[i].dep_ == "dobj" and doc[i].head.pos_ == "VERB":
            event = ''.join(doc[find_index(text):i+1].text)
        if doc[i].ent_type_ == "DATE":
            if 'pm' not in (doc[i-1].text + ' ' + doc[i].text) and 'from' not in (doc[i-1].text + ' ' + doc[i].text) and '-' not in (doc[i-1].text + ' ' + doc[i].text) and 'am' not in (doc[i-1].text + ' ' + doc[i].text):
                the_date = doc[i-1].text + ' ' + doc[i].text
        if i < len(doc) - 1:
            if doc[i].pos_ == "NUM" and (doc[i+1].text == '-' or doc[i+1].text == 'to'):
                start_time = doc[i].text
                end_time = doc[i+2].text
                time_range = start_time + '-' + end_time

    if event:
        event_and_date.append(event)
    else:
        event_and_date.append('unable to extract event')

    if the_date:
        event_and_date.append(the_date)
        if 'tomorrow' in the_date:
            del event_and_date[1]
            tmrw = date.today() + timedelta(days=1)
            the_date = 'tomorrow, ' + str(tmrw)
            event_and_date.append(the_date)
    else:
        event_and_date.append('unable to extract date')

    if time_range:
        event_and_date.append(time_range)
    else:
        event_and_date.append('unable to extract time range')

    return event_and_date

def check_if_month(word):
    months = [
        'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
        'december', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sept', 'aug', 'oct', 'nov', 'dec'
    ]

    if word in months:
        return True
    return False

def is_number(num):
    return int(num)

def parse_calendar_message2(text):
    useless_words = [
        'to my calendar',
        'my calendar'
    ]

    for i in useless_words:
        if i in text:
            text = text.replace(i, '')

    doc = nlp(text)

    # Extract tokens and POS tags
    tokens = [token.text for token in doc]
    pos_tags = [token.pos_ for token in doc]

    my_dict = {key: value for key, value in zip(tokens, pos_tags)}

    events = []
    date = []
    consecutive_nouns = ''

    for i in my_dict:
        if my_dict[i] == 'NOUN':
            consecutive_nouns += i + ' '
        elif my_dict[i] == 'PROPN':
            if check_if_month(i):
                date.append(i)
        else:
            events.append(consecutive_nouns.strip())
            consecutive_nouns = ''

    #print(my_dict['jul'])
    print(events)
    print(date)


if __name__ == '__main__':
    while True:
        text = input("enter something: ")
        if text == 'q':
            break
        parse_calendar_message2(text)
    '''
    res = parse_calendar_message(text)
    print (res[0], ' ', res[1], ' ', res[2])
    print(get_numbered_date(res[1]))
    '''
    