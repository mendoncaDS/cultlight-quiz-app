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
    st.image("https://cultlight.com.br/wp-content/uploads/logo-cultlight-horizontal.png", width=200)

    st.subheader("Quiz da Cultlight")
    st.write("Teste seus conhecimentos canábicos!")

    st.write("---")

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}

    # Get the current question
    if st.session_state.current_question < len(quiz):
        question_data = quiz[st.session_state.current_question]
        st.write(f"**Pergunta {st.session_state.current_question + 1}: {question_data['question']}**")

        # Display options as radio buttons
        options = question_data['options']
        option_keys = list(options.keys())
        selected_option = st.radio(
            "",
            options=[f"{key}) {options[key]}" for key in option_keys],
            key=f"question_{st.session_state.current_question}"
        )

        if st.button("Próxima pergunta"):
            # Extract the selected key from the displayed option
            selected_key = selected_option.split(')')[0]
            # Save the answer
            st.session_state.answers[st.session_state.current_question] = selected_key
            # Move to the next question
            st.session_state.current_question += 1
            st.rerun()
    else:
        st.subheader("Parabéns! Você concluiu o quiz.")
        st.write("Suas respostas:")
        for idx, answer_key in st.session_state.answers.items():
            question = quiz[idx]['question']
            selected_option_text = quiz[idx]['options'][answer_key]
            st.write(f"**Pergunta {idx + 1}:** {question}")
            st.write(f"Sua resposta: {answer_key}) {selected_option_text}")
            st.write("---")

        if st.button("Recomeçar o Quiz"):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.rerun()

if __name__ == "__main__":
    main()