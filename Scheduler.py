#to do- format decimals, print statment in two lines, fix printing after one process terminates
#to do- fix verbose output for rr
import random
import sys
import getopt
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
verbose=False

def globals_to_default_values():
    global preReadyArray
    global readyArray
    global runningArray
    global blockedArray
    global globalTime
    global numOfTerminatedProcesses
    global finalFinishingTime
    global cpuUnused
    global ioUnused
    global verbose

    preReadyArray = []
    readyArray = []
    runningArray = []
    blockedArray = []
    globalTime = 0
    numOfTerminatedProcesses = 0
    finalFinishingTime = 0
    cpuUnused = 0
    ioUnused = 0
    verbose = False

def debug():
    file = open('psjf-output-4-detailed.txt', mode='r')
    text = file.read()
    global textArray
    textArray = text.split('\n')
    #print(textArray[0].replace(' ',''))


def createProcesses():
    options, remainder=getopt.getopt(sys.argv[1:], '', 'verbose')
    if options!=[] and options[0][0]=='--verbose':
        global verbose
        verbose=True
    file=open(remainder[0], mode='r')
    a=file.read()
    a = a.replace('    ', '   ')
    arr=a.split('  ')
    processArr=[]
    for i in range(1,int(arr[0])+1):
        arr[i]=arr[i].lstrip()
        tempArr=arr[i].split(' ')
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
    randomArray=text.split('\n')
    randomArray.pop(-1) #removes the \n char at end of array


def randomOS(u):
    #print('random:', 1+(int(randomArray[0])%u), randomArray[0])
    num=randomArray[0]
    randomArray.pop(0)
    return 1+(int(num)%u)

def runFcfs():
    global globalTime
    global verbose

    print 'The scheduling algorithm used was First Come First Served'
    while not_all_processes_terminated():
        if verbose==True:
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
            fcfs_move_process_from_preready_to_ready()

        if not runningArray and readyArray:
            fcfs_move_process_from_ready_to_running()


        if not runningArray and not_all_processes_terminated():
            global cpuUnused
            cpuUnused+=1

        if not blockedArray and not_all_processes_terminated():
            global ioUnused
            ioUnused+=1

        #increment time
        globalTime+=1

def runRr():
    global globalTime
    global verbose

    print 'The scheduling algorithm used was Round Robin, with quantum=2'
    while not_all_processes_terminated():
        if verbose==True:
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

        # preempt
        if runningArray:
            if runningArray[0].quantum == 2:
                rr_preempt()

        if preReadyArray:
            fcfs_move_process_from_preready_to_ready()

        if not runningArray and readyArray:
            fcfs_move_process_from_ready_to_running()


        if not runningArray and not_all_processes_terminated():
            global cpuUnused
            cpuUnused+=1

        if not blockedArray and not_all_processes_terminated():
            global ioUnused
            ioUnused+=1

        #increment time
        globalTime+=1


def runLcfs():
    global globalTime
    global verbose

    print 'The scheduling algorithm used was Last Come First Served'
    while not_all_processes_terminated():
        if verbose==True:
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
            lcfs_move_process_from_preready_to_ready()

        if not runningArray and readyArray:
            lcfs_move_process_from_ready_to_running()


        if not runningArray and not_all_processes_terminated():
            global cpuUnused
            cpuUnused+=1

        if not blockedArray and not_all_processes_terminated():
            global ioUnused
            ioUnused+=1

        #increment time
        globalTime+=1

def runPsjf():
    global globalTime
    global verbose

    print 'The scheduling algorithm used was Preemptive Shortest Job First'
    while not_all_processes_terminated():
        if verbose==True:
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
            psjf_move_process_from_preready_to_ready()

        #preempt
        if runningArray:
            for process in readyArray:
                if process.totalTimeLeft<runningArray[0].totalTimeLeft:
                    rr_preempt()
                    break
            psjf_move_process_from_preready_to_ready()

        if not runningArray and readyArray:
            fcfs_move_process_from_ready_to_running()


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
    runningArray[0].quantum+=1

def update_process_io_time(process):
    process.ioTimeLeft-=1
    process.ioTimeTotal+=1

def fcfs_move_process_from_ready_to_running():

    if readyArray[0].cpuTimeLeft==0:
        readyArray[0].cpuTimeLeft=min(randomOS(readyArray[0].maxCpuBurst),readyArray[0].totalCpuTimeNeeded)
    readyArray[0].state=2
    readyArray[0].quantum=0
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

