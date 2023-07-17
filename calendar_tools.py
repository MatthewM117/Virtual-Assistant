import json

def write_json_calendar(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["calendar"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def add_to_calendar(title, date):
    new_item = {
        'title': title,
        'date': date
    }
    write_json_calendar(new_item)

if __name__ == '__main__':
    add_to_calendar('test calendar event', 'october 1 2023')
