
'''
External Help: I used AI for help with debugging a few parts 
(logic for checking color limits, display conditionals) and for brainstorming
ideas for the completion animation.

Key Features:
1. The user can add tasks based on text that they input. They can indicate the 
urgency level and type of task (Academic, Personal, Chores, Miscellaneous), 
which correspond to the size and color of the corresponding flower, respectively.

2. Clicking icons allows the user to edit a task (task text, urgency level, and 
type of task) and the user can also delete their tasks. Both actions sync up 
appropriately with the garden.

3. Checking and unchecking tasks controls the animation of the sprouts into 
flowers and visual strikethrough of tasks.

4. Tasks are represented through a garden visualization where tasks correspond 
to sprouts that bloom into flowers upon completion. Sprouts are positioned in 
four color-coded rows representing task type and are sized based on their urgency
level. Hovering over the sprouts displays a text bubble displaying the corresponding
task, with text wraparound.

5. Limits enforced on max number of tasks (5 per color and 8 in total) with 
warning messages. I also set a limit for the length of the task text.

6. When all tasks are checked, there is a temporary confetti animation of flowers  
dropping from above, with flowers varying in random colors and scales.

7. OOP classes for both individual tasks paired with attributes for each task
as well as the overall task list that is updated accordingly with current tasks.

8. There's a cohesive color palette throughout app with custom digitally-drawn 
garden and flower elements. Buttons have rounded corners for visual appeal.

9. I incorporated text wraparound in three areas: the task text for the pop up, 
text in the to-do list, and the hover text bubbles in the garden.

'''


from cmu_graphics import *
import random, math

def onAppStart(app):
    app.width = 600
    app.height = 400
    app.popUp = False
    app.addTaskTop = 120
    app.currentTask = None
    app.types = ['Academic', 'Personal', 'Chores', 'Miscellaneous']
    app.typeColors = ['lightSkyBlue', 'plum', 'gold', 'pink']
    app.taskList = taskList()
    app.incomplete = False
    app.allFull = False
    app.complete = False
    app.dropConfetti = False
    app.editing = False
    
    app.sprout = 'cmu://1073416/43484261/IMG_1475+(1).png'
    app.blueFlower = 'cmu://1073416/43492445'
    app.purpleFlower = 'cmu://1073416/43492439'
    app.yellowFlower = 'cmu://1073416/43492444'
    app.pinkFlower = 'cmu://1073416/43492442'
    app.pencil = 'cmu://1073416/43655637/pencil'
    app.trash = 'cmu://1073416/43655621/trash'
    app.blue = app.purple = app.yellow = app.pink = ()
    app.blueFull = app.purpleFull = app.yellowFull = app.pinkFull = False
    
    app.stepsPerSecond = 10
    app.rows = 8
    app.cols = 16
    app.confettiLocations = []
    app.steps = 1
    
def distance(x0, y0, x1, y1):
    return ((y1-y0)**2 + (x1-x0)**2)**0.5
    
class taskList:
    def __init__(self):
        self.tasks = []
        
    def addTask(self, Task):
        self.tasks.append(Task)
        
    def __repr__(self):
        return f'{self.tasks}'
        
    def getTask(self, color, sproutIndex): # returns task given index of the sprout within a color
        count = 0
        for task in self.tasks:
            if task.taskColor == color:
                count += 1
                if count-1 == sproutIndex:
                    return task
    
class Task:
    def __init__(self, task, urgency, taskType, color, checked, hover):
        self.task = task
        self.urgency = urgency
        self.taskType = taskType
        self.taskColor = color
        self.checked = checked
        self.hover = hover

    def __repr__(self):
        return f'Task: {self.task}, Urgency: {self.urgency}, Type: {self.taskType}, Color: {self.taskColor}'
    
def onStep(app):
    dropConfetti(app)
    if app.steps <= 30 and app.dropConfetti == True:
        app.steps += 1
        spawnConfetti(app)
    else:
        app.steps = 0
        app.dropConfetti = False
        
def dropConfetti(app):
    remaining = []
    for row, col in app.confettiLocations:
        newRow, newCol = row+1, col
        if newRow < app.rows:
            remaining.append((newRow, newCol))
    app.confettiLocations = remaining
    
