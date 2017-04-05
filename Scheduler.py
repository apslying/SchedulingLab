#to do- format decimals, print statment in two lines, fix printing after one process terminates
#important input-3 has more spaces in input file, tie break rule
import random
from Process import Process
textArray=[]

randomArray=[]
preReadyArray=[]
readyArray=[]
runningArray=[]
blockedArray=[]
globalTime=0
numOfTerminatedProcesses=0
finalFinishingTime=0
cpuUnused=0
ioUnused=0

def debug():
    file = open('fcfs-output-4-detailed.txt', mode='r')
    text = file.read()
    global textArray
    textArray = text.split(sep='\n')
    #print(textArray[0].replace(' ',''))


def createProcesses():
    file=open('input-7.txt', mode='r')
    a=file.read()
    arr=a.split(sep='  ')
    processArr=[]
    for i in range(1,int(arr[0])+1):
        arr[i]=arr[i].lstrip()
        tempArr=arr[i].split(sep=' ')
        #print(tempArr)
        obj=Process(int(tempArr[0]),int(tempArr[1]),int(tempArr[2]),int(tempArr[3]))
        processArr.append(obj)
    # processArr=sorted(processArr, key=lambda process: process.maxCpuBurst)
    # for p in processArr:
    #     print(p.arrivalTime, p.maxCpuBurst, p.totalCpuTimeNeeded, p.maxIoBurst)
    return processArr

def readRandom():
    global randomArray
    file = open('random-numbers.txt', mode='r')
    text=file.read()
    randomArray=text.split(sep='\n')
    randomArray.pop(-1) #removes the \n char at end of array


def randomOS(u):
    #print('random:', 1+(int(randomArray[0])%u), randomArray[0])
    num=randomArray[0]
    randomArray.pop(0)
    return 1+(int(num)%u)

def runProcesses():
    global globalTime

    while not_all_processes_terminated():
        verbose_output()
        #print('')
        #decrement running/blocked times
        # increment waiting time
        if readyArray:
            increment_all_process_waiting_time()

        if runningArray:
            decrement_process_cpu_and_total_time()

        if blockedArray:
            for process in blockedArray:
                update_process_io_time(process)

        if runningArray and runningArray[0].totalTimeLeft == 0:
            terminate_process()

        if runningArray and runningArray[0].cpuTimeLeft==0:
            move_process_from_running_to_blocked()

        #create and terminate processes
        create_processes_by_globalTime()

        #move processes

        if blockedArray:
            for process in reversed(blockedArray):
                if process.ioTimeLeft==0:
                    move_process_from_blocked_to_preready(process)

        if preReadyArray:
            move_process_from_preready_to_ready()

        if not runningArray and readyArray:
            move_process_from_ready_to_running()


        if not runningArray and not_all_processes_terminated():
            global cpuUnused
            cpuUnused+=1

        if not blockedArray and not_all_processes_terminated():
            global ioUnused
            ioUnused+=1

        #increment time
        globalTime+=1


def increment_all_process_waiting_time():
    for process in readyArray:
        process.waitingTime+=1

def decrement_process_cpu_and_total_time():
    runningArray[0].cpuTimeLeft-=1
    runningArray[0].totalTimeLeft-=1

def update_process_io_time(process):
    process.ioTimeLeft-=1
    process.ioTimeTotal+=1

def move_process_from_ready_to_running():
    readyArray[0].cpuTimeLeft=min(randomOS(readyArray[0].maxCpuBurst),readyArray[0].totalCpuTimeNeeded)
    readyArray[0].state=2
    runningArray.append(readyArray[0])
    readyArray.pop(0)

def move_process_from_running_to_blocked():
    runningArray[0].ioTimeLeft=randomOS(runningArray[0].maxIoBurst)
    runningArray[0].state=3
    blockedArray.insert(0,runningArray[0])
    runningArray.pop(0)

