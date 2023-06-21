import spacy
from datetime import date, timedelta
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
        'hi '
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
    #print(my_dict['22'])

    important_words = []
    consecutive_nouns = ''

    do_once = False

    index = 0

    # gather conescutive nouns
    # need to hardcode some special cases such as 'finish' and 'clean' because spacy doesnt recognize it as a verb
    for i in my_dict:
        if index == len(my_dict) - 1:
            if consecutive_nouns != '':
                consecutive_nouns += i + ' '
                important_words.append(consecutive_nouns.strip())
                break

            if my_dict[i] == 'NOUN' or my_dict[i] == 'PRON':
                consecutive_nouns += i + ' '
                important_words.append(consecutive_nouns.strip())
                break

        if (i == 'put' or i == 'add') and not do_once:
            do_once = True
            index += 1
            continue

        if (my_dict[i] == "NOUN" or my_dict[i] == "DET" or my_dict[i] == 'PRON' or my_dict[i] == 'ADP' or my_dict[i] == 'ADJ' or my_dict[i] == 'PROPN' or my_dict[i] == 'NUM') and i != 'finish' and i != 'clean':
            consecutive_nouns += i + ' '
        elif my_dict[i] == "VERB" or i == 'finish' or i == 'clean':
            important_words.append(consecutive_nouns.strip())
            consecutive_nouns = ''
            consecutive_nouns += i + ' '
        else:
            important_words.append(consecutive_nouns.strip())
            consecutive_nouns = ''
        
        index += 1
    
    important_words_stripped = []

    # remove blank indexes
    for i in important_words:
        if i != '':
            important_words_stripped.append(i)

    for i in range(0, len(important_words_stripped)):
        if 'do list' in important_words_stripped[i]:
            del important_words_stripped[i]
            break

    #print(important_words_stripped)

    unimportant_words = [
        ' a ', 'a ', ' it ', ' i ', 'i ', 'have ', 'have', ' an '
    ]
    # remove unnecessary words like 'have', 'a' or 'it
    for i in range(len(important_words_stripped)):
        for j in unimportant_words:
            if j in important_words_stripped[i]:
                new_string = important_words_stripped[i].replace(j, '')
                important_words_stripped[i] = new_string

    #print(important_words_stripped)
    #print(my_dict['clean'])
    #print(my_dict['house'])
    # remove accidental words being added as tasks, such as ['days from', 'it in my']
    for i in range(len(important_words_stripped)):
        noun_count = 0
        propn_count = 0
        verb_count = 0
        num_count = 0
        split_string = important_words_stripped[i].split()
        if len(split_string) == 1:
            important_words_stripped[i] = ''
        else:
            for j in split_string:
                if my_dict[j] == 'NOUN':
                    noun_count += 1
                if my_dict[j] == "PROPN":
                    propn_count += 1
                if my_dict[j] == "VERB":
                    verb_count += 1
                if my_dict[j] == 'NUM':
                    num_count += 1

            if (noun_count < 2 and propn_count < 2 and verb_count < 1 and num_count < 1 and (noun_count != 1 and propn_count != 1)):
                important_words_stripped[i] = ''

    for i in range(len(important_words_stripped)):
        split_string = important_words_stripped[i].split()
        for j in range(len(split_string)):
            if split_string[j] == 'tomorrow':
                tmrw = str(date.today() + timedelta(days=1))
                important_words_stripped[i] = important_words_stripped[i].replace('tomorrow', 'on ' + convert_datenum_to_word(tmrw))

    # remove blank indexes again
    important_words_stripped2 = []

    for i in important_words_stripped:
        if i != '':
            important_words_stripped2.append(i)
    
    #print(important_words_stripped)

    return important_words_stripped2

def convert_datenum_to_word(thedate):
    months = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }

    nums = thedate.split('-')

    return months[nums[1]] + ' ' + str(nums[2]) + ', ' + nums[0]

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
