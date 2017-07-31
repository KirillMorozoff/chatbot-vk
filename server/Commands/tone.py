import command_system
import vkapi

def tone():
    message = vkapi.tone_answer()
    return message, ''

tone_command = command_system.Command()

tone_command.name = "Если назовешь главное для тебя в тональном средстве"
tone_command.keys = ['стойкость', 'естественность', 'легкость']
tone_command.description = 'Запомню это..'
tone_command.process = tone