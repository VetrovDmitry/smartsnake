import modes.classroomV2 as ClassRoom
# import nntest as NNTest

PARAMS_PATH = 'PARAMS.json'


modes = {
    'class_room': ClassRoom,
    # 'nn_test': NNTest
}


def start_launcher():
    mode_name = 'class_room'
    # mode_name = 'nn_test'
    modes.get(mode_name)




start_launcher()





