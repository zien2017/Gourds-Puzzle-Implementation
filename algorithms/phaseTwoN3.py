import copy

import pygame

class phaseTwoN3(object):

    def __init__(self, screen, myBoardsConfig, myButtons, myCellsConstructor, myGourdsConstructor, myHamiltonianCycle, myFinalGourdsConfig, myFinalHCycleOrderConfig):
        self.screen = screen
        self.myBoardsConfig = myBoardsConfig
        self.myButtons = myButtons
        self.myCellsConstructor = myCellsConstructor
        self.myGourdsConstructor = myGourdsConstructor
        self.myHamiltonianCycle = myHamiltonianCycle
        self.myFinalGourdsConfig = myFinalGourdsConfig
        self.myFinalHCycleOrderConfig = myFinalHCycleOrderConfig

        self.HCycleAux = self.myHamiltonianCycle.HCycleAux
        self.firstRunFlag = True
        self.gourdsFinalOrderInHCycle = self.myFinalHCycleOrderConfig.gourdsFinalOrderInHCycle
        self.leafType = -1
        self.leafIndex = -1

    def runPhaseTwoN3(self, buttonState4):
        if buttonState4 != 2: # running
            return False

        if self.myButtons.buttonStates[3] != 1:
            self.myButtons.buttonStates[4] = 0
            print("Phase 1 should be finished first!")
            self.redrawTheScreen()
            return False


        print("Phase two O(n^3) is running")

        resultOfSort = False


        # gourdsOrderInHCycleGenerator
        if len(self.gourdsFinalOrderInHCycle) <= 0:
            self.gourdsFinalOrderInHCycleGetter()



        # search type one
        self.leafIndex, threeConnection = self.searchLeafInTypeOne()
        if self.leafIndex != -1:
            self.leafType = 1
            print("\t", self.HCycleAux[self.leafIndex], "is the x of leaf type one")
            resultOfSort = self.typeOneInsertionSort(self.leafIndex)
            self.typeOneCheckTheDirectionOfGourds(self.leafIndex, threeConnection)

        else:
            # search type two
            self.leafIndex = self.searchLeafInTypeTwo()
            if self.leafIndex != -1:
                self.leafType = 2
                resultOfSort = self.typeTwoBubbleSort(self.leafIndex)



        self.myButtons.buttonStates[4] = 1  # finished
        self.myButtons.buttonStates[5] = 1  # finished
        self.redrawTheScreen()
        if not resultOfSort: print("---WARN--- Something went wrong in Phase 2 O(n^3)!")


        print("Phase two finished!")
        return resultOfSort

    def cellChecking(self, aCell):
        isEmpty = True
        gourdsIndexInHCycle = -1
        for aGourds in self.myBoardsConfig.gourdsList:
            gourdsIndexInHCycle += 1
            if (aCell[0] == aGourds[0] and aCell[1] == aGourds[1]):
                isEmpty = False
                break
            elif (aCell[0] == aGourds[2] and aCell[1] == aGourds[3]):
                isEmpty = False
                break
        if isEmpty:
            return True, -1
        return False, gourdsIndexInHCycle

    def movesGourdsCClockwiseAlongACycle(self, aCycleDup):
        lenOfACycle = int(len(aCycleDup) / 2)

        for i in range(lenOfACycle):
            if self.cellChecking(aCycleDup[i])[0]:
                self.movesAGourdAloneTheACycle(aCycleDup, i)
                return

    def movesAGourdAloneTheACycle(self, aCycleDup, cycleIndex):

        # move first part
        cycleIndex += 1
        gourdsIndex, partIndex = self.myGourdsConstructor.gourdsClicked(aCycleDup[cycleIndex], 'al')
        if gourdsIndex == -1:
            print ("---WARN--- No these gourds found!")
            return False

        # check if the next part is along the HCycle
        if (self.myBoardsConfig.gourdsList[gourdsIndex][2-partIndex] == aCycleDup[cycleIndex][0]
                and self.myBoardsConfig.gourdsList[gourdsIndex][2-partIndex+1] == aCycleDup[cycleIndex][1]):
            # is along the HCycle
            pass
        else:
            # is not along the HCycle
            nextPartofGourds = self.myBoardsConfig.gourdsList[gourdsIndex][2-partIndex], self.myBoardsConfig.gourdsList[gourdsIndex][2-partIndex+1]
            # move the next part
            self.myGourdsConstructor.gourdsClicked(nextPartofGourds, 'al')

        self.redrawTheScreen()

    def gourdsFinalOrderInHCycleGetter(self):
        return self.gourdsFinalOrderInHCycle

    def gourdsPresentOrderAndDirectionInHCycleGetter(self):
        order = []
        directionDict = {}
        for cell in self.myHamiltonianCycle.hamiltonianCycleStack:
            for i in range(self.myFinalGourdsConfig.totalNumberOfGourds):
                if i not in order:
                    gourd = self.myBoardsConfig.gourdsList[i]
                    if gourd[0] == cell[0] and gourd[1] == cell[1]:
                        order.append(i)
                        directionDict[i] = 0
                        break
                    elif gourd[2] == cell[0] and gourd[3] == cell[1]:
                        order.append(i)
                        directionDict[i] = 1
                        break

        return order, directionDict

    def gourdsOrderedWithOffset(self):
        # measure the offset
        presentGourdsOrder = self.gourdsPresentOrderAndDirectionInHCycleGetter()[0]
        offset = 0
        for i in range(len(presentGourdsOrder)):
            if presentGourdsOrder[i] == self.gourdsFinalOrderInHCycle[0]:
                offset = i
                break
        # check if the offset valid
        duplicatePresentGourdsOrder = presentGourdsOrder * 2
        result = True
        for i in range(len(presentGourdsOrder)):
            if not duplicatePresentGourdsOrder[i + offset] == self.gourdsFinalOrderInHCycle[i]:
                result = False

                break
        return result

    def searchLeafInTypeOne(self):
        HCycleIndex = -1
        threeConnection = -1

        # calculate the distance between i+0 and i+3
        for i in range(self.myHamiltonianCycle.lengthOfHCycle):
            diffInX = self.HCycleAux[i][0] - self.HCycleAux[i+3][0]
            diffInY = self.HCycleAux[i][1] - self.HCycleAux[i+3][1]
            squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
            if squaredDistance <= 4:
                HCycleIndex = i

                break

        diffInX = self.HCycleAux[HCycleIndex][0] - self.HCycleAux[HCycleIndex + 2][0]
        diffInY = self.HCycleAux[HCycleIndex][1] - self.HCycleAux[HCycleIndex + 2][1]
        squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
        if squaredDistance <= 4:
            threeConnection = 12
        else:
            threeConnection = 123

        return HCycleIndex, threeConnection

    def searchLeafInTypeTwo(self):
        HCycleIndex = -1


        for i in range(self.myHamiltonianCycle.lengthOfHCycle):
            # calculate the distance between i+0 and i+2
            diffInX = self.HCycleAux[i][0] - self.HCycleAux[i + 2][0]
            diffInY = self.HCycleAux[i][1] - self.HCycleAux[i + 2][1]
            squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
            if squaredDistance <= 4:
                # calculate the distance between i+0 and i+4
                diffInX = self.HCycleAux[i][0] - self.HCycleAux[i + 4][0]
                diffInY = self.HCycleAux[i][1] - self.HCycleAux[i + 4][1]
                squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
                if squaredDistance <= 4:
                    # calculate the distance between i+2 and i+4
                    diffInX = self.HCycleAux[i + 2][0] - self.HCycleAux[i + 4][0]
                    diffInY = self.HCycleAux[i + 2][1] - self.HCycleAux[i + 4][1]
                    squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
                    if squaredDistance <= 4:
                        return i

        return HCycleIndex

    def typeOneInsertionSort(self, cellIndexInHCycle):
        # this is not really an Insertion Sort, it just an Insertion Sort-like algorithms

        # initialization
        HCycleDup = self.myHamiltonianCycle.hamiltonianCycleStack * 2
        HPrimeCycleDup = copy.copy(self.myHamiltonianCycle.hamiltonianCycleStack)
        HPrimeCycleDup.pop(cellIndexInHCycle + 2)
        HPrimeCycleDup.pop(cellIndexInHCycle + 1)
        HPrimeCycleDup = HPrimeCycleDup * 2
        print("\tThe order of gourds now: ", self.gourdsPresentOrderAndDirectionInHCycleGetter())




        while(True):
            presentGourdsOrder = self.gourdsPresentOrderAndDirectionInHCycleGetter()[0]

            lenOfACycle = int(len(HCycleDup) / 2)


            # check if it is done (but with an offset)
            if self.gourdsOrderedWithOffset():
                print("\tThe order of gourds now: ", self.gourdsPresentOrderAndDirectionInHCycleGetter())
                return True



            # insertion
            # Ensure Gourds In Proper Places
            self.typeOneEnsureGourdsInProperPlaces(HCycleDup, cellIndexInHCycle, HPrimeCycleDup)

            # get the index of x + 1
            gourdsIndexAtXPlusOne = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 1][0], HCycleDup[cellIndexInHCycle + 1][1])[0]

            gourdsIndexShouldBeAtX = -1





            # don't align 0
            if gourdsIndexAtXPlusOne == 0:
                self.movesGourdsCClockwiseAlongACycle(HCycleDup)
                continue



            for i in range(lenOfACycle):
                if gourdsIndexAtXPlusOne == self.gourdsFinalOrderInHCycle[i]:
                    gourdsIndexShouldBeAtX = self.gourdsFinalOrderInHCycle[i-1]
                    break


            # get the index of x really be
            if self.cellChecking(HCycleDup[cellIndexInHCycle + 0])[0]:
                gourdsIndexAtX = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle - 1][0], HCycleDup[cellIndexInHCycle - 1][1])[0]
            else:
                gourdsIndexAtX = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 0][0], HCycleDup[cellIndexInHCycle + 0][1])[0]


            while not (gourdsIndexAtX == gourdsIndexShouldBeAtX):
                self.movesGourdsCClockwiseAlongACycle(HPrimeCycleDup)

                if self.cellChecking(HCycleDup[cellIndexInHCycle + 0])[0]:
                    gourdsIndexAtX = \
                    self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle - 1][0],
                                                                    HCycleDup[cellIndexInHCycle - 1][1])[0]
                else:
                    gourdsIndexAtX = \
                    self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 0][0],
                                                                    HCycleDup[cellIndexInHCycle + 0][1])[0]

                # print("\tThe order of gourds now: ", self.gourdsPresentOrderInHCycleGetter(), "gourdsIndexAtX+1: ", gourdsIndexAtXPlusOne,
                #       "gourdsIndexAtX: ", gourdsIndexAtX, "gourdsIndexAtX should be: ", gourdsIndexShouldBeAtX)


            # self.typeOneEnsureGourdsInProperPlaces(HCycleDup, cellIndexInHCycle, HPrimeCycleDup)

            for i in range(lenOfACycle):
                if self.cellChecking(HCycleDup[i])[0]:
                    self.movesAGourdAloneTheACycle(HCycleDup, i)
                    break
            print("\tThe order of gourds now: ", self.gourdsPresentOrderAndDirectionInHCycleGetter())



        return True

    def typeOneEnsureGourdsInProperPlaces(self, HCycleDup, cellIndexInHCycle, HPrimeCycleDup):
        # moves a pair of gourds at the leaf (x+1) and (x+2)
        tempOne = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 1][0],
                                                                  HCycleDup[cellIndexInHCycle + 1][1])
        tempTwo = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 2][0],
                                                                  HCycleDup[cellIndexInHCycle + 2][1])
        while not (tempOne[0] == tempTwo[0]):
            self.movesGourdsCClockwiseAlongACycle(HCycleDup)

            tempOne = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 1][0],
                                                                      HCycleDup[cellIndexInHCycle + 1][1])
            tempTwo = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 2][0],
                                                                      HCycleDup[cellIndexInHCycle + 2][1])

        # make sure not a pair of gourds at the leaf (x+0) and (x+3)
        tempOne = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 0][0],
                                                                  HCycleDup[cellIndexInHCycle + 0][1])
        tempTwo = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 3][0],
                                                                  HCycleDup[cellIndexInHCycle + 3][1])
        while (tempOne[0] == tempTwo[0]):
            self.movesGourdsCClockwiseAlongACycle(HPrimeCycleDup)

            tempOne = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 0][0],
                                                                      HCycleDup[cellIndexInHCycle + 0][1])
            tempTwo = self.myGourdsConstructor.gourdsSearchingByIndex(HCycleDup[cellIndexInHCycle + 3][0],
                                                                      HCycleDup[cellIndexInHCycle + 3][1])

    def typeOneCheckTheDirectionOfGourds(self, leafIndex, threeConnection):

        targetDirectionDict = self.myFinalHCycleOrderConfig.gourdsFinalDirectionInHCycle
        orderList, directionDict = self.gourdsPresentOrderAndDirectionInHCycleGetter()
        # print("targetDirectionDict: ",targetDirectionDict)
        # print("directionDict: ",directionDict)



        # main loop L326
        whileCounterMainLoop = 0
        while not targetDirectionDict == directionDict:
            whileCounterMainLoop += 1
            # print("targetDirectionDict: ", targetDirectionDict)
            # print("directionDict: ", directionDict)

            indexOfGourdsShouldChangeDirection = -1
            # identify the gourds with opposite direction
            for i in range(len(self.myBoardsConfig.gourdsList)):
                if not targetDirectionDict.get(i) == directionDict.get(i):
                    indexOfGourdsShouldChangeDirection = i
                    break
            if indexOfGourdsShouldChangeDirection == -1:
                print("---WARN--- Something went wrong in direction detection")
                return False



            # move these gourds into the leaf (x+1) and (x+2)
            indexOfGourdsNow, tempX, tempY = self.myGourdsConstructor.gourdsSearchingByIndex(self.HCycleAux[leafIndex+1][0], self.HCycleAux[leafIndex+1][1])
            if threeConnection == 12: isEmptyPrepared = self.cellChecking(self.HCycleAux[leafIndex + 0])[0]
            elif threeConnection == 123: isEmptyPrepared = self.cellChecking(self.HCycleAux[leafIndex + 3])[0]

            # while loop phaseTwoN3 L350
            whileCounter2 = 0
            while not (indexOfGourdsNow == indexOfGourdsShouldChangeDirection and isEmptyPrepared):
                whileCounterMainLoop = 0
                whileCounter2 += 1
                self.movesGourdsCClockwiseAlongACycle(self.HCycleAux)

                # Ending: refresh the present gourds at leaf
                if threeConnection == 12:
                    isEmptyPrepared = self.cellChecking(self.HCycleAux[leafIndex + 0])[0]
                elif threeConnection == 123:
                    isEmptyPrepared = self.cellChecking(self.HCycleAux[leafIndex + 3])[0]

                indexOfGourdsNow, tempX, tempY = self.myGourdsConstructor.gourdsSearchingByIndex(
                    self.HCycleAux[leafIndex+1][0], self.HCycleAux[leafIndex+1][1])

                # print("isEmptyPrepared", isEmptyPrepared)
                # print("indexOfGourdsNow", indexOfGourdsNow)
                # print("indexOfGourdsShouldChangeDirection", indexOfGourdsShouldChangeDirection)

                # while counter checking
                if whileCounter2 > len(self.HCycleAux)*len(self.HCycleAux):
                    print("---WARN--- Infinitely while loop in phaseTwoN3 L350")
                    return False


            # change direction
            self.typeOneChangeGourdsDirection(leafIndex, threeConnection)

            # Ending: refresh the present dict
            orderList, directionDict = self.gourdsPresentOrderAndDirectionInHCycleGetter()

            # while counter checking
            if whileCounterMainLoop > len(self.HCycleAux)*len(self.HCycleAux):
                print("---WARN--- Infinitely while loop in phaseTwoN3 L326")
                return False


        return True

    def typeOneChangeGourdsDirection(self, leafIndex, threeConnection):
        # print("\tChange the direction! threeConnection: ", threeConnection, "cellIndexInHCycle: ", leafIndex)


        if threeConnection == 123:
            if not self.cellChecking(self.HCycleAux[leafIndex + 3])[0]:
                return False
            print(leafIndex + 3, " is empty")
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 1], 'al')
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 2], 'al')
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 3], 'al')


        elif threeConnection == 12:
            if not self.cellChecking(self.HCycleAux[leafIndex + 0])[0]:
                return False
            print(leafIndex, " is empty")
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 2], 'al')
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 1], 'al')
            self.myGourdsConstructor.gourdsClicked(self.HCycleAux[leafIndex + 0], 'al')

        else:
            print("---WARN--- Something went wrong in direction changing!")
            return False


        return True

    def typeTwoBubbleSort(self, cellIndexInHCycle):
        # this is also not really a Bubble Sort, it just a Bubble Sort-like algorithm.
        # TODO

        return True

    def redrawTheScreen(self):

        self.screen.fill(self.myBoardsConfig.coloursLibrary['backGround'])
        self.myButtons.buttonConstructor()
        self.myCellsConstructor.cellsAndAxisConstructor(self.myButtons.buttonStates[1])
        self.myGourdsConstructor.gourdsConstructor(self.myButtons.buttonStates[1])
        self.myHamiltonianCycle.hamiltonianCycleDrawer(self.myButtons.buttonStates[2])

        offset = self.myHamiltonianCycle.offset
        widthOfHexCell = self.myHamiltonianCycle.widthOfHexCell
        # draw the sub H-cycle


        if self.leafType == 1:
            pygame.draw.line(self.screen, self.myBoardsConfig.coloursLibrary['backGround'],
                             (int(offset + self.HCycleAux[self.leafIndex][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex][1] * widthOfHexCell * 1.732)),
                             (int(offset + self.HCycleAux[self.leafIndex + 3][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex + 3][1] * widthOfHexCell * 1.732)),
                             4)
            pygame.draw.line(self.screen, self.myBoardsConfig.coloursLibrary['hamiltonianCycle'],
                             (int(offset + self.HCycleAux[self.leafIndex][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex][
                                  1] * widthOfHexCell * 1.732)),
                             (int(offset + self.HCycleAux[self.leafIndex + 3][
                                 0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex + 3][
                                  1] * widthOfHexCell * 1.732)),
                             2)

        if self.leafType == 2:
            pygame.draw.line(self.screen, self.myBoardsConfig.coloursLibrary['backGround'],
                             (int(offset + self.HCycleAux[self.leafIndex][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex][1] * widthOfHexCell * 1.732)),
                             (int(offset + self.HCycleAux[self.leafIndex + 4][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex + 4][1] * widthOfHexCell * 1.732)),
                             4)
            pygame.draw.line(self.screen, self.myBoardsConfig.coloursLibrary['hamiltonianCycle'],
                             (int(offset + self.HCycleAux[self.leafIndex][0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex][
                                  1] * widthOfHexCell * 1.732)),
                             (int(offset + self.HCycleAux[self.leafIndex + 4][
                                 0] * widthOfHexCell),
                              int(offset + self.HCycleAux[self.leafIndex + 4][
                                  1] * widthOfHexCell * 1.732)),
                             2)


        pygame.display.update()

