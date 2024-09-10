import streamlit as st
from os.path import exists

# Read data from tn.txt
def load_data():
    if exists('tn.txt'):
        with open('tn.txt', 'r', encoding='utf8') as f:
            data = []
            raw_data = f.read().split('\n\n')
            for q in raw_data:
                q = q.split('\n')
                question = q[0]
                options = q[1:]
                correct = [c for c in options if c.endswith('*')]
                if correct:
                    correct = correct[0].replace('*', '')
                else:
                    correct = None  # Set to None if no correct answer is marked
                options = [o.replace('*', '') for o in options]
                data.append({"question": question, "options": options, "correct": correct})
            return data
    else:
        return [
            {"question": "Câu 1: ...", "options": ["A", "B", "C", "D"], "correct": "A"},
            {"question": "Câu 2: ...", "options": ["A", "B", "C", "D"], "correct": "B"},
            # Add more questions as needed
        ]

# Write updated quiz data back to tn.txt
def save_data(data):
    with open('tn.txt', 'w', encoding='utf8') as f:
        for entry in data:
            question = entry['question']
            options = [f"{o}{'*' if o == entry['correct'] else ''}" for o in entry['options']]
            f.write(f"{question}\n" + "\n".join(options) + "\n\n")

# Store the quiz data in session_state
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = load_data()

# Initialize the quiz index in session_state if it doesn't exist
if 'qs_index' not in st.session_state:
    st.session_state.qs_index = 0

# Initialize the state to close the expander after updating the answer
if 'close_expander' not in st.session_state:
    st.session_state.close_expander = False

# Initialize the checkbox state for editing
if 'checkbox_checked' not in st.session_state:
    st.session_state.checkbox_checked = False

st.set_page_config(layout="wide")



st.title("Làm trắc nghiệm")
col1, col2, col3 = st.columns([1, 10, 1])

# CSS to style the buttons to fill the entire column
st.markdown(
    """
    <style>
    .full-size-button {
        width: 100%;
        height: 100px; /* You can adjust the height as needed */
        font-size: 20px; /* Adjust the font size if needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    st.write(quiz_data[qs_index]['question'])

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
            st.warning("Please select an answer before 
