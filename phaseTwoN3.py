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


    def runPhaseTwoN3(self, buttonState4):
        if buttonState4 != 2: # running
            self.firstRun = True
            return
        print("Phase two O(n^3) is running")


        #TODO
















        self.myButtons.buttonStates[4] = 1  # finished
        self.myButtons.buttonStates[5] = 1  # finished
        self.myGourdsConstructor.gourdsClicked([ 4, 2], 'a')
        self.redrawTheScreen()


    def redrawTheScreen(self):

        self.screen.fill(self.myBoardsConfig.coloursLibrary['backGround'])
        self.myButtons.buttonConstructor()
        self.myCellsConstructor.cellsAndAxisConstructor(self.myButtons.buttonStates[1])
        self.myGourdsConstructor.gourdsConstructor(self.myButtons.buttonStates[1])
        self.myHamiltonianCycle.hamiltonianCycleDrawer(self.myButtons.buttonStates[2])

        pygame.display.update()
