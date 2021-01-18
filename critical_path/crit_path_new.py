import math
from collections import deque

maxid = 0   

class Task:
    def __init__(self, id, name, time, nextTasksIds=list()):
        self.id = id
        self.name = name
        self.time = time
        self.nextTasksIds = nextTasksIds
        
        self.prevTasksIds = list()
        self.nextTasks = list()
        self.prevTasks = list()
        self.S_direct = 0
        self.F_direct = 0
        self.S_reverse = math.inf
        self.F_reverse = math.inf
        self.isPrinted = False
        
    def to_string(self):
        return str('Task {} --  Name: {};  Duration: {};  NextTasks: {};  PrevTasks: {}\n'
                   .format(self.id, self.name, self.time, self.nextTasksIds, self.prevTasksIds))
    
    def clearSandF(self):
        self.S_direct = 0
        self.F_direct = 0
        self.S_reverse = math.inf
        self.F_reverse = math.inf
        
    def isCPM(self):
        return ((self.S_direct == self.S_reverse) and (self.F_direct == self.F_reverse))
    
    def timeReserve(self):
        return (self.S_reverse - self.S_direct);
        
    def resultString(self):
        if (self.isCPM()):
            additional_str = str('Cricical') 
        else:
            additional_str = str('TimeReserve = {}'.format(self.timeReserve()))
        
        if (self.prevTasksIds == [0]):
            self.prevTasksIds = list()
            
        if (self.nextTasksIds == [maxid + 1]):
            self.nextTasksIds = list()
            
        result_str = str('Task< id={}; name={}; time={}; StartTime_early={}; FinishTime_early={}; '
                         'StartTime_late={}; FinishTime_late={}; previousTasks={}; nextTasks={}> {}'
                         .format(self.id, self.name, self.time, self.S_direct - 1, self.F_direct - 1,
                                 self.S_reverse - 1, self.F_reverse - 1, self.prevTasksIds, self.nextTasksIds, additional_str))
            
        return result_str
      
        
           
        
      
def readFileStrings (filename):
    with open(filename) as data:
        strings = [row.strip() for row in data]
        tasks = list(row.split(';') for row in strings)
    return tasks



def writeFileStrings (filename, result_data):
    with open(filename, "w") as file:
        file.write(result_data)
    


def updateDirect(task):
    newEndTime = task.S_direct + task.time
    task.F_direct = newEndTime
    
    tasks = task.nextTasks
    if (len(tasks) > 0):
        for value in tasks:
            if (newEndTime > value.S_direct):
                value.S_direct = newEndTime
                updateDirect(value)



def findLastTask(task):
    lastTask = task
    tasks = task.nextTasks
    
    #print(task.to_string())
    
    if (len(tasks) > 0):
        for value in tasks:
            #print(value.to_string())
            lastTask = findLastTask(value)
    return lastTask



def updateReverse(task):
    newStartTime = task.F_reverse - task.time
    task.S_reverse = newStartTime
    tasks = task.prevTasks
    if (len(tasks) > 0):
        for value in tasks:
            if (newStartTime < value.F_reverse):
                value.F_reverse = newStartTime
                updateReverse(value)
                
                

def printGroup(task):
    queue = deque()
    queue.append(task)
    result_str = str()
    
    while (len(queue) > 0):
        processedTask = queue.popleft()
        tasks = processedTask.nextTasks
        if (len(tasks) > 0):
            queue.extend(tasks);
        if (processedTask.isPrinted == False and 
            len(processedTask.nextTasksIds) > 0 and len(processedTask.prevTasksIds) > 0):
            result_str += processedTask.resultString() + '\n'

        processedTask.isPrinted = True;
    return result_str
    
    





if __name__ == '__main__':
    
    task_strings = readFileStrings('input_new.txt')
    
    tasks=list()
    for string in task_strings:
        id = int(string[0])
        name = string[1]
        time = int(string[2])
        
        if id > maxid:
            maxid = id
        
        next_task_list = list()
        if (len(string[3]) != 2):
            next_task_list = list(map(int, string[3].strip('][').split(',')))
        
        tasks.append(Task(id, name, time, next_task_list))
        
        
    #добавление фиктивного конца
    for task in tasks:
        if len(task.nextTasksIds) == 0:
            task.nextTasksIds.append(maxid + 1)
    
    fict_end_task = Task(maxid + 1, 'FictEnd', 0)
    tasks.append(fict_end_task)
        
        
    for task in tasks:
        next_tasks = list()
        for task_id in task.nextTasksIds:
            next_task = next((x for x in tasks if x.id == int(task_id)), None)
            if next_task != None:
                next_tasks.append(next_task)
                next_task.prevTasks.append(task)
                next_task.prevTasksIds.append(task.id)
                
        task.nextTasks = next_tasks
    
    
    #добавление фиктивного начала
    begin_list = list()
    begin_ids_list = list()
    for task in tasks:
        if len(task.prevTasksIds) == 0:
            begin_list.append(task)
            begin_ids_list.append(task.id)
            task.prevTasksIds.append(0)
                  
    fict_begin_task = Task(0, 'FictBegin', 1, begin_ids_list)
    fict_begin_task.nextTasks = begin_list
    tasks.insert(0, fict_begin_task)
    
    
    for t in tasks:
        t.isPrinted = False
        t.clearSandF()
        
        
    #direct task
    updateDirect(tasks[0])
        
    #reverse task
    last_task = findLastTask(tasks[0])
    last_task.F_reverse = last_task.F_direct
    updateReverse(last_task)
        
    
    printed_str = str()    
    last_task = findLastTask(tasks[0])
    process_time_str = str('Total time: {}\n'.format(last_task.F_direct - 1))
    printed_str += process_time_str
    
    printed_str += printGroup(tasks[0])
    for t in tasks:
        t.isPrinted = False
    printed_str += '\n'
        
    print(printed_str)
    
    writeFileStrings("result.txt", printed_str)