import command_system
import vkapi

def skin_color():
    message = vkapi.skin_answer()
    return message, ''

tell_about_command = command_system.Command()

tell_about_command.name = "Если назовешь цвет своей кожи"
tell_about_command.keys = ['розовый', 'оливковый', 'розовая', 'оливковая']
tell_about_command.description = 'Запомню его'
tell_about_command.process = skin_color