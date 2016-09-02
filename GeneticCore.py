from random import randint
from queue import Queue

class Node:
    def __init__(self,value,level,leftChildNode,rightChildNode,leaf=False):
        self.value=value
        self.level=level
        self.leftChildNode=leftChildNode
        self.rightChildNode=rightChildNode
        self.leaf=leaf
    def __init__(self,leaf=False):
        self=self
        self.leaf=leaf

class Tree:
    def __init__(self,maineNode):
        self.mainNode=maineNode
        self.nodes=[]

class Chromosome:
    def __init__(self,tree,fitness=0):
        self.fitness=fitness
        self.tree=tree


def ParseData(fileName):
    file=open(fileName)
    array=[]
    for line in file:
        innerArray=[]
        for char in line.rstrip():
            innerArray.append(char)
        array.append(innerArray)

    return  array

def CreateRandomPool(sizeOfPool):
    for i in range(0,sizeOfPool):
        nodesQueue=Queue()
        node=Node()
        node.parent=None
        node.level=0
        tree=Tree(node)
        nodes=tree.nodes
        nodes.append(node)
        chromosome=Chromosome(tree)
        pool.append(chromosome)

        nodesQueue.put(node)
        while (True):
            if (nodesQueue.empty()):
                break
            else:
                node=nodesQueue.get()
                if (node.level<2):
                    node.value=operators[randint(0,1)]
                    if (node.value=='&' or node.value=='|'):
                        tempNode=Node()
                        tempNode.parent=node
                        tempNode.level=node.level+1
                        node.rightChildNode=tempNode
                        nodesQueue.put(tempNode)
                        nodes.append(tempNode)
                        tempNode=Node()
                        tempNode.parent=node
                        tempNode.level=node.level+1
                        node.leftChildNode=tempNode
                        nodesQueue.put(tempNode)
                        nodes.append(tempNode)
                elif (node.level>=2):
                    node.value=operatorsAndOperands[randint(0,6)]
                    if (node.value=='&' or node.value=='|'):
                        tempNode=Node()
                        tempNode.parent=node
                        tempNode.level=node.level+1
                        node.rightChildNode=tempNode
                        nodesQueue.put(tempNode)
                        nodes.append(tempNode)
                        tempNode=Node()
                        tempNode.parent=node
                        tempNode.level=node.level+1
                        node.leftChildNode=tempNode
                        nodesQueue.put(tempNode)
                        nodes.append(tempNode)
                    else:
                        node.leaf=True

                elif  (node.level==4):
                    node.value=operands[randint(0,4)]
                    node.leaf=True

def CalculateFittnessOFthePool(valueDict,finallResult):
    for i in range(0,len(pool)):
        chromosome=pool[i]
        tree=chromosome.tree
        node=tree.mainNode
        operationStack=[]

        readyStateNode=None

        if(not node.leaf):
            operationStack.append(node)
        result=0
        while(len(operationStack)!=0):
            node=operationStack.pop()
            if(node.leaf and readyStateNode != None):
                operatorNode=operationStack.pop()
                if (operatorNode=='&'):
                    result=valueDict[node.value] & valueDict[readyStateNode.value]
                else:
                    result=valueDict[node.value] | valueDict[readyStateNode.value]
                newNode=Node()
                newNode.value=result
                newNode.leaf=True
                operationStack.append(newNode)
                readyStateNode=None
            elif (node.leaf and readyStateNode == None):
                readyStateNode=node
            elif (not node.leaf and readyStateNode != None):
                operationStack.append(readyStateNode)
                readyStateNode=None
                operationStack.append(node)
                operationStack.append(node.rightChildNode)
                operationStack.append(node.leftChildNode)
            elif (not node.leaf and  readyStateNode == None):
                operationStack.append(node)
                operationStack.append(node.rightChildNode)
                operationStack.append(node.leftChildNode)
        if (result==finallResult):
            chromosome.fitness=chromosome.fitness+1

def InitilizePool(sizeOfPool):
    tempPool=[]
    totatFitness=0
    for choromosoe in pool:
        totatFitness=totatFitness+choromosoe.fitness
    pool.sort(key=lambda x: x.fitness,reverse=True)
    index=0
    while(len(tempPool)!=sizeOfPool):
        choromosoe=pool[index]
        index = index +1
        if (index>=sizeOfPool):
            index=0
        countOfChromosoe= int((choromosoe.fitness*sizeOfPool)/totatFitness)
        for j in range(0,countOfChromosoe):
            tempPool.append(choromosoe)
    return tempPool


