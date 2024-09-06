import streamlit as st
import pandas as pd
import os

# File to store the questionnaire responses
RESPONSES_FILE = 'responses.csv'

# Function to load or create a CSV file for responses
def load_responses():
    if os.path.exists(RESPONSES_FILE):
        return pd.read_csv(RESPONSES_FILE)
    else:
        return pd.DataFrame(columns=['user_id', 'category', 'video', 'safety', 'movement', 'comfort', 'completed'])

responses_df = load_responses()

# Define categories and YouTube video URLs
categories = {
    'Category 1': [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Replace with your actual video URLs
        'https://www.youtube.com/watch?v=example2',
        'https://www.youtube.com/watch?v=example3',
        'https://www.youtube.com/watch?v=example4'
    ],
    'Category 2': [
        'https://www.youtube.com/watch?v=example5',
        'https://www.youtube.com/watch?v=example6',
        'https://www.youtube.com/watch?v=example7',
        'https://www.youtube.com/watch?v=example8'
    ],
    'Category 3': [
        'https://www.youtube.com/watch?v=example9',
        'https://www.youtube.com/watch?v=example10',
        'https://www.youtube.com/watch?v=example11',
        'https://www.youtube.com/watch?v=example12'
    ],
    'Category 4': [
        'https://www.youtube.com/watch?v=example13',
        'https://www.youtube.com/watch?v=example14',
        'https://www.youtube.com/watch?v=example15',
        'https://www.youtube.com/watch?v=example16'
    ]
}

# Streamlit App
st.title("Video App with Questionnaire")

# User ID input
user_id = st.text_input("Enter your User ID:")

if user_id:
    st.write(f"Welcome, User {user_id}!")
    
    # Show available categories
    selected_category = st.selectbox("Choose a category:", list(categories.keys()))

    # Show available videos in the selected category
    if selected_category:
        selected_video = st.selectbox("Choose a video:", categories[selected_category])
        
        # Show the YouTube video
        if selected_video:
            st.video(selected_video)
            
            # Questionnaire after video
            st.write("Please rate the following aspects of the robot:")
            
            # Question 1: Robot's safety regarding objects/people
            safety = st.select_slider(
                "Rate robot's safety regarding objects/people:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Safe" if x == 1 else ("Safe" if x == 5 else "")
            )
            
            # Question 2: Robot's movement
            movement = st.select_slider(
                "Rate robot's movement:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Natural" if x == 1 else ("Natural" if x == 5 else "")
            )
            
            # Question 3: Comfort level with the robot
            comfort = st.select_slider(
                "Rate your comfort level with the robot:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "Not Comfortable" if x == 1 else ("Comfortable" if x == 5 else "")
            )
            
            if st.button("Submit"):
                # Save the response
                new_entry = pd.DataFrame([[user_id, selected_category, selected_video, safety, movement, comfort, True]], 
                                         columns=['user_id', 'category', 'video', 'safety', 'movement', 'comfort', 'completed'])
                responses_df = pd.concat([responses_df, new_entry], ignore_index=True)
                responses_df.to_csv(RESPONSES_FILE, index=False)
                st.success("Your response has been recorded!")

            # Show completed videos
            completed_videos = responses_df[(responses_df['user_id'] == user_id) & 
                                            (responses_df['category'] == selected_category) & 
                                            (responses_df['completed'] == True)]['video'].tolist()
            if completed_videos:
                st.write("You have completed the following videos:")
                st.write(completed_videos)
            
            # Check if all videos are completed
            if len(completed_videos) == len(categories[selected_category]):
                st.write("Congratulations! You have completed all videos in this category.")

            # Provide download link for user's responses
            user_responses = responses_df[responses_df['user_id'] == user_id]
            if not user_responses.empty:
                csv = user_responses.to_csv(index=False)
                st.download_button(
                    label="Download your responses",
                    data=csv,
                    file_name=f"user_{user_id}_responses.csv",
                    mime='text/csv'
                )
