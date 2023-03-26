from main import *
from button import Button
from random import choice, randrange
from config_examples import examples
from card import Photo, BigImage

skill.add_variables(task_number=0)
skill.add_variables(task_answer=0, task_link='')
AUTH_TOKEN = 'OAuth AQAAAABFR7qRAAT7o-z5WS14-E3NgJ6iI4IoUeI'
SKILL_ID = 'be55abd0-b4c2-4bf8-b57c-765f1151c91a'


def start(text, entity):
    response = build_default_response()
    response['response']['text'] = choice(['Привет, готов готовиться к ЕГЭ? Давай начнем!', 'Привет, давай начнём готовиться к ЕГЭ!', 'Ну что ж, пришло время прокачать свой скилл по информатике, ты готов?'])
    response['next_scene'] = 'choice'
    return response


def second_scenary(text, entity):
    response = build_default_response()
    if text.lower() in ['да', 'давай']:
        response['response']['text'] =  choice(['Отлично! напиши номер задания, которое хочешь отработать','Тогда отправь мне номер задания для отработки'])
        response['next_scene'] = 'task'
    elif text.lower() == 'нет':
        response['response']['text'] = choice(['Когда захотите улучшить свои навыки по ЕГЭ - обращайтесь! До встречи!', 
                                        'Когда захотите улучшить свои навыки по ЕГЭ - обращайтесь! До встречи! "Навык выключается"']
                                        )
        response['next_scene'] = 'END'

    else:
        response['response']['text'] = 'Я не очень вас поняла. Скажите, пожалуйста, еще раз.'
        response['next_scene'] = 'choice'
        response['response']['buttons'] = []
    return response


def number_task_choice(text, entity):
    response = build_default_response()
    if text.lower().split()[-1].isdigit() and 1 <= int(text.lower().split()[-1]) <= 27:
        skill.dialogs[skill.current_id].variables['task_number'].value = int(text.lower().split()[-1])
        response['response']['text'] = 'Вы хотите начать прорешивать задания или ознакомиться с теорией?'
        response['next_scene'] = 'task_complaining'
        response['response']['buttons'] = [Button('Практика', hide=True).get_button_object(), 
                                           Button('Теория', hide=True).get_button_object()]
    else:
        response['response']['text'] = choice(['Я не очень вас поняла. Скажите, пожалуйста, еще раз.', 'Мне кажется, что я не совсем поняла вас, попробуйте перефразировать или повторить запрос','Ой, кажется такого номера не существует','Мне очень жаль, но такого задания нет в моем каталоге, попробуйте выбрать другой номер'])
        response['next_scene']  = 'task'
    return response

def task_complaining(text, entity):
    response = build_default_response()
    if text.lower() == 'практика':
        
        task_num = skill.dialogs[skill.current_id].variables['task_number'].value
        path = f'examples\\{task_num}\\'
        filename = str(task_num) + '_' + str(randrange(1, 7)) + '.png'
        skill.dialogs[skill.current_id].variables['task_answer'].value = examples[filename][0]
        skill.dialogs[skill.current_id].variables['task_link'].value = examples[filename][1]
        task_var = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN, file=path+filename, title='Попробуйте решить это задание.\nНажмите на изображение, если вам не видно текст задания')
        task_var.upload_image()
        complete_photo = BigImage(task_var)
        complete_photo.button = Button('', url=skill.dialogs[skill.current_id].variables['task_link'].value)
        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'check_answer'
        response['response']['text'] = 'Ой'
        if len(examples[filename]) == 3:
            response['response']['buttons'] = [Button('Скачать файл', url=examples[filename][2]).get_button_object()]
        if len(examples[filename]) == 4:
            response['response']['buttons'] = [Button('Скачать файл A', url=examples[filename][2]).get_button_object(),
                                               Button('Скачать файл B', url=examples[filename][3]).get_button_object()]
    return response

def task_check_answer(text, entity):
    response = build_default_response()
    if skill.dialogs[skill.current_id].variables['task_answer'].value == text:
        response['response']['text'] = 'Всё правильно! Ты молодец. Хочешь еще решить что-нибудь?'
        response['response']['buttons'] = [Button('да', hide=True).get_button_object(), Button('нет', hide=True).get_button_object(), Button('Поменять задание', hide=True).get_button_object()]
        response['next_scene'] = 'continue'
    else:
        answer = skill.dialogs[skill.current_id].variables['task_answer'].value
        response['response']['text'] = f'Похоже вы ошиблись. Правильный ответ: {answer}. Еще немного практики и всё получится. Хотите еще порешать заданий?'
        response['response']['buttons'] = [Button('да', hide=True).get_button_object(), Button('нет', hide=True).get_button_object(), Button('Поменять задание', hide=True).get_button_object()]
        response['next_scene'] = 'continue'
    return response


def continue_scene(text, entity):
    response = build_default_response()
    response['response']['text'] = 'Я не очень вас поняла, повторите пожалуйста еще раз'
    response['next_scene'] = 'continue'
    if text.lower() in ['да', 'конечно', 'го', 'давай']:
         
        task_num = skill.dialogs[skill.current_id].variables['task_number'].value
        path = f'examples\\{task_num}\\'
        filename = str(task_num) + '_' + str(randrange(1, 7)) + '.png'
        skill.dialogs[skill.current_id].variables['task_answer'].value = examples[filename][0]
        skill.dialogs[skill.current_id].variables['task_link'].value = examples[filename][1]
        task_var = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN, file=path+filename, title='Вот еще одно задание для вас.\nНажмите на изображение, если вам не видно текст задания')
        task_var.upload_image()
        complete_photo = BigImage(task_var)
        complete_photo.button = Button('', url=skill.dialogs[skill.current_id].variables['task_link'].value)
        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'check_answer'
        response['response']['text'] = 'Ой'
        if len(examples[filename]) == 3:
            response['response']['buttons'] = [Button('Скачать файл', url=examples[filename][2]).get_button_object()]
        if len(examples[filename]) == 4:
            response['response']['buttons'] = [Button('Скачать файл A', url=examples[filename][2]).get_button_object(),
                                               Button('Скачать файл B', url=examples[filename][3]).get_button_object()]
    if text.lower() in ['нет', 'неа', 'не хочу', 'хватит']:
        response['response']['text'] = 'Вы сегодня хорошо постарались. Приходите, когда захотите прорешать еще заданий.'
        response['next_scene'] = 'END'
    if text.lower() == 'поменять задание':
        response['response']['text'] = 'Какое задание с 1 по 27 хотите прорешать?'
        response['next_scene'] = 'task'
    return response

start_scene = Scene('start',skill, scenary=start,buttons=[Button('Давай', hide=True), Button('Помощь', hide=True)])
second_scene = Scene('choice', skill, second_scenary, buttons=[Button(str(x+1), hide=False) for x in range(27)])
task_scene = Scene('task', skill, number_task_choice)
complete_scene = Scene('task_complaining', skill, task_complaining)
check_answer = Scene('check_answer', skill, task_check_answer)
continue_scene = Scene('continue', skill, continue_scene)

skill.add_scene(start_scene)
skill.add_scene(second_scene)
start_skill(skill.host, skill.port)