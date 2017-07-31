import command_system
import vkapi

def hello():
   message = vkapi.hello_answer()
   return message, ''

hello_command = command_system.Command()

hello_command.name = "привет"
hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello