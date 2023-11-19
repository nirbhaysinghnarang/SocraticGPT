import streamlit as st
from question import Question

def display_question_info(question_obj, depth=0):
    """ Recursively display question information. """
    # Display the question and its atomic status
    st.text(f"{'--' * depth} Question: {question_obj.question}")
    st.text(f"{'--' * depth} Is Atomic: {question_obj.is_atomic()}")

    # Get and display the answer
    answer = question_obj.get_answer(depth, 3)  # Assuming a max_depth of 3
    st.text(f"{'--' * depth} Answer: {answer}")

    # If not atomic, display sub-questions
    if not question_obj.is_atomic():
        sub_questions = question_obj.get_sub_questions()
        for sub_q in sub_questions:
            sub_question_obj = Question(sub_q)
            display_question_info(sub_question_obj, depth + 1)

st.title("HistoryAGI")
query = st.text_input("Query")

if st.button("Answer!", type="primary") and query:
    question = Question(query)
    display_question_info(question)