def spawnConfetti(app):
    row, col = 0, random.randint(0, app.cols-1)
    app.confettiLocations.append((row, col))
    
    
def redrawAll(app):
    # background UI
    drawRect(0, 70, app.width/2, app.height-70, fill='aliceBlue')
    for i in range(12):
        if i%4 == 0:
            color = 'plum'
        elif i%4 == 1:
            color = 'lightSkyBlue'
        elif i%4 == 2:
            color = 'gold'
        elif i%4 == 3:
            color = 'pink'
        drawCircle(10+25*i, 70, 13, fill=color, opacity=60)
        drawCircle(10+25*i, 400, 13, fill=color, opacity=60)
    for i in range(14):
        if i%4 == 0:
            color = 'plum'
        elif i%4 == 1:
            color = 'lightSkyBlue'
        elif i%4 == 2:
            color = 'gold'
        elif i%4 == 3:
            color = 'pink'
        drawCircle(0, 70+25*i, 13, fill=color, opacity=60)
        drawCircle(300, 70+25*i, 13, fill=color, opacity=60)
    drawImage('cmu://1073416/43492583/Untitled_Artwork+14+(1).png', app.width/2, 70, width=app.width/2, height=app.height-70)
    drawRect(0, 0, app.width, 70, fill='skyBlue')
    drawLabel('Task Garden', 24, 27, size=30, align='left', font='monospace', bold=True)
    drawLabel('Check off tasks to grow your garden!', 24, 44, size=15, bold=True, align='left-top', font='monospace')
    
    # Add Task button
    drawRect(36, app.addTaskTop, 121, 40, fill='mediumPurple', align='left')
    drawCircle(40, app.addTaskTop, 20, fill='mediumPurple')
    drawCircle(153, app.addTaskTop, 20, fill='mediumPurple')
    drawRect(37, app.addTaskTop, 120, 36, fill='lavender', align='left')
    drawCircle(40, app.addTaskTop, 18, fill='lavender')
    drawCircle(153, app.addTaskTop, 18, fill='lavender')
    drawCircle(45, app.addTaskTop, 10, fill=None, border='mediumPurple', borderWidth=2)
    drawLabel('+    Add Task', 40, app.addTaskTop, fill='mediumPurple', size=20, align='left')
    

    drawTasks(app)
    drawFlower(app)
    drawSprouts(app, 'lightSkyBlue', app.blue)
    drawSprouts(app, 'plum', app.purple)
    drawSprouts(app, 'gold', app.yellow)
    drawSprouts(app, 'pink', app.pink)
    if app.complete:
        drawLabel('Congrats, your garden', 580, 20, fill='mediumPurple', size=18, bold=True, align='right-top', font='monospace')
        drawLabel('is in full bloom!', 580, 39, fill='mediumPurple', size=18, bold=True, align='right-top', font='monospace')
        drawConfetti(app)
    if app.popUp:
        drawPopUp(app)

def getBreakOff(string, breakOff): 
    breakOff = breakOff
    while string[breakOff].isalpha() and breakOff >= 0:
        breakOff -= 1
    return breakOff+1     
    

