from main import skill, Scene, build_default_response, current_app, start_skill, Button, Photo, ItemList

def start(text, entities):
    response = build_default_response()
    response['response']['text'] = 'Привет. Купи слона.'
    response['next_scene'] = '1'

    return response


def second_scene_scenary(text, entities, yes):
    global photo1, photo2
    response = build_default_response()
    if text.lower() != 'да':
        response['response']['text'] = f'Все говорят купи {text}, а ты возьми и купи слона'
        response['next_scene'] = '1'
        
    else:
        response['response']['text'] = f'Слона можно купить на ываоываываоылвароыл маркете'
        response['next_scene'] = 'END'
    
    return response


skill.add_variables(yes=0)
start_scene = Scene('start', skill, start)
second_scene = Scene('1', skill, second_scene_scenary, buttons=[Button('да')])
skill.add_scene(start_scene, second_scene)
start_skill(skill.host, skill.port)
