import json

def write_json_calendar(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["calendar"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def add_to_calendar(title, date):
    new_item = {
        'title': title,
        'date': date
    }
    write_json_calendar(new_item)

if __name__ == '__main__':
    add_to_calendar('test calendar event', 'october 1 2023')
