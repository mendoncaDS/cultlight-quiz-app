import streamlit as st
from quiz_data import quiz

# Set the page title and favicon
st.set_page_config(
    page_title="Quiz da Cultlight",
    page_icon="https://cultlight.com.br/wp-content/uploads/logo-padrao-150x150.png"
)

st.markdown("""
    <style>
    [role=radiogroup]{
        gap: 3rem;
    }
    </style>
    """,unsafe_allow_html=True)

def main():

    # Render image from URL in Streamlit
    st.image("https://cultlight.com.br/wp-content/uploads/logo-cultlight-horizontal.png", width=200)

    st.subheader("Quiz da Cultlight")
    st.write("Teste seus conhecimentos canábicos!")

    st.write("---")

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
    st.subheader(f"**{current_node['question']}**")

    if current_node['options']:
        selected_option = st.radio("", current_node['options'], key=len(st.session_state.history))
        if st.button("Next"):
            st.session_state.history.append(selected_option)
            st.rerun()
    else:
        if st.button("Restart Quiz"):
            st.session_state.history = []
            st.rerun()

if __name__ == "__main__":
    main()