def move_process_from_blocked_to_preready(process):
    process.state=-1
    preReadyArray.append(process)
    blockedArray.pop(blockedArray.index(process))

def move_process_from_preready_to_ready():
    global preReadyArray
    tempPreReady=[]
    while preReadyArray:
        print(preReadyArray)
        chosenProcess=preReadyArray[0]
        for i in range(1,len(preReadyArray)):
            print('here')
            if preReadyArray[i].arrivalTime<chosenProcess.arrivalTime or preReadyArray[i].arrivalTime==chosenProcess.arrivalTime and processArray.index(preReadyArray[i])<processArray.index(chosenProcess):
                chosenProcess=preReadyArray[i]
        tempPreReady.append(chosenProcess)
        preReadyArray.remove(chosenProcess)

    preReadyArray=tempPreReady
    for process in preReadyArray:
        process.state = 1
    readyArray.extend(preReadyArray)
    preReadyArray=[]

def create_processes_by_globalTime():
    for process in processArray:
        if process.arrivalTime==globalTime:
            preReadyArray.append(process)
            process.state=-1

def terminate_process():
    runningArray[0].state=4
    runningArray[0].finishingTime=globalTime
    global finalFinishingTime
    finalFinishingTime = runningArray[0].finishingTime
    runningArray[0].turnaroundTime=runningArray[0].finishingTime-runningArray[0].arrivalTime
    process_output_summary()
    runningArray.pop(0)
    global numOfTerminatedProcesses
    numOfTerminatedProcesses+=1

def not_all_processes_terminated():
    if numOfTerminatedProcesses==len(processArray):
        #print('false')
        return False
    else:
        #print('true')
        return True

def process_output_summary():
    print('Process ', processArray.index(runningArray[0]) ,':', sep='')
    print('\t\t(A,B,C,IO) = (',runningArray[0].arrivalTime, ',' ,runningArray[0].maxCpuBurst,',' , runningArray[0].totalCpuTimeNeeded,',' , runningArray[0].maxIoBurst, ')', sep='')
    print('\t\tFinishing time:', runningArray[0].finishingTime)
    print('\t\tTurnaround time:', runningArray[0].turnaroundTime)
    print('\t\tI/O time:', runningArray[0].ioTimeTotal)
    print('\t\tWaiting time:', runningArray[0].waitingTime)

def print_summary_data():
    print('Summary Data:')
    print('\t\tFinishing time:', finalFinishingTime)
    print('\t\tCPU Utilization:', (finalFinishingTime-cpuUnused)/finalFinishingTime)
    print('\t\tI/O Utilization:', (finalFinishingTime-ioUnused)/finalFinishingTime)
    print('\t\tThroughput:', (len(processArray)/finalFinishingTime) * 100 ,'processes per hundred cycles')
    print('\t\tAverage turnaround time:', average_turnaround())
    print('\t\tAverage waiting time:', average_waiting())

def average_turnaround():
    sum=0
    for process in processArray:
        sum+=process.turnaroundTime
    return sum/len(processArray)

def average_waiting():
    sum=0
    for process in processArray:
        sum+=process.waitingTime
    return sum/len(processArray)

def verbose_output():
    string = 'Beforecycle' + str(globalTime) + ':'
    for process in processArray:
        if process.state==0:
            string+='unstarted0'
        elif process.state==1:
            string+='ready0'
        elif process.state==2:
            string += 'running' + str(process.cpuTimeLeft)
        elif process.state==3:
            string += 'blocked' + str(process.ioTimeLeft)
        elif process.state==4:
            string += 'terminated0'
        elif process.state == -1:
            string += 'preready'
        else:
            string += 'error'

    string+='.'
    print(globalTime, string)
    if string!=textArray[globalTime].replace(' ',''):
        print(globalTime)



#running the code
debug()

readRandom()
processArray = createProcesses()

runProcesses()
print_summary_data()

