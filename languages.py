class Language(object):
    def __init__(self, language):
        self.language = language
        if language == 'en':
            self.langwelcome = 'Using English.'
            self.welcome = 'New game set up. Welcome!'
        elif language == 'es':
            self.langwelcome = 'Estás usando español.'
            self.welcome = 'Un juego nuevo creado. ¡Bienvenido!'

languages = ('en', 'es')
