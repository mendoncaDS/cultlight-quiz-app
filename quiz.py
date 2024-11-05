
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
    
    # Inicializa o estado da sessão
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.options_per_question = {}
        st.session_state.correct_indices = {}
        # Embaralha as perguntas e salva no estado da sessão
        st.session_state.shuffled_quiz = quiz.copy()
        random.shuffle(st.session_state.shuffled_quiz)
    
    # Número da pergunta atual
    question_number = st.session_state.current_question
    
    total_questions = len(st.session_state.shuffled_quiz)
    
    # Se ainda houver perguntas
    if question_number < total_questions:
        question_data = st.session_state.shuffled_quiz[question_number]
        st.write(f"### Pergunta {question_number + 1} de {total_questions}:")
        st.write(f"**{question_data['question']}**")
    
        # Verifica se as opções já foram embaralhadas para esta pergunta
        if f'question_{question_number}_options' not in st.session_state:
            # Embaralha as opções e salva no estado da sessão
            options = question_data['options'].copy()
            random.shuffle(options)
            st.session_state[f'question_{question_number}_options'] = options
            # Encontra o índice da resposta correta nas opções embaralhadas
            correct_answer = question_data['options'][0]  # Resposta correta é sempre a primeira na lista original
            st.session_state[f'question_{question_number}_correct_index'] = options.index(correct_answer)
        else:
            # Recupera as opções do estado da sessão
            options = st.session_state[f'question_{question_number}_options']
    
        # Obtém a resposta já selecionada, se houver
        if question_number in st.session_state.answers:
            selected_option = st.session_state.answers[question_number]
            index = options.index(selected_option)
        else:
            index = 0  # Seleciona a primeira opção por padrão

        # Exibe as opções como botões de rádio
        selected_option = st.radio(
            "",
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
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Voltar"):
                if question_number > 0:
                    # Retorna à pergunta anterior
                    st.session_state.current_question -= 1
                    st.rerun()
        with col2:
            if st.button("Próxima pergunta"):
                # Avança para a próxima pergunta
                st.session_state.current_question += 1
                st.rerun()
    
    # Pergunta final para confirmar se o usuário deseja finalizar o quiz
    elif question_number == total_questions:
        st.subheader("Você deseja finalizar o quiz?")
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
        st.subheader("Parabéns! Você concluiu o quiz.")
        st.write("Suas respostas:")
        score = 0
        for idx in range(total_questions):
            question = st.session_state.shuffled_quiz[idx]['question']
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
        st.write(f"**Você acertou {score} de {total_questions} perguntas.**")
    
        if st.button("Recomeçar o Quiz"):
            # Limpa o estado da sessão
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()