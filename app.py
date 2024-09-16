import streamlit as st
from os.path import exists
import os
import random
import re
# list all txt file from the current directory
txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]

# Read data from tn.txt
def load_data(file_name):
    if file_name in txt_files:
        with open(file_name, 'r', encoding='utf8') as f:
            data = []
            raw_data = f.read().split('\n\n')
            for q in raw_data:
                q = q.strip().split('\n')
                question = q[0]
                imgs = re.findall(r'<img>(.+?)</img>', question)
                if imgs:
                    for img in imgs:
                        question = question.replace(f'<img>{img}</img>', '')
                options = q[1:]
                correct = [c.strip() for c in options if c.strip().endswith('*')]
                if correct:
                    # remove * character at the end of the correct answer
                    correct = correct[0].rstrip('*')
                else:
                    correct = None  # Set to None if no correct answer is marked
                options = [o.rstrip('*') for o in options]
                data.append({"question": question, "options": options, "correct": correct, "imgs": imgs})
            random.shuffle(data)
            st.session_state.quiz_data = data
            return data
    else:
        return []

st.set_page_config(layout="wide")
st.title("Trắc Nghiệm Sau Đại Học Y Khoa Phạm Ngọc Thạch")
st.write("Liên hệ: jetaudio.media@gmail.com")
db_selector_col1, db_selector_col2 = st.columns([7, 3], vertical_alignment='bottom')
with db_selector_col1:
    # let user choose the file
    file_name = st.selectbox("Choose a file", [t.replace('.txt','') for t in txt_files]) + '.txt'

with db_selector_col2:
    if st.button("Load Selected Data", use_container_width=True):
        st.session_state.quiz_data = load_data(file_name)

# Store the quiz data in session_state
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = load_data(txt_files[0])

# Initialize the quiz index in session_state if it doesn't exist
if 'qs_index' not in st.session_state:
    st.session_state.qs_index = 0

# Initialize the state to close the expander after updating the answer
if 'close_expander' not in st.session_state:
    st.session_state.close_expander = False

# Initialize the checkbox state for editing
if 'checkbox_checked' not in st.session_state:
    st.session_state.checkbox_checked = False

# hide topbar
st.markdown("""
<style>
    header {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    div[class^="viewerBadge"] {
        visibility: hidden;
    }
</style>""",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 10, 1], vertical_alignment='bottom')

# Handle previous and next buttons
with col1:
    if st.button("Previous", key="prev_button", help="Previous Question", use_container_width=True):
        st.session_state.qs_index = max(0, st.session_state.qs_index - 1)

with col3:
    if st.button("Next", key="next_button", help="Next Question", use_container_width=True):
        st.session_state.qs_index = min(len(st.session_state.quiz_data) - 1, st.session_state.qs_index + 1)

qs_index = st.session_state.qs_index
quiz_data = st.session_state.quiz_data

with col2:
    st.write(f"Question {qs_index + 1} of {len(quiz_data)}")
    st.write(quiz_data[qs_index]['question'])
    if quiz_data[qs_index]['imgs']:
        for img in quiz_data[qs_index]['imgs']:
            st.image(img, width=360)

    # Radio button with no default selection (initial value is None)
    user_answer = st.radio("Select an answer", quiz_data[qs_index]["options"], index=None, key=f"answer_{qs_index}")
    
    if st.button("Check", use_container_width=True):
        # Check if an option has been selected
        if user_answer:
            if user_answer == quiz_data[qs_index]['correct']:
                st.success("Correct!")
            else:
                st.error("Wrong!")
        else:
            st.warning("Please select an answer before check")
