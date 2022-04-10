import math
maxNodeSize = 0
nodesVisited=0
eContainsQ = 0
insideQ = 0
numberOfIntersects = 0

class Node():
    def __init__(self , isLeaf = None):
        self.entriesList = [] ## a listo keep entries of a node
        self.nodeMBR = [] ##the actual szie of a node produced by its entries
        self.isLeaf = isLeaf ## check if it is a leaf 1 if it is gives as

    def getMBR(self):
        MBR = [0, math.inf, -math.inf, math.inf, -math.inf]
        #Calculates the size of boundrys of the node by the entries
        for i in self.entriesList:
            if (i[1] < MBR[1]): ##xl<if
                MBR[1] = i[1]
            if (i[2] > MBR[2]):##xh >
                MBR[2] = i[2]
            if (i[3] < MBR[3]):
                MBR[3] = i[3]
            if (i[4] > MBR[4]):
                MBR[4] = i[4]
        self.nodeMBR = MBR
        return self.nodeMBR

    def getArea(self):
        if (len(self.nodeMBR) == 0):
            self.getMBR()

        a = math.sqrt( pow(self.nodeMBR[2] - self.nodeMBR[1] ,2) + pow(self.nodeMBR[3] - self.nodeMBR[3],2) )
        b = math.sqrt( pow(self.nodeMBR[1] - self.nodeMBR[1] ,2) + pow(self.nodeMBR[4] - self.nodeMBR[3],2) )
        return a * b
    def update(self,objectID , entriesID): ##used in reversing the tree
        if (self.isLeaf == None):
            entriesID = entriesID + len(self.entriesList)-1
            for i in self.entriesList:
                i[0] = entriesID
                entriesID = entriesID - 1
        else:
            for i in range(0 , len(self.entriesList)):
                self.entriesList[i][0] = int( self.entriesList[i][0] )# objectID of leaf are turned to int

    def getEntries(self): #returns the list of entries
        return self.entriesList

    def entriesSize(self): #returns how many entries we have at most 28 based on calculations made
        return len(self.entriesList)

    def addMBR(self,MBR): #we add an MBR to node ,at the entriesList is where we add them
        self.entriesList.append(MBR)   # return 1 or 0 in case the node is full

        if (len(self.entriesList) == maxNodeSize):
            return 1
        else:
            return 0

    def leafCheck(self): #returns 1 if is a leaf
        if (self.isLeaf == None):
            return 0
        else:
            return self.isLeaf

def loadRectanglesFile(filePath): ##load rectangles from a file used for quer_rectangles.txt and data_rectangles
    file = open(filePath ,'r' , encoding = 'utf-8')
    rectangleList = []
    for rectangle in file:
        tempRectangle = rectangle.replace("\n", "").split("\t")
        tempRectangle = [float(i) for i in tempRectangle] #turn loaded data to float
        rectangleList.append(tempRectangle)
    file.close()
    return rectangleList

def sortRectangles(rectanglesList):
    global maxNodeSize

    rectanglesList = sorted(rectanglesList,key=lambda x: x[1]) #sort by xlow
    maxNodeSize = math.floor(1024 / 36) #calculate the node size
    print("Node size:", maxNodeSize)
    leafCount = math.ceil( len(rectanglesList) / maxNodeSize)  #calculate leaf
    print("Number of leafs:", leafCount)
    slice = math.ceil( math.sqrt( leafCount ) ) * maxNodeSize #calcualte slices to short ylow by
    print("Slice:",slice)
    temp = []
    sortedList = []
    for i in range (0 , len(rectanglesList)):
        temp.append(rectanglesList[i])
        if ( i %  slice == 0): ##  count number of rectangles loaded to be sorted by ylow
            temp = sorted(temp, key=lambda x: x[3])
            sortedList = sortedList + temp
            temp.clear()
    temp = sorted(temp, key=lambda x: x[3]) #sort rest of the rectangles that are les than slice number
    sortedList = sortedList + temp

    return sortedList

