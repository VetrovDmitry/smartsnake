import modes.classroomV2 as ClassRoom
# import nntest as NNTest
# import modes.photostudio as Photostudio

modes = {
    'class_room': ClassRoom,
    # 'photostudion':Photostudio,
    # 'nn_test': NNTest
}


def start_launcher():
    mode_name = 'class_room'
    # mode_name = 'nn_test'
    modes.get(mode_name)




start_launcher()





