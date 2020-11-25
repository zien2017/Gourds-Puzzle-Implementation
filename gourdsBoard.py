import pygame
import numpy as np  # for matrix

pygame.init()
# size of the window
screen = pygame.display.set_mode((500, 400))
# caption setting
pygame.display.set_caption('Gourds')
# background colour setting
screen.fill((242, 242, 242))
# set width of the hexagonal cell
widthOfHexCell = 50;
offset = widthOfHexCell
# gourd size
gourdSize = widthOfHexCell * 0.6

# set a matrix of board
matrixOfBoard = np.array([[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]])

# set a initial gourds placement
#                           x, y, x, y
gourdsLocation = np.array([[2, 1, 3, 2]])


def boardConstructor():
    font = pygame.font.Font('OpenSans-Light.ttf', 16)

    for i in range(len(matrixOfBoard)):
        for j in range(len(matrixOfBoard[0])):
            # display matrix
            text = font.render(str(matrixOfBoard[i][j]), True, (0, 0, 255))
            screen.blit(text, (-4 + offset + j * widthOfHexCell, -12 + offset + i * widthOfHexCell * 1.732))
            # pygame.draw.circle(screen,(0,0,0),(offset + j * widthOfHexCell, offset + i * widthOfHexCell * 1.732) ,6,1)

            if (matrixOfBoard[i][j]):
                # draw a hexagonal cell
                pygame.draw.polygon(screen, (100, 100, 200,),
                                    [(offset + j * widthOfHexCell,
                                      offset + i * widthOfHexCell * 1.732 + widthOfHexCell * 1.1547), (
                                         offset + j * widthOfHexCell + widthOfHexCell,
                                         offset + i * widthOfHexCell * 1.732 + widthOfHexCell * 0.57735), (
                                         offset + j * widthOfHexCell + widthOfHexCell,
                                         offset + i * widthOfHexCell * 1.732 - widthOfHexCell * 0.57735),
                                     (offset + j * widthOfHexCell,
                                      offset + i * widthOfHexCell * 1.732 - widthOfHexCell * 1.1547),
                                     (offset + j * widthOfHexCell - widthOfHexCell,
                                      offset + i * widthOfHexCell * 1.732 - widthOfHexCell * 0.57735), (
                                         offset + j * widthOfHexCell - widthOfHexCell,
                                         offset + i * widthOfHexCell * 1.732 + widthOfHexCell * 0.57735)], 1)

    # refresh the window
    pygame.display.flip()


def gourdsConstructor():
    for i in range(len(gourdsLocation)):
        pygame.draw.circle(screen, (100, 0, 0), (
            offset + gourdsLocation[i][0] * widthOfHexCell, offset + gourdsLocation[i][1] * widthOfHexCell * 1.732),
                           gourdSize, 1)
        pygame.draw.circle(screen, (100, 0, 0), (
            offset + gourdsLocation[i][2] * widthOfHexCell, offset + gourdsLocation[i][3] * widthOfHexCell * 1.732),
                           gourdSize, 1)
        pygame.draw.line(screen, (100, 0, 0), (
            offset + gourdsLocation[i][0] * widthOfHexCell, offset + gourdsLocation[i][1] * widthOfHexCell * 1.732), (
                             offset + gourdsLocation[i][2] * widthOfHexCell,
                             offset + gourdsLocation[i][3] * widthOfHexCell * 1.732), width=1)
    # refresh the window
    pygame.display.flip()


def searchGourdsFromCoordinate(pos):
    x, y = pos

    # shrink the searching area
    x = x - offset
    y = y - offset
    x = x / widthOfHexCell
    y = y / 1.732 / widthOfHexCell
    x = int(x + 0.5)
    y = int(y + 0.5)

    return searchGourdsFromIndex(x, y)


def searchGourdsFromIndex(x, y, xDestination = -1, yDestination = -1):
    # search if there is a gourd on (x, y)
    for i in range(len(gourdsLocation)):
        if (x == gourdsLocation[i][0] and y == gourdsLocation[i][1]):
            if xDestination != -1:
                gourdsLocation[i][0] = xDestination
                gourdsLocation[i][1] = yDestination
            return x, y
        if (x == gourdsLocation[i][2] and y == gourdsLocation[i][3]):
            if xDestination != -1:
                gourdsLocation[i][2] = xDestination
                gourdsLocation[i][3] = yDestination
            return x, y
    return -1, -1


def searchAnEmptyCellAround(x, y):
    # search an empty cell around x, y

    if (matrixOfBoard[y - 1][x - 1] == 1) and (searchGourdsFromIndex(x - 1, y - 1) == (-1, -1)):  # upper left
        return x - 1, y - 1
    if (matrixOfBoard[y + 1][x - 1] == 1) and (searchGourdsFromIndex(x - 1, y + 1) == (-1, -1)):  # lower left
        return x - 1, y + 1
    if (matrixOfBoard[y + 1][x + 1] == 1) and (searchGourdsFromIndex(x + 1, y + 1) == (-1, -1)):  # lower right
        return x + 1, y + 1
    if (matrixOfBoard[y - 1][x + 1] == 1) and (searchGourdsFromIndex(x + 1, y - 1) == (-1, -1)):  # upper right
        return x + 1, y - 1
    if (matrixOfBoard[y][x - 2] == 1) and (searchGourdsFromIndex(x - 2, y) == (-1, -1)):  # left
        return x - 2, y
    if (matrixOfBoard[y][x + 2] == 1) and (searchGourdsFromIndex(x + 2, y) == (-1, -1)):  # right
        return x + 2, y
    return -1, -1


def main():
    # 开启一个事件循环处理发生的事件
    running = True
    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # MOUSE BUTTON DOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                xGourd, yGourd = searchGourdsFromCoordinate(event.pos)
                if xGourd != -1:
                    print(xGourd, yGourd)
                    xCell, yCell = searchAnEmptyCellAround(xGourd, yGourd)
                    if xCell != -1:
                        searchGourdsFromIndex(xGourd, yGourd, xCell, yCell)
                        screen.fill((242, 242, 242))
                        boardConstructor()
                        gourdsConstructor()
                        pygame.display.flip()

            # 鼠标弹起
            if event.type == pygame.MOUSEBUTTONUP:
                pass


if __name__ == '__main__':
    boardConstructor()
    gourdsConstructor()
    main()
