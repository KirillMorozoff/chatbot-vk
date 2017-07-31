import command_system
import vkapi

def eye_color():
    message = vkapi.eye_answer()
    return message, ''

tell_about_command = command_system.Command()

tell_about_command.name = "Если назовешь цвет своих глаз"
tell_about_command.keys = ['карие', 'голубые', 'зеленые', 'зеленый', 'серые', 'серый', 'красные', 'синие',
                           'голубого', 'зеленого', 'серого', 'красного', 'синего',
                           'серо-голубые', 'серо-зеленые', 'серо-голубого', 'серо-зеленого',]
tell_about_command.description = 'Запомню его'
tell_about_command.process = eye_color