def build(leafs):
    nodeslist = []
    level = 0
    totalArea = 0
    newnode = Node(1) #create a leaf node
    for i in listOfLeafs: #for every leaf in listofLeafs
        if ( newnode.addMBR(i) ): ## we add a leaf to the leafnode in the class we check every time if maxentries where aded to the entrie if yes the it return 1 so we can enter in if
            totalArea = totalArea +newnode.getArea()
            nodeslist.append(newnode) ##since the node is full we add it to the list f nodes
            newnode = Node(1) #we create a new leaf node that is empty
    nodeslist.append(newnode) ##we ad the last node that it may not be full
    totalArea = totalArea + newnode.getArea()
    newnode = Node() #create new empty node
    counter = 0
    level = level + 1
    print('Level ',level , ' nodes ',len(nodeslist) , ' area ',totalArea/len(nodeslist))
    totalArea = 0


    while (1): #for the nodes that are not leafs we build the rest of the tree
        nodesCount = len(nodeslist)
        for i in range(counter , nodesCount): #for the node from the counter to the node of the curent level we build the uper level
            mbr=nodeslist[i].getMBR() # get the mdbr of all the entries  of the curent node
            mbr[0] = i #pointer to the node
            counter = counter +1
            if (newnode.addMBR(mbr)): #if node is full get in if
                totalArea = totalArea + newnode.getArea()
                nodeslist.append(newnode) #add node to nodes list
                newnode = Node() #new empty node
        nodeslist.append(newnode) #we ad the last node that it may not be full
        totalArea = totalArea + newnode.getArea()
        newnode = Node() #new empty node
        level = level + 1
        print('Level ', level, ' nodes ', len(nodeslist) - nodesCount , ' area ',totalArea/(len(nodeslist) - nodesCount))
        nodesCount = len(nodeslist) #update the counter for the if se we can make the uper level for the nodes we just aded
        totalArea = 0
        if ( nodesCount - counter <maxNodeSize): #whene we have les than full ode to create next level wich is root
            for i in range(counter , nodesCount):
                mbr = nodeslist[i].getMBR()
                mbr[0] = i
                newnode.addMBR(mbr)
            totalArea = totalArea +newnode.getArea()
            nodeslist.append(newnode)

            level = level + 1
            print('Level ', level, ' nodes ', len(nodeslist) - nodesCount ,' area ',totalArea/ (len(nodeslist)-nodesCount))
            break #break since root is created

    rTree=reversTree(nodeslist)# function used to reverse list cause the root will be in the last elemnt of the list insted of the first
    writeR_Tree(rTree , level)
    return rTree

def reversTree(nodeslist):
    counter = 0
    nodesUpdate = 1
    reverseTreeList =[]
    for i in range(len(nodeslist)-1 , -1, -1): ##start from the last element and go to the first
        node = nodeslist[i] # we get the node
        node.update(counter,nodesUpdate) #update the node pointers
        reverseTreeList.append( node ) ##ad node to the new reversed list
        nodesUpdate = nodesUpdate + reverseTreeList[counter].entriesSize() #update entries based on the number of entries before
        counter = counter + 1
    return reverseTreeList

def writeR_Tree(tree, level):#write r tree
    file = open('rtree.txt', 'w' ,encoding = 'utf-8') # open file to write
    text = ''
    file.write('root-id=0\n')
    file.write('levels='+str(level)+'\n')
    for i in  range(len(tree) ): #loop throu all nodes ony by one
        node = tree[i] #get node
        text = 'node-id='+ str(i) + ' [' # write node id
        entries = node.getEntries() #get all entries of node
        for x in entries: #loop throu entries
            text = text +  '('+str(x[0])+ ', ('+str(x[1])+','+str(x[2])+','+str(x[3])+','+str(x[4])+')),' + ' ' #write entries of nodes
        text = list(text) # list string to corect some mistakes cause of loop
        text.pop(-1) #delete last ' '
        text.pop(-1) #delete ,
        text = ''.join(text)#join text list
        file.write(text+']\n') #write to file
    file.close() #close file

