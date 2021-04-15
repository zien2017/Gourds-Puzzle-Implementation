import pygame

class phaseTwoN3(object):

    def __init__(self, screen, myBoardsConfig, myButtons, myCellsConstructor, myGourdsConstructor, myHamiltonianCycle, myFinalGourdsConfig):
        self.screen = screen
        self.myBoardsConfig = myBoardsConfig
        self.myButtons = myButtons
        self.myCellsConstructor = myCellsConstructor
        self.myGourdsConstructor = myGourdsConstructor
        self.myHamiltonianCycle = myHamiltonianCycle
        self.myFinalGourdsConfig = myFinalGourdsConfig
        self.HCycleAux = self.myHamiltonianCycle.HCycleAux
        self.firstRunFlag = True
        self.gourdsOrderInHCycle = []

    def runPhaseTwoN3(self, buttonState4):
        if buttonState4 != 2: # running
            return False

        if self.myButtons.buttonStates[3] != 1:
            self.myButtons.buttonStates[4] = 0
            print("Phase 1 should be finished first!")
            self.redrawTheScreen()
            return False


        print("Phase two O(n^3) is running")

        result = False


        # gourdsOrderInHCycleGenerator
        if len(self.gourdsOrderInHCycle) <= 0:
            self.gourdsFinalOrderInHCycleGenerator()


        # search type two
        cellIndexInHCycle = self.searchLeafInTypeTwo()
        if cellIndexInHCycle != -1:
            print("\t", self.HCycleAux[cellIndexInHCycle], "is the x of leaf type two")
            result = self.typeTwoBubbleSort(cellIndexInHCycle)


        else:
            # search type one
            cellIndexInHCycle = self.searchLeafInTypeOne()
            if cellIndexInHCycle != -1:
                print("\t", self.HCycleAux[cellIndexInHCycle], "is the x of leaf type one")
                result = self.typeOneInsertionSort(cellIndexInHCycle)



        self.myButtons.buttonStates[4] = 1  # finished
        self.myButtons.buttonStates[5] = 1  # finished
        self.redrawTheScreen()
        if not result: print("---WARN--- Something went wrong in Phase 2 O(n^3)!")
        return result





    def gourdsFinalOrderInHCycleGenerator(self):
        orderlist = []

        for cell in self.myHamiltonianCycle.hamiltonianCycleStack:
            for i in range(self.myFinalGourdsConfig.totalNumberOfGourds):
                if i not in orderlist:
                    gourd = self.myFinalGourdsConfig.gourdsAssignedDict.get(i)
                    if gourd[1] == cell[0] and gourd[2] == cell[1]:
                        orderlist.append(i)
                        break
                    elif gourd[3] == cell[0] and gourd[4] == cell[1]:
                        orderlist.append(i)
                        break

        print("\tThe order of gourds should be reached in phase 2: ",orderlist)
        self.gourdsOrderInHCycle = orderlist
        return self.gourdsOrderInHCycle

    def gourdsPresentOrderInHCycle(self):
        order = []
        for cell in self.myHamiltonianCycle.hamiltonianCycleStack:
            for i in range(self.myFinalGourdsConfig.totalNumberOfGourds):
                if i not in order:
                    gourd = self.myBoardsConfig.gourdsList[i]
                    if gourd[0] == cell[0] and gourd[1] == cell[1]:
                        order.append(i)
                        break
                    elif gourd[2] == cell[0] and gourd[3] == cell[1]:
                        order.append(i)
                        break

        return order


    def searchLeafInTypeOne(self):
        HCycleIndex = -1

        # calculate the distance between i+0 and i+3
        for i in range(self.myHamiltonianCycle.lengthOfHCycle):
            diffInX = self.HCycleAux[i][0] - self.HCycleAux[i+3][0]
            diffInY = self.HCycleAux[i][1] - self.HCycleAux[i+3][1]
            squaredDistance = diffInX * diffInX + diffInY * diffInY * 1.732 * 1.732
            if squaredDistance <= 4:
                return i

        return HCycleIndex

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
        #TODO

        print("\tThe order of gourds right now: ", self.gourdsPresentOrderInHCycle())



        # while(True):
        presentGourdsOrder = self.gourdsPresentOrderInHCycle()
        if(self.gourdsOrderInHCycle == presentGourdsOrder):
            return True
        else:
            # check if there's an offset

            # measure the offset
            offset = 0
            for i in range(len(presentGourdsOrder)):
                if presentGourdsOrder[i] == self.gourdsOrderInHCycle[0]:
                    offset = i
                    break
            # check if the offset valid
            duplicatePresentGourdsOrder = presentGourdsOrder*2
            isAllDone = True
            for i in range(len(presentGourdsOrder)):
                if not duplicatePresentGourdsOrder[i + offset] == self.gourdsOrderInHCycle[i]:
                    isAllDone = False

                    break
            print(isAllDone)










            pass

        # self.myGourdsConstructor.gourdsClicked([4, 2], 'al')
        return True

    def typeTwoBubbleSort(self, cellIndexInHCycle):
        # this is also not really a Bubble Sort, it just a Bubble Sort-like algorithm.
        #TODO


        return True

    def redrawTheScreen(self):

        self.screen.fill(self.myBoardsConfig.coloursLibrary['backGround'])
        self.myButtons.buttonConstructor()
        self.myCellsConstructor.cellsAndAxisConstructor(self.myButtons.buttonStates[1])
        self.myGourdsConstructor.gourdsConstructor(self.myButtons.buttonStates[1])
        self.myHamiltonianCycle.hamiltonianCycleDrawer(self.myButtons.buttonStates[2])

        pygame.display.update()

