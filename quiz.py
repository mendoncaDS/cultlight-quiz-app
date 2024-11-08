
import os
import dotenv
import random
import gspread

import streamlit as st

from quiz_data import quiz
from google.oauth2.service_account import Credentials

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

dotenv.load_dotenv()





def write_answers_to_sheet(answers, total_questions, name, email, cellphone):


    # Authentication code (reuse your existing credentials)
    # Fetch the private key from environment variables
    private_key = os.getenv("private_key")
    
    # Define the service account info
    service_account_info = {
        "type": "service_account",
        "project_id": "cultlight-calc",
        "private_key_id": os.getenv("private_key_id"),
        "private_key": private_key.replace('\\n', '\n'),
        "client_email": "cl-calc-service-acc@cultlight-calc.iam.gserviceaccount.com",
        "token_uri": "https://oauth2.googleapis.com/token",
    }

    # Define the scopes
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # Authenticate using the stored credentials or create new ones
    if 'credentials' not in st.session_state:
        st.session_state.credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    credentials = st.session_state.credentials

    # Authorize with gspread
    gc = gspread.authorize(credentials)

    # Open the spreadsheet and select the first sheet
    sheet = gc.open('quiz-sheet').sheet1

    # Prepare a list to hold the answer indices
    answer_indices = []

    for question_index in range(total_questions):
        # Get the user's answer
        user_answer = answers.get(question_index, None)

        if user_answer is None:
            # Shouldn't happen with radio buttons, but included for robustness
            answer_indices.append('')
        else:
            # Get the option mapping from session state
            option_mapping = st.session_state.get(f'question_{question_index}_option_mapping', {})
            # Get the original index of the user's answer
            original_index = option_mapping.get(user_answer, None)
            if original_index is not None:
                # Indices start from 0; add 1 to start counting from 1
                answer_indices.append(original_index + 1)
            else:
                # User's answer not found in mapping
                answer_indices.append('')

    # Prepare the row to append
    # Include name, email, and cellphone as the first three columns
    row = [name, email, cellphone] + answer_indices

    # For debugging purposes, print the row
    print(f"\n\nRow to append: {row}\n\n")

    # Append the row to the sheet
    if "answers_stored" not in st.session_state:
        sheet.append_row(row)
        st.session_state.answers_stored = True





