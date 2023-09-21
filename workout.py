import csv
import sys
import json

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        sys.exit('Wrong input, please write the name of the file for the Workout Plan')
    elif not sys.argv[1].endswith('csv'):
        sys.exit('File has to be a ".csv"')
    sex = get_sex(input('What gender are you: M or F? '))
    level = get_level(input('Are you a Beginner, Advanced, or Expert? '))
    muscle_group = None
    with open(f'{sys.argv[1]}', 'w', newline='') as file_modified:
        writer = csv.writer(file_modified)
        writer.writerow([f'Sex: {sex.capitalize()}, Level: {level.capitalize()}'])
        writer.writerow(['45 seconds rest between each series'])
        writer.writerow(['1 minute rest between each exercise'])
        writer.writerow([' '])
        while muscle_group != "exit":
            try:
                muscle_group = get_muscle_group(input('What would you like to train: Chest/Shoulders/Back/Legs? '))
            except EOFError:
                break
            if muscle_group != 'exit':
                data = read_data_from_txt("project.txt")
                reach = data[sex.capitalize()][level.capitalize()][muscle_group.capitalize()]
                writer.writerow([f'{muscle_group.capitalize()}'])
                for ele in reach:
                    writer.writerow([f'{ele}: {reach.get(ele)}'])
                writer.writerow([' '])

def get_sex(s):
    s = s.strip().lower()
    if s == 'm' or s == 'f':
        return s
    else:
        raise ValueError('Wrong input. Please write "M" for "Male", or "F" for "Female".')

def get_level(s):
    s = s.strip().lower()
    if s == 'beginner' or s == 'advanced' or s == 'expert':
        return s
    else:
        raise ValueError('Wrong input. Please write "Beginner", "Advanced", or "Expert", depending on your fitness level.')

def get_muscle_group(s):
    s = s.strip().lower()
    if s == 'chest' or s == 'shoulders' or s == 'back' or s == 'legs':
        return s
    else:
        raise ValueError('Wrong input. Please write the muscle group you would like to work out between Chest / Shoulders / Back / Legs.')

def read_data_from_txt(file_path):
    with open(file_path, 'r') as txt_file:
        data = json.loads(txt_file.read())
    return data

if __name__ == '__main__':
    main()
