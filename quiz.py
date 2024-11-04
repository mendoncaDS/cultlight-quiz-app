import streamlit as st
from quiz_data import quiz

# Set the page title and favicon
st.set_page_config(
    page_title="Quiz da Cultlight",
    page_icon="https://cultlight.com.br/wp-content/uploads/logo-padrao-150x150.png"
)

def main():

    # Render image from URL in Streamlit
    st.image("https://cultlight.com.br/wp-content/uploads/logo-cultlight-horizontal.png", width=200)

    st.subheader("Quiz da Cultlight")

    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Function to traverse the quiz tree
    def get_current_node(quiz_structure, history):
        node = quiz_structure
        for answer in history:
            node = node['next'][answer]
        return node

    current_node = get_current_node(quiz, st.session_state.history)
    st.write(current_node['question'])

    if current_node['options']:
        selected_option = st.radio("Choose an option:", current_node['options'], key=len(st.session_state.history))
        if st.button("Next"):
            st.session_state.history.append(selected_option)
            st.rerun()
    else:
        if st.button("Restart Quiz"):
            st.session_state.history = []
            st.rerun()

if __name__ == "__main__":
    main()