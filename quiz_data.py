# quiz_data.py

# Definindo os nós para cada pergunta

q1_node = {
    'question': 'Qual é o principal indicador de que a planta de cannabis está pronta para a colheita?',
    'options': [
        'A) Cor das folhas',
        'B) Aparência dos pistilos e dos tricomas',
        'C) Altura da planta',
        'D) Tempo desde a germinação'
    ],
    'next': {}  # Será preenchido posteriormente
}

q2_node = {
    'question': 'O que é VPD e como ele impacta o cultivo de cannabis?',
    'options': [
        'A) Volatilidade de Plantas Decíduas; controla a maturação',
        'B) Déficit de Pressão de Vapor; influencia na transpiração e absorção de nutrientes',
        'C) Variedade de Plantas Decorativas; afeta a altura das plantas',
        'D) Volume de Pulverização Diária; regula a frequência de irrigação'
    ],
    'next': {}
}

q3_node = {
    'question': 'Para que serve o uso de dióxido de carbono (CO₂) em uma sala de cultivo?',
    'options': [
        'A) Aumentar a umidade relativa do ar',
        'B) Acelerar o crescimento e potencializar a fotossíntese',
        'C) Diminuir a temperatura do ambiente',
        'D) Regular o pH do substrato'
    ],
    'next': {}
}

q4_node = {
    'question': 'Quais são os nutrientes considerados "macronutrientes" essenciais para o cultivo de cannabis?',
    'options': [
        'A) Nitrogênio, Fósforo e Potássio',
        'B) Ferro, Manganês e Zinco',
        'C) Cálcio, Enxofre e Cobre',
        'D) Níquel, Molibdênio e Cloro'
    ],
    'next': {}
}

q5_node = {
    'question': 'Qual é a diferença entre cultivo orgânico e mineral no cultivo de cannabis?',
    'options': [
        'A) No cultivo orgânico são usados nutrientes sintéticos, e no mineral, nutrientes naturais',
        'B) O cultivo orgânico utiliza insumos naturais e micro-organismos; o mineral usa fertilizantes sintéticos',
        'C) O cultivo mineral é mais barato e menos eficiente que o orgânico',
        'D) No cultivo orgânico, as plantas crescem em hidroponia; no mineral, em solo'
    ],
    'next': {}
}

q6_node = {
    'question': 'O que é a técnica "Sea of Green" (SOG) e qual é seu principal benefício?',
    'options': [
        'A) Um método de poda que aumenta a produção de resina',
        'B) Uma técnica de cultivo com várias plantas pequenas para maximizar o uso do espaço e reduzir o tempo de cultivo',
        'C) A prática de manter o solo sempre úmido para estimular o crescimento',
        'D) Uma estratégia de nutrição orgânica que aumenta o rendimento da colheita'
    ],
    'next': {}
}

q7_node = {
    'question': 'Por que é importante o pH do solo no cultivo de cannabis e qual faixa é ideal?',
    'options': [
        'A) Influencia a disponibilidade de nutrientes; ideal entre 5.5 e 6.5',
        'B) Evita o crescimento de mofo; ideal entre 4.5 e 5.0',
        'C) Melhora a absorção de água; ideal entre 7.0 e 8.0',
        'D) Maximiza a produção de terpenos; ideal entre 6.5 e 7.5'
    ],
    'next': {}
}

q8_node = {
    'question': 'O que é o tricoma e qual é sua função principal na planta de cannabis?',
    'options': [
        'A) Um tipo de raiz que ajuda na absorção de nutrientes',
        'B) Um tipo de célula de defesa que protege contra insetos',
        'C) A estrutura onde são produzidos os canabinoides e terpenos',
        'D) Uma folha modificada que absorve luz extra para a planta'
    ],
    'next': {}
}

q9_node = {
    'question': 'Quais são os fatores principais que afetam a densidade e o rendimento das flores de cannabis?',
    'options': [
        'A) Iluminação, nutrientes, controle de pragas e treinamento',
        'B) Quantidade de água, vento e altura das plantas',
        'C) Tempo de cultivo, tipo de solo e altura da sala de cultivo',
        'D) Frequência de poda, tipo de fertilizante e horário de luz'
    ],
    'next': {}
}

q10_node = {
    'question': 'Na clonagem de cannabis, qual é o fator mais importante para garantir o sucesso dos clones?',
    'options': [
        'A) Temperatura da água',
        'B) Qualidade e saúde da planta-mãe',
        'C) Quantidade de luz solar direta',
        'D) Utilização de substrato seco para evitar excesso de umidade'
    ],
    'next': {}
}

# Mapeando as opções de cada pergunta para a próxima pergunta

q1_node['next'] = {option: q2_node for option in q1_node['options']}
q2_node['next'] = {option: q3_node for option in q2_node['options']}
q3_node['next'] = {option: q4_node for option in q3_node['options']}
q4_node['next'] = {option: q5_node for option in q4_node['options']}
q5_node['next'] = {option: q6_node for option in q5_node['options']}
q6_node['next'] = {option: q7_node for option in q6_node['options']}
q7_node['next'] = {option: q8_node for option in q7_node['options']}
q8_node['next'] = {option: q9_node for option in q8_node['options']}
q9_node['next'] = {option: q10_node for option in q9_node['options']}

# Para a última pergunta, o 'next' será um dicionário vazio, indicando o fim do quiz
q10_node['next'] = {}
# Opcionalmente, podemos deixar 'options' vazio para sinalizar o fim
q10_node['options'] = []

# O objeto 'quiz' é o nó raiz do quiz
quiz = q1_node