def fcfs_move_process_from_preready_to_ready():
    global preReadyArray
    tempPreReady=[]
    while preReadyArray:
        chosenProcess=preReadyArray[0]
        for i in range(1,len(preReadyArray)):
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
    for process in processArray:
        print 'Process ', processArray.index(process), ':'
        print '\t\t(A,B,C,IO) = (', process.arrivalTime, ',', process.maxCpuBurst, ',', process.totalCpuTimeNeeded, ',', process.maxIoBurst, ')'
        print '\t\tFinishing time:', process.finishingTime
        print '\t\tTurnaround time:', process.turnaroundTime
        print '\t\tI/O time:', process.ioTimeTotal
        print '\t\tWaiting time:', process.waitingTime

def print_summary_data():
    print 'Summary Data:'
    print '\t\tFinishing time:', finalFinishingTime
    print '\t\tCPU Utilization:', '%f' % ((finalFinishingTime-cpuUnused)/float(finalFinishingTime))
    print '\t\tI/O Utilization:', '%f' % ((finalFinishingTime-ioUnused)/float(finalFinishingTime))
    print '\t\tThroughput:', '%f' % ((len(processArray)/float(finalFinishingTime)) * 100) ,'processes per hundred cycles'
    print '\t\tAverage turnaround time:', '%f' % (average_turnaround())
    print '\t\tAverage waiting time:', '%f' % (average_waiting())
    print '\n\n\n'

def average_turnaround():
    sum=0
    for process in processArray:
        sum+=process.turnaroundTime
    return sum/float(len(processArray))

def average_waiting():
    sum=0
    for process in processArray:
        sum+=process.waitingTime
    return sum/float(len(processArray))

def verbose_output():
    string = 'Before cycle ' + str(globalTime) + ':'
    for process in processArray:
        if process.state==0:
            string+=' unstarted 0'
        elif process.state==1:
            string+=' ready ' + str(process.cpuTimeLeft)
        elif process.state==2:
            string += ' running ' + str(process.cpuTimeLeft)
            #string += 'running' + str(2-process.quantum)
        elif process.state==3:
            string += ' blocked ' + str(process.ioTimeLeft)
        elif process.state==4:
            string += ' terminated 0'
        elif process.state == -1:
            string += 'preready'
        else:
            string += 'error'

    string+='.'
    print(string)
    # if string!=textArray[globalTime].replace(' ',''):
    #     print(globalTime)

def lcfs_move_process_from_preready_to_ready():
    global preReadyArray
    tempPreReady = []
    while preReadyArray:
        chosenProcess = preReadyArray[0]
        for i in range(1, len(preReadyArray)):
            if preReadyArray[i].arrivalTime < chosenProcess.arrivalTime or preReadyArray[
                i].arrivalTime == chosenProcess.arrivalTime and processArray.index(
                    preReadyArray[i]) < processArray.index(chosenProcess):
                chosenProcess = preReadyArray[i]
        tempPreReady.insert(0,chosenProcess)
        preReadyArray.remove(chosenProcess)

    preReadyArray = tempPreReady
    for process in preReadyArray:
        process.state = 1
    readyArray.extend(preReadyArray)
    preReadyArray = []

def lcfs_move_process_from_ready_to_running():
    readyArray[-1].cpuTimeLeft=min(randomOS(readyArray[-1].maxCpuBurst),readyArray[-1].totalCpuTimeNeeded)
    readyArray[-1].state=2
    runningArray.append(readyArray[-1])
    readyArray.pop(-1)

def rr_preempt():
    runningArray[0].state = -1
    preReadyArray.append(runningArray[0])
    runningArray.pop(0)

def psjf_move_process_from_preready_to_ready():
    global readyArray
    global preReadyArray
    preReadyArray.extend(readyArray)
    for process in preReadyArray:
        process.state = 1
    readyArray=sorted(preReadyArray, key=lambda process: process.totalTimeLeft)
    preReadyArray=[]




#running the code
debug()

readRandom()
processArray = createProcesses()
runFcfs()
process_output_summary()
print_summary_data()
globals_to_default_values()

readRandom()
processArray = createProcesses()
runRr()
process_output_summary()
print_summary_data()
globals_to_default_values()

readRandom()
processArray = createProcesses()
runLcfs()
process_output_summary()
print_summary_data()
globals_to_default_values()

readRandom()
processArray = createProcesses()
runPsjf()
process_output_summary()
print_summary_data()
globals_to_default_values()
print('End.')