def main():
    
    st.image("https://cultlight.com.br/wp-content/uploads/logo-cultlight-horizontal.png", width=200)
    
    st.subheader("Teste seus conhecimentos canábicos!")
    
    st.write("---")
    
    # Initialize session state for user info
    if 'user_info_collected' not in st.session_state:
        st.session_state.user_info_collected = False
    
    # If user info hasn't been collected yet, display the input form
    if not st.session_state.user_info_collected:
        st.write("Insira suas informações")
        
        # Collect user inputs
        name = st.text_input("Nome")
        email = st.text_input("E-mail")
        cellphone = st.text_input("Celular")
        
        st.write("")
        st.write("Se não quiser, pode deixar em branco")
        st.write("---")
        
        if st.button("Iniciar o Quiz"):
            # Store the user info in session state
            st.session_state.user_name = name
            st.session_state.user_email = email
            st.session_state.user_cellphone = cellphone
            st.session_state.user_info_collected = True
            st.rerun()  # Rerun the app to proceed to the quiz
        return  # Stop execution here until user info is collected
    
    # Initialize the quiz after user info is collected
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.options_per_question = {}
        st.session_state.correct_indices = {}
        # Shuffle the quiz and save it in session state
        st.session_state.shuffled_quiz = quiz.copy()
        random.shuffle(st.session_state.shuffled_quiz)
    
    # Número da pergunta atual
    question_number = st.session_state.current_question
    
    total_questions = len(st.session_state.shuffled_quiz)
    
    # If there are still questions left
    if question_number < total_questions:
        # Retrieve the current question data
        question_data = st.session_state.shuffled_quiz[question_number]
        st.write(f"#### **# {question_number + 1}: {question_data['question']}**")
        #st.write(f"**{question_data['question']}**")
        
        # Check if options have already been shuffled for this question
        if f'question_{question_number}_options' not in st.session_state:
            # Get the original options list from the current question
            original_options = question_data['options']
            
            # Copy and shuffle the options
            options = original_options.copy()
            random.shuffle(options)
            st.session_state[f'question_{question_number}_options'] = options
            
            # Find the index of the correct answer in the shuffled options
            correct_answer = original_options[0]  # Correct answer is always the first in the original list
            st.session_state[f'question_{question_number}_correct_index'] = options.index(correct_answer)
            
            # Create a mapping from shuffled options to their original indices
            option_mapping = {}
            for option in options:
                original_idx = original_options.index(option)
                option_mapping[option] = original_idx
            st.session_state[f'question_{question_number}_option_mapping'] = option_mapping
        else:
            # Retrieve the shuffled options and mapping from session state
            options = st.session_state[f'question_{question_number}_options']
            option_mapping = st.session_state[f'question_{question_number}_option_mapping']
    
        # Obtém a resposta já selecionada, se houver
        if question_number in st.session_state.answers:
            selected_option = st.session_state.answers[question_number]
            index = options.index(selected_option)
        else:
            index = 0  # Seleciona a primeira opção por padrão

        # Exibe as opções como botões de rádio
        selected_option = st.radio(
            "_",
            label_visibility="hidden",
            options=options,
            index=index,
            key=f"question_{question_number}"
        )

        # Salva a resposta atual
        st.session_state.answers[question_number] = selected_option

        st.write("")
        st.write("")
    
        # Exibe a barra de progresso
        progress = question_number / total_questions
        st.progress(progress)

        st.write("---")
    
        # Botões de navegação
        col1, col2, col3 = st.columns(3)
        with col1:
            if question_number:
                if st.button("Voltar"):
                    if question_number > 0:
                        # Retorna à pergunta anterior
                        st.session_state.current_question -= 1
                        st.rerun()
        with col3:
            if question_number+1==total_questions:
                btn_name = "Finalizar"
            else:
                btn_name = "Próxima pergunta"
            if st.button(btn_name):
                # Avança para a próxima pergunta
                st.session_state.current_question += 1
                st.rerun()
    
    # Pergunta final para confirmar se o usuário deseja finalizar o quiz
    elif question_number == total_questions:
        st.subheader("Tem certeza que deseja finalizar o quiz?")
        st.write("Você pode voltar para revisar suas respostas antes de finalizar.")

        st.write("")
        st.write("")

        # Exibe a barra de progresso completa
        st.progress(1.0)
        
        st.write("---")
        
        # Botões de navegação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Voltar"):
                st.session_state.current_question -= 1
                st.rerun()
        with col2:
            if st.button("Finalizar"):
                st.session_state.current_question += 1  # Avança para a tela de resultados
                st.rerun()
    
    # Exibe os resultados
    else:
        print(f"\n\nRESULTADOS:\n\n{st.session_state.answers}")
        st.subheader("Parabéns! Você concluiu o quiz.")
        st.write("Suas respostas:")
        score = 0
        for idx in range(total_questions):
            question = st.session_state.shuffled_quiz[idx]['question']
            options = st.session_state[f'question_{idx}_options']
            correct_index = st.session_state[f'question_{idx}_correct_index']
            correct_answer = options[correct_index]
            user_answer = st.session_state.answers.get(idx, "Não respondida")
            if user_answer == correct_answer:
                st.write(f"**#{idx + 1}: {question}**")
                st.write(f"**Sua resposta:** **{user_answer}**")
                st.write("✅ **Correto!**")
                score += 1
            else:
                st.write(f"**#{idx + 1}: {question}**")
                st.write(f"**Sua resposta:** {user_answer}")
                st.write("❌ **Incorreto.**")
                st.write(f"**Resposta correta:** {correct_answer}")
            st.write("---")
        st.write(f"**Você acertou {score} de {total_questions} perguntas.**")
    
        # Write the user's answers to the Google Sheet
        write_answers_to_sheet(
            st.session_state.answers,
            total_questions,
            st.session_state.user_name,
            st.session_state.user_email,
            st.session_state.user_cellphone
        )

if __name__ == "__main__":
    main()

