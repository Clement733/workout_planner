import streamlit as st
import csv
import sys
import os
import json

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

def get_number_of_days(s):
    s = s.strip().lower()
    if s == "1 day" or s == "2 days" or s == "3 days" or s == "4 days" or s == "5 days" or s == "6 days":
        return s
    else:
        raise ValueError("Wrong input. Please input the number of days you'd like to workout.")

def read_data_from_txt(file_path):
    with open(file_path, 'r') as txt_file:
        data = json.loads(txt_file.read())
    return data

def generate_workout_plan_custom(file_name, sex, level, muscle_group):
    with open(file_name, 'a', newline='') as file_modified:
        writer = csv.writer(file_modified)
        if file_modified.tell() == 0:
            writer.writerow([f'Sex: {sex.capitalize()}, Level: {level.capitalize()}'])
            writer.writerow(['45 seconds rest between each series'])
            writer.writerow(['1 minute rest between each exercise'])
            writer.writerow([' '])

        data = read_data_from_txt("program-custom.txt")
        reach = data[sex.capitalize()][level.capitalize()][muscle_group.capitalize()]
        writer.writerow([f'{muscle_group.capitalize()}'])
        for ele in reach:
            writer.writerow([f'{ele}: {reach.get(ele)}'])
        writer.writerow([' '])

def generate_workout_plan_default(file_name, number_of_days, sex, level):
    with open(file_name, 'a', newline='') as file_modified:
        writer = csv.writer(file_modified)
        if file_modified.tell() == 0:
            writer.writerow([f'Sex: {sex.capitalize()}, Level: {level.capitalize()}, Number of days: {number_of_days.capitalize()}'])
            writer.writerow(['45 seconds rest between each series'])
            writer.writerow(['1 minute rest between each exercise'])
            writer.writerow([' '])

        data = read_data_from_txt('program-default.txt')
        reach = data[number_of_days.capitalize()][sex.capitalize()][level.capitalize()]
        day_data = data.get(number_of_days.capitalize(), {}).get(sex.capitalize(), {}).get(level.capitalize(), {})

        for day, reach in day_data.items():
            writer.writerow([f'{day}'])
            for ele, value in reach.items():
                writer.writerow([f'{ele}: {value}'])
            writer.writerow([' '])

def main():

    st.markdown(f'''
                <style>
                .stApp{{
                    background: url('https://pix4free.org/assets/library/2021-05-25/originals/workout.jpg');
                    background-size: cover
                    }}
                    </style>''',
                    unsafe_allow_html=True)
    st.title('WORKOUT PLANNER 💪')
    st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: white;
        color: black; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
    )

    with st.expander('Here if you want a default workout program:'):
        default_radio_days = st.radio('Per week, you want to train:',
                                      ('0 day, just wanted to see the app', '1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days'))
        if default_radio_days not in ['0 day, just wanted to see the app', '7 days']:
            default_radio_level = st.radio('What level are you:', ('Beginner', 'Advanced', 'Expert'), key="default")
            default_radio_genre = st.radio('What genre are you:', ('F', 'M'))
            if st.button('Generate Workout Plan', key="default"):
                file_name = 'workout_plan.csv'
                try:
                    generate_workout_plan_default(file_name, default_radio_days, default_radio_genre, default_radio_level)
                    st.success(f'Workout plan saved as {file_name}')
                    download_button = st.download_button(
                            label="Download Workout Plan",
                            data=open(file_name, 'rb').read(),
                            key='download_button',
                            file_name='Workout Plan',
                            mime='text/txt'
                        )
                    os.remove(file_name)
                except Exception as e:
                    st.error(f'An error occurred: {e}')
        elif default_radio_days == '0 day, just wanted to see the app':
            st.write('Cool, now go train!')
        elif default_radio_days == '7 days':
            st.write('No, you need a rest day!')

    with st.expander('Here if you want a custom workout program:'):
        custom_radio_sex = st.radio('What genre are you:', ('Non-Binary', 'F', 'M'))
        if custom_radio_sex != 'Non-Binary':
            custom_radio_level = st.radio('What level are you:', ('Beginner', 'Advanced', 'Expert'), key="custom")
            if custom_radio_level is not None:
                custom_radio_muscle = st.multiselect('What muscle groups do you want to train:',
                                                     ('Chest', 'Back', 'Shoulders', 'Legs'))
                if st.button('Generate Workout Plan', key='custom'):
                    file_name = 'workout_plan.csv'
                    try:
                        for muscle_group in custom_radio_muscle:
                            generate_workout_plan_custom(file_name, custom_radio_sex, custom_radio_level, muscle_group)
                        st.success(f'Workout plan saved as {file_name}')
                        download_button = st.download_button(
                            label="Download Workout Plan",
                            data=open(file_name, 'rb').read(),
                            key='download_button',
                            file_name='Workout Plan',
                            mime='text/txt'
                        )
                        os.remove(file_name)
                    except Exception as e:
                        st.error(f'An error occurred: {e}')
        else:
            st.write("You're sick, get out of my app")

if __name__ == "__main__":
    main()
