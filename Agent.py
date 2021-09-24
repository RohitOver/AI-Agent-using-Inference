"""
Logical Agent for programming assignment 2.
"""

class Agent:
    def __init__(self):
        self._mineFieldWorld = [
                 ['M','','',''], # Rooms [1,4] to [4,4]
                 ['M','','',''], # Rooms [1,3] to [4,3]
                 ['','','M','M'], # Rooms [1,2] to [4,2] 
                 ['','','','M'],  # Rooms [1,1] to [4,1]
                ] # This is the mine field world shown in the assignment question.
                  # A different instance of the mine field world will be used for evaluation.
        self._curLoc = [1,1]
        self._isAlive = True
        self._hasExited = False

    def _FindIndicesForLocation(self,loc):
        x,y = loc
        i,j = 4-y, x-1
        return i,j

    def _CheckForMine(self):
        mf = self._mineFieldWorld
        i,j = self._FindIndicesForLocation(self._curLoc)
        if 'M' in mf[i][j]:
            print(mf[i][j])
            self._isAlive = False
            print('Agent is DEAD.')
        return self._isAlive

    def TakeAction(self,action): # The function takes an action and returns whether the Agent is alive
                                # after taking the action.
        validActions = ['Up','Down','Left','Right']
        assert action in validActions, 'Invalid Action.'
        if self._isAlive == False:
            print('Action cannot be performed. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return False
        if self._hasExited == True:
            print('Action cannot be performed. Agent has exited the Mine field world.'.format(self._curLoc))
            return False

        index = validActions.index(action)
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        move = validMoves[index]
        newLoc = []
        for v, inc in zip(self._curLoc,move):
            z = v + inc #increment location index
            z = 4 if z>4 else 1 if z<1 else z #Ensure that index is between 1 and 4
            newLoc.append(z)
        self._curLoc = newLoc
        print('Action Taken: {0}, Current Location {1}'.format(action,self._curLoc))
        if self._curLoc[0]==4 and self._curLoc[1]==4:
            self._hasExited=True
        return self._CheckForMine()
    
    def _FindAdjacentRooms(self):
        cLoc = self._curLoc
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        adjRooms = []
        for vM in validMoves:
            room = []
            valid = True
            for v, inc in zip(cLoc,vM):
                z = v + inc
                if z<1 or z>4:
                    valid = False
                    break
                else:
                    room.append(z)
            if valid==True:
                adjRooms.append(room)
        return adjRooms
                
        
    def PerceiveCurrentLocation(self): #This function perceives the current location. 
                                        #It detects whether mine is present in adjacent rooms.
        percept = None
        mf = self._mineFieldWorld
        if self._isAlive == False:
            print('Agent cannot perceive. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return None
        if self._hasExited == True:
            print('Agent cannot perceive. Agent has exited the Mine field World.'.format(self._curLoc))
            return None

        adjRooms = self._FindAdjacentRooms()
        count=0
        for room in adjRooms:
            i,j = self._FindIndicesForLocation(room)
            if 'M' in mf[i][j]:
                count+=1
        percept = '=0' if count==0 else '=1' if count==1 else '>1'
        return percept
    
    def FindCurrentLocation(self):
        return self._curLoc

def main():
    ag = Agent()
    print('curLoc',ag.FindCurrentLocation())
    print('Percept ',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Left')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())


if __name__=='__main__':
    main()  