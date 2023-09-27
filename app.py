import streamlit as st
import csv
import sys
import os
import json
import cv2 as cv

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

def generate_workout_plan(file_name, sex, level, muscle_group):
    with open(file_name, 'a', newline='') as file_modified:
        writer = csv.writer(file_modified)
        if file_modified.tell() == 0:
            writer.writerow([f'Sex: {sex.capitalize()}, Level: {level.capitalize()}'])
            writer.writerow(['45 seconds rest between each series'])
            writer.writerow(['1 minute rest between each exercise'])
            writer.writerow([' '])

        data = read_data_from_txt("program.txt")
        reach = data[sex.capitalize()][level.capitalize()][muscle_group.capitalize()]
        writer.writerow([f'{muscle_group.capitalize()}'])
        for ele in reach:
            writer.writerow([f'{ele}: {reach.get(ele)}'])
        writer.writerow([' '])

def main():

    st.title('WORKOUT PLANNER 💪')

    with st.expander('Here if you want a default workout program:'):
        default_radio_days = st.radio('Per week, you want to train:',
                                      ('0 day, just wanted to see the app', '1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days'))
        if default_radio_days != '0 day, just wanted to see the app' and default_radio_days != '7 days':
            default_radio_level = st.radio('What level are you:', ('Beginner', 'Advanced', 'Expert'))
            default_radio_genre = st.radio('What genre are you:', ('F', 'M'))
        elif default_radio_days == '0 day, just wanted to see the app':
            st.write('Cool, now go train!')
        elif default_radio_days == '7 days':
            st.write('No, you need a rest day!')

    with st.expander('Here if you want a custom workout program:'):
        custom_radio_sex = st.radio('What genre are you:', ('Non-Binary', 'F', 'M'))
        if custom_radio_sex != 'Non-Binary':
            custom_radio_level = st.radio('What level are you:', ('Beginner', 'Advanced', 'Expert'))
            if custom_radio_level is not None:
                custom_radio_muscle = st.multiselect('What muscle groups do you want to train:',
                                                     ('Chest', 'Back', 'Shoulders', 'Legs'))
                if st.button('Generate Workout Plan'):
                    file_name = 'workout_plan.csv'
                    try:
                        for muscle_group in custom_radio_muscle:
                            generate_workout_plan(file_name, custom_radio_sex, custom_radio_level, muscle_group)
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
