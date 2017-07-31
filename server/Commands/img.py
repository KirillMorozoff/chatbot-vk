import command_system
import vkapi

def img():
   # Получаем случайную картинку из пабли
   #attachment = vkapi.img_answer(147469960)
   message = "Максимально похожие фото:"
   attachment = vkapi.img_answer()

   return message, attachment

img_command = command_system.Command()

img_command.name = "фотка"
img_command.keys = ['фотка', 'фотография']
img_command.description = 'Пришлю фотографии с твоим участием'
img_command.process = img