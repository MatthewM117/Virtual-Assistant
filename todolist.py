import json

def write_json_todolist(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["todolist"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def add_to_todo_list(title, date):
    new_item = {
        'title': title,
        'due_date': date
    }

    write_json_todolist(new_item)
    '''
    todo_list_data = {
        'todolist': [
            {
                'title': new_item,
                'due_date': '2023-01-01'
            },
            {
                'title': 'test todo list item number two',
                'due_date': '2023-01-02'
            }
        ]
    }

    json_string = json.dumps(todo_list_data, indent=4)

    with open('data.json', 'a') as outfile:
        outfile.write(json_string)
    '''

def read_todo_list_data():
    with open('data.json') as json_file:
        data = json.load(json_file)

    return data

def search_todo_list(date):
    todo_list_data = read_todo_list_data()

    return_data = []

    for i in todo_list_data['todolist']:
        if i['due_date'] == date:
            return_data.append(i['title'])
    
    return return_data

if __name__ == '__main__':
    add_to_todo_list('testing appending', 'june 1st 2023')
    #read_todo_list_data()
    
    todo_list_data = read_todo_list_data()
    for i in todo_list_data['todolist']:
        print(i['title'])
    

