
import random

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
        st.session_state.options_per_question = {}
        st.session_state.correct_indices = {}

    # Get the current question number
    question_number = st.session_state.current_question

    if question_number < len(quiz):
        question_data = quiz[question_number]
        st.write(f"**Pergunta {question_number + 1}: {question_data['question']}**")

        # Check if options are already randomized for this question
        if f'question_{question_number}_options' not in st.session_state:
            # Randomize options and save to session state
            options = question_data['options'].copy()
            random.shuffle(options)
            st.session_state[f'question_{question_number}_options'] = options
            # Find the index of the correct answer in the randomized options
            correct_answer = question_data['options'][0]  # Correct answer is always the first in the original list
            st.session_state[f'question_{question_number}_correct_index'] = options.index(correct_answer)
        else:
            # Retrieve options from session state
            options = st.session_state[f'question_{question_number}_options']

        # Display options as radio buttons
        selected_option = st.radio(
            "",
            options=options,
            key=f"question_{question_number}"
        )

        st.write("---")

        if st.button("Próxima pergunta"):
            if selected_option:
                # Save the user's answer
                st.session_state.answers[question_number] = selected_option
                # Move to the next question
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("Por favor, selecione uma opção antes de prosseguir.")
    else:
        # Display results
        st.subheader("Parabéns! Você concluiu o quiz.")
        st.write("Suas respostas:")
        score = 0
        for idx in range(len(quiz)):
            question = quiz[idx]['question']
            options = st.session_state[f'question_{idx}_options']
            correct_index = st.session_state[f'question_{idx}_correct_index']
            correct_answer = options[correct_index]
            user_answer = st.session_state.answers.get(idx, "Não respondida")
            st.write(f"**Pergunta {idx + 1}:** {question}")
            st.write(f"Resposta correta: {correct_answer}")
            st.write(f"Sua resposta: {user_answer}")
            if user_answer == correct_answer:
                st.write("✅ **Correto!**")
                score += 1
            else:
                st.write("❌ **Incorreto.**")
            st.write("---")
        st.write(f"**Você acertou {score} de {len(quiz)} perguntas.**")

        if st.button("Recomeçar o Quiz"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()