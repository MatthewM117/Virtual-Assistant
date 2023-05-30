import spacy

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

def parse_calendar_message(text):
    doc = nlp(text)

    event = None
    date = None

    for i in range(len(doc)):
        if doc[i].dep_ == "dobj" and doc[i].head.pos_ == "VERB":
            event = ''.join(doc[find_index(text):i+1].text)
        if doc[i].ent_type_ == "DATE":
            date = doc[i-1].text + ' ' + doc[i].text

    if event and date:
        print("Event:", event)
        print("Date:", date)
    else:
        print("Unable to extract event and date.")

text = input("enter something: ")
parse_calendar_message(text)
