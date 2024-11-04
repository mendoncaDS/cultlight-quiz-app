
quiz = {
    'question': 'What is your favorite color?',
    'options': ['Red', 'Blue'],
    'next': {
        'Red': {
            'question': 'Do you like apples?',
            'options': ['Yes', 'No'],
            'next': {
                'Yes': {
                    'question': 'You must love apple pie!',
                    'options': [],
                    'next': {}
                },
                'No': {
                    'question': 'Maybe you prefer cherries?',
                    'options': [],
                    'next': {}
                }
            }
        },
        'Blue': {
            'question': 'Do you enjoy the ocean?',
            'options': ['Yes', 'No'],
            'next': {
                'Yes': {
                    'question': 'Sailing might be your thing!',
                    'options': [],
                    'next': {}
                },
                'No': {
                    'question': 'Mountains could be your escape!',
                    'options': [],
                    'next': {}
                }
            }
        }
    }
}