def drawPopUp(app):
    # pop up background
    drawRect(0, 0, app.width, app.height, fill='gray', opacity=20)
    drawRect(50, 50, app.width-100, app.height-100, fill='honeydew')
    drawCircle(55, 55, 20, fill='honeydew')
    drawRect(35, 60, 20, 290, fill='honeydew')
    drawCircle(545, 55, 20, fill='honeydew')
    drawRect(545, 60, 20, 290, fill='honeydew')
    drawCircle(55, 345, 20, fill='honeydew')
    drawCircle(545, 345, 20, fill='honeydew')
    drawRect(55, 35, 490, 20, fill='honeydew')
    drawRect(55, 345, 490, 20, fill='honeydew')
    
    # task text
    if len(app.currentTask.task) >= 20:
        breakOff = getBreakOff(app.currentTask.task, 19)
        drawLabel(f'Task: {app.currentTask.task[:breakOff]}', 70, 80, size=30, font='monospace', align='left', bold=True)
        if len(app.currentTask.task[breakOff:]) >= 25:
            breakOff2 = getBreakOff(app.currentTask.task[breakOff:], 24)
            drawLabel(f'{app.currentTask.task[breakOff:breakOff+breakOff2]}', 70, 120, size=30, font='monospace', align='left', bold=True)
            drawLabel(f'{app.currentTask.task[breakOff+breakOff2:]}', 70, 160, size=30, font='monospace', align='left', bold=True)
        else:
            drawLabel(f'{app.currentTask.task[breakOff:]}', 70, 120, size=30, font='monospace', align='left', bold=True)
    else:
        drawLabel(f'Task: {app.currentTask.task}', 70, 80, size=30, font='monospace', align='left', bold=True)

    # urgency level
    drawLabel('Urgency', 130, 220, size=20, font='monospace', align='left', bold=True)
    for i in range(3):
        if app.currentTask.urgency != None:
            coloredCircle = app.currentTask.urgency-1
            if i == coloredCircle:
                if app.currentTask.taskType == None:
                    color = 'gray'
                else:
                    color = app.currentTask.taskColor
            else:
                color = 'gainsboro'
        else:
            color = 'gainsboro'
        for petal in range(3):
            scale = 3-i
            drawOval(110+60*i, 270, 30+10*scale, 25+scale, rotateAngle=60*petal, fill=color, align='center')
            drawCircle(110+60*i, 270, 10+2*scale, fill='navajoWhite')
        drawLabel(f'{i+1}', 110+60*i, 270, size=14)
        
    # type of task  
    drawLabel('Type of Task', 400, 220, size=20, font='monospace', bold=True)
    for i in range(len(app.types)):
        currType = app.types[i]
        color = app.currentTask.taskColor if app.typeColors[i] == app.currentTask.taskColor else None
        if i <= 1:
            drawLabel(f'{currType}', 330+100*i, 255, size=14, fill='gray', align='left', font='monospace', bold=True)
            drawCircle(315+100*i, 255, 8, fill=color, border=app.typeColors[i])
        else:
            drawLabel(f'{currType}', 330+100*(i-2), 285, size=14, fill='gray', align='left', font='monospace', bold=True)
            drawCircle(315+100*(i-2), 285, 8, fill=color, border=app.typeColors[i])
        drawRect(485, 319, 60, 28, fill='mediumPurple')
        drawCircle(490, 333, 14, fill='mediumPurple')
        drawCircle(540, 333, 14, fill='mediumPurple')
        drawRect(486, 321, 59, 24, fill='lavender')
        drawCircle(490, 333, 12, fill='lavender')
        drawCircle(540, 333, 12, fill='lavender')
        drawLabel('Add Task', 515, 333, fill='mediumPurple', size=15)
    
    # if either type or urgency not selected
    if app.incomplete:
        missing = []
        if app.currentTask.urgency == None:
            missing.append('an Urgency Level')
        if app.currentTask.taskType == None:
            missing.append('a Task Type')
        if len(missing) == 1:
            drawLabel(f'Please select {missing[0]}.', 300, 340, fill='red', size=15)
        elif len(missing) == 2:
            drawLabel(f'Please select {missing[0]} and {missing[1]}.', 300, 340, fill='red', size=15)
            
    if app.allFull:
        drawLabel('Max amount of tasks added!', 300, 340, fill='red', size=15)
        
    if app.blueFull and app.currentTask.taskColor == 'lightSkyBlue':
        drawLabel(f'Max amount of Academic tasks added!', 300, 340, fill='red', size=15)
    elif app.purpleFull:
        drawLabel(f'Max amount of Personal tasks added!', 300, 340, fill='red', size=15)
    elif app.yellowFull:
        drawLabel(f'Max amount of Chores tasks added!', 300, 340, fill='red', size=15)
    elif app.pinkFull:
        drawLabel(f'Max amount of Miscellaneous tasks added!', 300, 340, fill='red', size=15)
        
    drawLine(525, 55, 545, 75, fill='gray', lineWidth=3)
    drawLine(545, 55, 525, 75, fill='gray', lineWidth=3)
        
        
