import numpy
class boardsConfig(object):
    board = numpy.array([
        # x 0, 1, 2, 3, 4, 5, 6, 7, 8
        [0, 4, 0, 4, 0, 1, 0],  # 0
        [2, 0, 2, 0, 3, 0, 2],  # 1
        [0, 1, 0, 1, 0, 1, 0],  # 2
        [2, 0, 2, 0, 3, 0, 0],  # 3
    ])

    gourdsList = numpy.array([
        # x, y, x, y, colourLib_1, colourLib_2
        [1, 0, 0, 1, 4, 2],
        [2, 1, 4, 1, 4, 3],
        [1, 2, 3, 2, 1, 2],
        [0, 3, 2, 3, 3, 1],
        [4, 3, 5, 2, 2, 1],
        [5, 0, 6, 1, 2, 2],
    ])