def equals(W,e): #if one rectangles ia equal to another one

    if (W[1] == e[1] and W[2] == e[2]  and W[3] == e[3] and W[4] == e[4]):
        return 1
    else:
        return 0

def contains(W,e):
    # e is in W
    if (W[1] < e[1] < W[2] and W[1] < e[2] < W[2]):
        if (W[3] < e[3] < W[4] and W[3] < e[4] < W[4] ):
            return 1
    return 0

def intersects(W,MBR):
    global numberOfIntersects,insideQ,eContainsQ
    if (equals(W,MBR) == 1) : #if they are equals
        return 1
    if (contains( W , MBR ) == 1 ): #if W contains MBR
        return 1
    if (contains( MBR , W)  == 1 ): #if MBR contains W
        return 1
    #reverse logic if the one is on top/down of the other or left/righ
    if ( W[2] < MBR[1] or MBR[2] < W[1]):
        return 0
    elif (W[3] > MBR[4] or MBR[3] > W[4]):
        return 0
    else:
        return 1
##Range quary based on algorithm
##3 diferent for every question on the exercise
def range_query_q1(W,node):
    global nodesVisited , numberOfIntersects
    entries = node.getEntries()
    nodesVisited = nodesVisited + 1
    if ( node.leafCheck() == 0 ):
        for e in entries:
            if (intersects(W,e) == 1):
                node = r_Tree[e[0]]
                range_query_q1(W,node)
    elif( node.leafCheck() ):
        for e in entries:
            if ( intersects(W,e) ):
                numberOfIntersects = numberOfIntersects +1

def range_query_q2(W,node):
    global nodesVisited , insideQ
    entries = node.getEntries()
    nodesVisited = nodesVisited + 1
    if ( node.leafCheck() == 0 ):
        for e in entries:
            if (intersects(W,e) == 1):
                node = r_Tree[e[0]]
                range_query_q2(W,node)
    elif( node.leafCheck()  ):
        for e in entries:
            if ( contains(W,e)  ):
                insideQ = insideQ +1

def range_query_q3(W,node):
    global nodesVisited , eContainsQ
    entries = node.getEntries()
    nodesVisited = nodesVisited + 1
    if ( node.leafCheck() ==0 ):
        for e in entries:
            if (intersects(W,e) == 1):
                node = r_Tree[e[0]]
                range_query_q3(W,node)
    elif( node.leafCheck() ):
        for e in entries:
            if ( contains(e,W) == 1 ):
                eContainsQ = eContainsQ + 1

def quarys():##funtion for quarys
    global nodesVisited ,numberOfIntersects, insideQ , eContainsQ
    root = r_Tree[0] #get root
    for W in queryList:#for every quary
        #run the 3 functions one for every question and print results
        print('Query:', int(W[0]))
        range_query_q1(W, root)
        print('Nodes visited: ', nodesVisited, ' results for Range intersection query ', numberOfIntersects)
        nodesVisited = 0
        range_query_q2(W, root)
        print('Nodes visited: ', nodesVisited, ' results for Range inside query ', insideQ)
        nodesVisited = 0
        range_query_q3(W, root)
        print('Nodes visited: ', nodesVisited, ' results Containment query ', eContainsQ)
        nodesVisited = 0
        numberOfIntersects = 0
        insideQ = 0
        eContainsQ = 0


queryList = loadRectanglesFile('query_rectangles.txt') #Load file
rectanglesList = loadRectanglesFile('data_rectangles.txt') # Load file
listOfLeafs = sortRectangles(rectanglesList) #Sort rectangles
r_Tree = build(listOfLeafs) #build tree
quarys() #run the quarys