def drawSprouts(app, color, colorBoard):
        for sproutIndex in range(len(colorBoard)):
            task = app.taskList.getTask(color, sproutIndex)
            if colorBoard[sproutIndex] != None and app.currentTask != None:
                urgency = colorBoard[sproutIndex]
                scale = 3-(urgency)
                colorIndex = app.typeColors.index(color)
                if task.checked == False:
                    drawImage(app.sprout, 425+30*sproutIndex, 160+66*colorIndex, width=18+5*scale, height=22+5*scale, align='bottom')
                else:
                    if task.taskColor == 'lightSkyBlue':
                        drawImage(app.blueFlower, 425+30*sproutIndex, 160+66*colorIndex, width=18+5*scale, height=40+5*scale, align='bottom')
                    elif task.taskColor == 'plum':
                        drawImage(app.purpleFlower, 425+30*sproutIndex, 160+66*colorIndex, width=18+5*scale, height=40+5*scale, align='bottom')
                    elif task.taskColor == 'gold':
                        drawImage(app.yellowFlower, 425+30*sproutIndex, 160+66*colorIndex, width=18+5*scale, height=40+5*scale, align='bottom')
                    elif task.taskColor == 'pink':
                        drawImage(app.pinkFlower, 425+30*sproutIndex, 160+66*colorIndex, width=18+5*scale, height=40+5*scale, align='bottom')
                
                if task.hover == True:
                    cx = 425+30*sproutIndex
                    cy = 125+66*colorIndex 
                    if len(task.task) <= 6:
                        drawRect(cx, cy-27, 35, 25, fill='white', align='center') 
                        drawRect(cx, cy-40, 32, 4, align='center', fill='white') 
                        drawRect(cx, cy-14, 32, 4, align='center', fill='white')
                        drawRect(cx-18, cy-27, 4, 23, align='center', fill='white') 
                        drawRect(cx+18, cy-27, 4, 23, align='center', fill='white')
                        drawCircle(cx-17, cy-39, 3, fill='white')
                        drawCircle(cx+17, cy-39, 3, fill='white')
                        drawCircle(cx-17, cy-15, 3, fill='white')
                        drawCircle(cx+17, cy-15, 3, fill='white')
                        drawPolygon(cx-7, cy-15, cx, cy+5, cx+7, cy-15, fill='white')
                        drawLabel(task.task, cx, cy-28, size=10)
                    elif len(task.task) <= 12: 
                        breakOff = getBreakOff(task.task, int(len(task.task) / 2))
                        drawRect(cx, cy-25, 45, 35, fill='white', align='center')
                        drawRect(cx, cy-44, 41, 4, align='center', fill='white') 
                        drawRect(cx, cy-6, 41, 4, align='center', fill='white') 
                        drawRect(cx-24, cy-26, 4, 31, align='center', fill='white') 
                        drawRect(cx+24, cy-26, 4, 31, align='center', fill='white')
                        drawCircle(cx-22, cy-42, 4, fill='white')
                        drawCircle(cx+22, cy-42, 4, fill='white')
                        drawCircle(cx-22, cy-8, 4, fill='white')
                        drawCircle(cx+22, cy-8, 4, fill='white')
                        
                        drawPolygon(cx-7, cy-15, cx, cy+5, cx+7, cy-15, fill='white')
                        drawLabel(task.task[:breakOff], cx, cy-30, size=10)
                        drawLabel(task.task[breakOff:], cx, cy-20, size=10)
                    else:
                        breakOff1 = getBreakOff(task.task, math.floor(len(task.task) / 3)-1)
                        breakOff2 = getBreakOff(task.task[breakOff1:], math.floor(len(task.task) / 3)-1)
                        drawRect(cx, cy-25, 69, 37, fill='white', align='center')
                        drawRect(cx, cy-45, 58, 4, align='center', fill='white') 
                        drawRect(cx, cy-5, 58, 4, align='center', fill='white') 
                        drawCircle(cx-31, cy-43, 4, fill='white')
                        drawCircle(cx+31, cy-43, 4, fill='white')
                        drawCircle(cx-31, cy-7, 4, fill='white')
                        drawCircle(cx+31, cy-7, 4, fill='white')
                        
                        
                        drawPolygon(cx-7, cy-15, cx, cy+5, cx+7, cy-15, fill='white')
                        drawLabel(task.task[:breakOff1], cx, cy-35, size=10)
                        drawLabel(task.task[breakOff1:breakOff1+breakOff2], cx, cy-25, size=10)
                        if len(task.task[breakOff1+breakOff2:]) <= 14:
                            ending = task.task[breakOff1+breakOff2:]
                        else:
                            ending = task.task[breakOff1+breakOff2:breakOff1+breakOff2+11] + '...'
                        drawLabel(ending, cx, cy-15, size=10)
