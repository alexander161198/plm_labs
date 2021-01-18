import math
from collections import deque


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
            
        result_str = str('Task< id={}; name={}; time={}; StartTime_early={}; FinishTime_early={}; '
                         'StartTime_late={}; FinishTime_late={}; previousTasks={}; nextTasks={}> {}'
                         .format(self.id, self.name, self.time, self.S_direct, self.F_direct,
                                 self.S_reverse, self.F_reverse, self.prevTasksIds, self.nextTasksIds, additional_str))
            
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
    print(task.to_string())
    
    if (len(tasks) > 0):
        for value in tasks:
            print(value.to_string())
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
    
    task_strings = readFileStrings('input.txt')
    
    maxid = 0
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
    
        
    first_tasks = list()
    for task in tasks:
        task_first = True
        for task_second in tasks:
            for next_task_id in task_second.nextTasksIds:
                if next_task_id == task.id:
                    task_first = False
                    break
            if task_first == False:
                break
        if task_first:
            first_tasks.append(task)
    
    #добавление фиктивного начала
    begin_list = list()
    for task in tasks:
        if len(task.prevTasksIds) == 0:
            begin_list.append(task.id)
            #task.prevTasksIds.append(0)
            
    fict_begin_task = Task(0, 'FictBegin', 1)
    fict_begin_task.nextTasksIds = begin_list
    #tasks.insert(0, fict_begin_task)
    
    #first_tasks.append(fict_begin_task)
    
    #print(tasks[0].to_string())
    #print(first_tasks[0].to_string())
    
    for t in tasks:
        t.isPrinted = False
        t.clearSandF()
        
        
    #direct task
    for i in range(len(first_tasks)):
        updateDirect(first_tasks[i])
        
    #reverse task
    for first_task in first_tasks:
        last_task = findLastTask(first_task)
        #print(last_task.to_string())
        last_task.F_reverse = last_task.F_direct
        updateReverse(last_task)
        
    
    printed_str = str()
    for i in range(len(first_tasks)):
        header = str('Option {}. Start from Task {} ({})\n'
                     .format(i+1, first_tasks[i].id, first_tasks[i].name))
        printed_str += header
        
        last_task = findLastTask(first_tasks[i])
        process_time_str = str('Total time: {}\n'.format(last_task.F_direct))
        printed_str += process_time_str
        
        printed_str += printGroup(first_tasks[i])
        for t in tasks:
            t.isPrinted = False
        printed_str += '\n'
        
   # print(printed_str)
    
    writeFileStrings("result.txt", printed_str)