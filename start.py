import modes.classroomV2 as ClassRoom


PARAMS_PATH = 'PARAMS.json'


modes = {
    'class_room': ClassRoom
}


def start_launcher():
    mode_name = 'class_room'
    modes.get(mode_name)




start_launcher()