def drawTasks(app):
    if app.taskList != None:
        for i in range(len(app.taskList.tasks)):
            task = app.taskList.tasks[i]
            if len(task.task) < 21:
                drawLabel(f'{task.task}', 83, 107+30*i, size=13, align='left')
            else:
                breakOff = getBreakOff(task.task, 20)
                drawLabel(f'{task.task[:breakOff]}', 83, 99+30*i, size=13, align='left')
                drawLabel(f'{task.task[breakOff:]}', 83, 115+30*i, size=13, align='left')
            drawRect(28, 100+30*i, 15, 15, fill=None, border='black', borderWidth=2)
            drawImage(app.pencil, 213, 93+30*i, width=30, height=30, align='left-top')
            drawImage(app.trash, 246, 93+30*i, width=30, height=30, align='left-top')
            if task.checked == True:
                drawLine(30, 105+30*i, 35, 112+30*i, lineWidth=2)
                drawLine(35, 112+30*i, 42, 95+30*i, lineWidth=2)
                taskLength = len(task.task) * 6
                if len(task.task) < 21:
                    drawLine(82, 108+30*i, 87+taskLength, 108+30*i, lineWidth=2)
                else:
                    breakOff = getBreakOff(task.task, 20)
                    firstLine = len(task.task[:breakOff])
                    secondLine = len(task.task[breakOff:])
                    drawLine(82, 100+30*i, 79+firstLine*6, 100+30*i, lineWidth=2)
                    drawLine(82, 116+30*i, 93+secondLine*6, 116+30*i, lineWidth=2)
            
            
def drawFlower(app):
    for i in range(len(app.taskList.tasks)):
        task = app.taskList.tasks[i]
        urgency = 4-task.urgency 
        for petal in range(3):
            drawOval(63, 107+30*i, 20+3*urgency, 6+3*urgency, rotateAngle=60*petal, fill=task.taskColor, align='center')
            drawCircle(63, 107+30*i, 3+urgency, fill='navajoWhite')

def drawConfetti(app):
    for confetti in app.confettiLocations:
        row, col = confetti
        cellLeft, cellTop = getCellLeftTop(app, row, col)
        cellWidth, cellHeight = getCellSize(app)
        color = app.typeColors[random.randrange(4)]
        scale = random.randrange(4)
        for petal in range(3):
            drawOval(cellLeft, cellTop, 30+5*scale, 15+2*scale, rotateAngle=60*petal, fill=color, align='center')
            drawCircle(cellLeft, cellTop, 5+2*scale, fill='navajoWhite')

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = col * cellWidth
    cellTop = row * cellHeight
    return (cellLeft, cellTop)
    
def getCellSize(app):
    cellWidth = app.width/app.cols
    cellHeight = app.height/app.rows
    return (cellWidth, cellHeight)

