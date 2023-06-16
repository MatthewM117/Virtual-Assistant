import spacy
model_path = "language_model/en_core_web_sm-3.5.0"
nlp = spacy.load(model_path)

def parse_todo_list2(message):

    message = message.lower()

    possible_todo_list_words = [ # possible combinations of useless words we dont want to look at.
        'on my todo list',
        'on my to do list',
        'on my to-do list',
        'to my todo list',
        'to my to do list',
        'to my to-do list',
        'on todo list',
        'on to do list',
        'on to-do list',
        'to todo list',
        'to to do list',
        'to to-do list',
        'create todo list with',
        'create to-do list with',
        'create to do list with',
        'create todo list',
        'create to-do list',
        'create to do list',
        'on it',
        'hi'
    ]

    for i in possible_todo_list_words:
        if i in message:
            message = message.replace(i, '')
    #print(message)
    doc = nlp(message)

    # Extract tokens and POS tags
    tokens = [token.text for token in doc]
    pos_tags = [token.pos_ for token in doc]

    #print(tokens)
    #print(pos_tags)

    my_dict = {key: value for key, value in zip(tokens, pos_tags)}
    #print(my_dict)

    important_words = []
    consecutive_nouns = ''

    do_once = False

    index = 0

    # gather conescutive nouns
    # need to hardcode some special cases such as 'finish' because spacy doesnt recognize it as a verb
    for i in my_dict:
        if index == len(my_dict) - 1:
            if my_dict[i] == 'NOUN' or my_dict[i] == 'PRON':
                consecutive_nouns += i + ' '
                important_words.append(consecutive_nouns.strip())
                break

        if (i == 'put' or i == 'add') and not do_once:
            do_once = True
            index += 1
            continue

        if (my_dict[i] == "NOUN" or my_dict[i] == "DET" or my_dict[i] == 'PRON' or my_dict[i] == 'ADP' or my_dict[i] == 'ADJ' or my_dict[i] == 'PROPN') and i != 'finish':
            consecutive_nouns += i + ' '
        elif my_dict[i] == "VERB" or i == 'finish':
            important_words.append(consecutive_nouns.strip())
            consecutive_nouns = ''
            consecutive_nouns += i + ' '
        else:
            important_words.append(consecutive_nouns.strip())
            consecutive_nouns = ''

        index += 1

    important_words_stripped = []

    for i in important_words:
        if i != '':
            important_words_stripped.append(i)

    #print(important_words_stripped)
    #print(my_dict['it'])
    return important_words_stripped
    '''
    nouns = []

    for i in range (0, len(pos_tags)):
        if pos_tags[i] == 'NOUN':
            nouns.append(tokens[i])
    
    print(nouns)
    '

    task_phrases = []
    
    for chunk in doc.noun_chunks:
        task_phrases.append(chunk.text)

    print(task_phrases)

    nouns = []

    for i in task_phrases:
        split_i = i.split()
        curr_string = ''
        for j in split_i:
            if my_dict[j] == 'NOUN' or my_dict[j] == 'VERB':
                curr_string += j + ' '
        nouns.append(curr_string.strip())

    print(nouns)
    '''

if __name__ == "__main__":
    #sentence = input('enter something: ')
    #print(parse_todo_list(sentence))

    while True:
        input_text = input('enter something: ')
        if input_text == 'q':
            break
        #input_text = 'please add dentist appointment, fix ship, finish letter, to my todo list thanks'
        #input_text = 'Please buy milk and eggs, and also complete the homework assignment.'
        print(parse_todo_list2(input_text))