def CrossOver(sizeOfPool):
    endOfSelection=sizeOfPool
    for i in range(0,int(sizeOfPool/2)):

        firstIndex=randint(0,endOfSelection-1)
        firstChromosoeTree=pool[firstIndex].tree

        pool[firstIndex] , pool[endOfSelection-1] = pool[endOfSelection-1],pool[firstIndex]

        endOfSelection=endOfSelection-1

        secondIndex=randint(0,endOfSelection-1)
        secondChromosoeTree=pool[secondIndex].tree

        pool[secondIndex] , pool[endOfSelection-1] = pool[endOfSelection-1],pool[secondIndex]

        endOfSelection=endOfSelection-1

        firstNodeMaxLevel=0
        secondNodeMaxLevel=0
        for node in firstChromosoeTree.nodes:
            if(node.level>firstNodeMaxLevel):
                firstNodeMaxLevel=node.level
        for node in secondChromosoeTree.nodes:
            if(node.level>secondNodeMaxLevel):
                secondNodeMaxLevel=node.level

        maxLevelOfSelection=0
        if (firstNodeMaxLevel<secondNodeMaxLevel):
            maxLevelOfSelection=firstNodeMaxLevel
        else:
            maxLevelOfSelection=secondNodeMaxLevel

        selectedLevel=randint(1,maxLevelOfSelection)

        firstChromosoeSelectedLevelNodes=[x for x in firstChromosoeTree.nodes if x.level==selectedLevel]
        secondChromosoeSelectedLevelNodes=[x for x in secondChromosoeTree.nodes if x.level==selectedLevel]

        selectionNodeIndex=randint(0,len(firstChromosoeSelectedLevelNodes)-1)
        firstNode=firstChromosoeSelectedLevelNodes[selectionNodeIndex]

        selectionNodeIndex=randint(0,len(secondChromosoeSelectedLevelNodes)-1)
        secondNode=secondChromosoeSelectedLevelNodes[selectionNodeIndex]



        firstNodeParent=firstNode.parent
        secondNodeParent=secondNode.parent

        if (firstNodeParent.rightChildNode==firstNode):
            firstNodeParent.rightChildNode=secondNode
            secondNode.parent=firstNodeParent
        elif (firstNodeParent.leftChildNode==firstNode):
            firstNodeParent.leftChildNode=secondNode
            secondNode.parent=firstNodeParent

        if (secondNodeParent.rightChildNode==secondNode):
            secondNodeParent.rightChildNode=firstNode
            firstNode.parent=secondNodeParent
        elif (secondNodeParent.leftChildNode==secondNode):
            secondNodeParent.leftChildNode=firstNode
            firstNode.parent=secondNodeParent

        ReParseNodesOfAChromosome(firstChromosoeTree)
        ReParseNodesOfAChromosome(secondChromosoeTree)




def ReParseNodesOfAChromosome(tree):
    tree.nodes=[]
    node=tree.mainNode

    stackOfParse=[]
    stackOfParse.append(node)

    while(len(stackOfParse)!=0):
        node=stackOfParse.pop()
        tree.nodes.append(node)
        if (not node.leaf):
            stackOfParse.append(node.rightChildNode)
            stackOfParse.append(node.leftChildNode)


def Generations(generationCount,pool):
    for i in range(0,generationCount):
        for row in parsedArray:
            dictValue=dict()
            dictValue[1]=1
            dictValue[0]=0
            for t in range(0,5):
                dictValue['x'+str((5-t))]=int(row[t])
            CalculateFittnessOFthePool(dictValue,int(row[5]))


        pool=InitilizePool(60)

        if (i==0):
            for k in range(0,60):
                print(pool[k],pool[k].fitness)
            print('after 1000 generation')

        for chromosoe in pool:
            chromosoe.fitness=0

        CrossOver(60)
    return pool





operators=['&','|']
operatorsAndOperands=['&','|','x1','x2','x3','x4','x5']
operands=['x1','x2','x3','x4','x5']
pool=[]

parsedArray=ParseData('test')
CreateRandomPool(60)
pool=Generations(100,pool)
for row in parsedArray:
    dictValue=dict()
    dictValue[1]=1
    dictValue[0]=0
    for t in range(0,5):
        dictValue['x'+str((5-t))]=int(row[t])
    CalculateFittnessOFthePool(dictValue,int(row[5]))

for i in range(0,60):
    print(pool[i],pool[i].fitness)


__author__ = 'Nazemi'