def onMousePress(app, mouseX, mouseY):
    if (app.popUp == False and 20 <= mouseX <= 170 and 
        app.addTaskTop-18 <= mouseY <= app.addTaskTop+18):
        app.popUp = True
        textInput = app.getTextInput('Enter Task:')
        while textInput == '':
            textInput = app.getTextInput('Enter Task:')
        while len(textInput) >= 42:
            textInput = app.getTextInput('Please input a shorter task:')
        app.currentTask = Task(textInput, None, None, None, False, None)
    
    if app.popUp:
        for i in range(3):
            cx = 110+60*i
            cy = 270
            r = 15+2*(3-i)
            if distance(mouseX, mouseY, cx, cy) <= r: # task urgency
                app.currentTask.urgency = i+1
        for i in range(4):
            cx = 315 if i%2 == 0 else 415
            cy = 255 if i <= 1 else 285
            if distance(mouseX, mouseY, cx, cy) <= 8: # task type
                app.currentTask.taskType = app.types[i]
                app.currentTask.taskColor = app.typeColors[i]
                app.blueFull = app.purpleFull = app.yellowFull = app.pinkFull = app.allFull = False
                
        if 480.5 <= mouseX <= 539.5 and 321 <= mouseY <= 345: # add task button
            if app.currentTask.urgency != None and app.currentTask.taskType != None:
                color = app.currentTask.taskColor
                colorLimitReached = (
                    (color == 'lightSkyBlue' and len(app.blue) >= 5) or
                    (color == 'plum' and len(app.purple) >= 5) or
                    (color == 'gold' and len(app.yellow) >= 5) or
                    (color == 'pink' and len(app.pink) >= 5)
                    )
                if len(app.taskList.tasks) >= 8:
                    app.allFull = True
                elif colorLimitReached:
                    if color == 'lightSkyBlue':
                        app.blueFull = True
                    elif color == 'plum':
                        app.purpleFull = True
                    elif color == 'gold':
                        app.yellowFull = True
                    elif color == 'pink':
                        app.pinkFull = True
                else:
                    app.incomplete = False
                    app.popUp = False
                    updateGarden(app)
                    if not app.editing:
                        app.taskList.addTask(app.currentTask)
                        app.addTaskTop += 30
                        app.editing = False
                    app.editing = False
                    if checkIfComplete(app):
                        app.complete = True
                        app.dropConfetti = True
                    else:
                        app.complete = False
                        app.dropConfetti = False
            else:
                app.incomplete = True
        if 525 <= mouseX <= 545 and 55 <= mouseY <= 75: # x button
            app.popUp = False
        
    else: # if there's no pop up
        for task in app.taskList.tasks:
            index = app.taskList.tasks.index(task)
            if 27 <= mouseX <= 42 and 100+30*index <= mouseY <= 115+30*index: # check box
                task.checked = not task.checked
                if checkIfComplete(app):
                    app.complete = True
                    app.dropConfetti = True
                else:
                    app.complete = False
                    app.dropConfetti = False
            pencilCx, pencilCy = 228, 107+30*index
            trashCx, trashCy = 259, 107+30*index
            if distance(mouseX, mouseY, pencilCx, pencilCy) <= 14:
                newTask = app.getTextInput('Editing Task...')
                app.popUp = True
                app.editing = True
                app.currentTask = app.taskList.tasks[index]
                app.currentTask.task = newTask
                colorIndex = app.typeColors.index(task.taskColor)
                if colorIndex == 0:
                    app.blue = app.blue[:-1]
                if colorIndex == 1:
                    app.purple = app.purple[:-1]
                if colorIndex == 2:
                    app.yellow = app.yellow[:-1]
                if colorIndex == 3:
                    app.pink = app.pink[:-1]
            if distance(mouseX, mouseY, trashCx, trashCy) <= 14:
                app.taskList.tasks.pop(index)
                colorIndex = app.typeColors.index(task.taskColor) # 0, 1, 2, 3
                allColors = [app.blue, app.purple, app.yellow, app.pink]
                if colorIndex == 0:
                    app.blue = app.blue[:-1]
                if colorIndex == 1:
                    app.purple = app.purple[:-1]
                if colorIndex == 2:
                    app.yellow = app.yellow[:-1]
                if colorIndex == 3:
                    app.pink = app.pink[:-1]
                app.addTaskTop -= 30
    
def checkIfComplete(app):
    for task in app.taskList.tasks:
        if task.checked == False:
            return False
    return True
            
def updateGarden(app):
    color = app.currentTask.taskColor
    urgency = app.currentTask.urgency
    if color == 'lightSkyBlue':
        app.blue = app.blue + (urgency,)
    elif color == 'plum':
        app.purple = app.purple + (urgency,)
    elif color == 'pink':
        app.pink = app.pink + (urgency,)
    elif color == 'gold':
        app.yellow = app.yellow + (urgency,)

def onMouseMove(app, mouseX, mouseY):
    if not app.popUp:
        colorBoards = [app.blue, app.purple, app.yellow, app.pink]
        for colorIndex in range(len(colorBoards)):
            color = app.typeColors[colorIndex]
            for sproutIndex in range(len(colorBoards[colorIndex])):
                currTask = app.taskList.getTask(color, sproutIndex)
                left = 413+30*sproutIndex
                right = left+25
                top = 125+66*colorIndex
                bottom = top+30
                if left <= mouseX <= right and top <= mouseY <= bottom:
                    currTask.hover = True
                else:
                    currTask.hover = False

def main():
    runApp()

main()