def remove_last_and(text):
    '''
    this function removes trailing 'and's
    '''
    words = text.split()

    if words[-1] == 'and':
        del words[-1]

    new_text = ''
    
    for i in words:
        new_text += i + ' '

    return new_text

def parse_todo_list(message):
    words = message.split()

    for i in words:
        i = i.lower()

    task_words = [
        'make', 'create', 'prepare', 'bake', 'cook', 'assemble', 'construct', 'design', 'develop',
        'buy', 'purchase', 'get', 'acquire', 'obtain', 'procure',
        'do', 'perform', 'execute', 'accomplish', 'complete', 'finish',
        'organize', 'sort', 'arrange', 'tidy', 'clean',
        'read', 'study', 'learn', 'research',
        'write', 'compose', 'draft', 'edit',
        'call', 'contact', 'reach out to',
        'attend', 'participate in', 'join',
        'exercise', 'work out', 'train',
        'visit', 'explore', 'tour',
        'watch', 'view', 'stream',
        'listen to', 'play', 'practice',
        'schedule', 'plan', 'arrange',
        'review', 'evaluate', 'assess',
        'submit', 'send', 'deliver'
    ]

    create_words = ['create', 'make', 'set', 'add']

    todo_list = []
    
    for i in range(len(words)):
        if words[i] in task_words:
            task_index = i
            task_word = words[task_index]
            task = ''

            for j in range(task_index + 1, len(words)):
                if words[j] in task_words:
                    break
                task += words[j] + ' '

            new_task = remove_last_and(task)
            full_task = task_word + ' ' + new_task
            full_task = full_task.replace(',', '')

            # don't add the 'create to-do list' to the todo list
            if 'todo' not in new_task and 'to-do' not in new_task and 'to do' not in new_task:
                todo_list.append(full_task.strip())
            else:
                if len(todo_list) < 1:
                    continue
                for j in create_words:
                    if j not in new_task:
                        temp = full_task.split()
                        for k in range(len(temp)):
                            if temp[k] == 'to' and ((temp[k + 1] == 'todo' or temp[k + 1] == 'to-do' or temp[k + 1] == 'to do') or (temp[k + 1] == 'my') or (temp [k + 1] == 'the')):
                                for l in range(len(temp)):
                                    if len(temp) - l <= 4:
                                        if temp[l] == 'to' or temp[l] == 'todo' or temp[l] == 'to-do' or temp[l] == 'to do' or temp[l] == 'list' or temp[l] == 'my' or temp[l] == 'the':
                                            temp[l] = temp[l].replace(temp[l], '')
                        
                        new_full_task = ''
                        for k in temp:
                            new_full_task += ' ' + k + ' '
                        todo_list.append(new_full_task.strip())
                        break
            full_task = ''

    return todo_list

def parse_calendar_event(message):
    words = message.split()
    for i in words:
        i = i.lower()

    event_and_date = [] # event name is index 0, date is index 1

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'may', 'june', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec']

    # example input: add dentist appointment to my calendar on july 22nd
    # example input: create new event on july 22nd for dentist appointment - need to implement this
    for i in range(len(words)):
        if words[i] == 'add':
            first_index = i + 1
        elif words[i] == 'to':
            second_index = i
        elif words[i] in months:
            month = words[i] + ' ' + words[i + 1]
            if words[i + 2] == 'for':
                event_and_date.append(' '.join(words[i + 3:]).strip())
                event_and_date.append(month.strip())
                return event_and_date

    event_and_date.append(' '.join(words[first_index:second_index]).strip())
    event_and_date.append(month.strip())
    return event_and_date

if __name__ == "__main__":
    sentence = input('enter something: ')
    test = parse_calendar_event(sentence)
    print(test[0])
    print(test[1])
    #print(parse_calendar_event(sentence))
    #print(parse_todo_list(sentence))
