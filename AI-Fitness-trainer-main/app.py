import streamlit as st
import subprocess

# Define the list of exercises
exercises = ["push-up", "pull-up", "squat", "walk", "sit-up", "jumping-jacks", "lunges", "leg-raises", "burpees"]

# Streamlit app header
st.title("Exercise Tracker")

# Dropdown to select exercise type
selected_exercise = st.selectbox("Select an exercise", exercises)

# Button to start the selected exercise
if st.button("Start Exercise"):
    # Run the command 'python main.py -t {exercise_type}'
    command = f"python main.py -t {selected_exercise}"
    
    # Use subprocess to execute the command
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error running the command: {e}")
    else:
        st.success(f"Exercise '{selected_exercise}' started successfully.")

# Additional Streamlit app logic...
