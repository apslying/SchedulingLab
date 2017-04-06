class Process:
    quantum=0
    state=0
    cpuTimeLeft=0
    ioTimeLeft=0
    finishingTime=0
    waitingTime=0
    turnaroundTime=0
    ioTimeTotal=0
    def __init__(self, arrivalTime, maxCpuBurst, totalCpuTimeNeeded, maxIoBurst):
        self.arrivalTime=arrivalTime
        self.maxCpuBurst=maxCpuBurst
        self.totalCpuTimeNeeded=totalCpuTimeNeeded
        self.maxIoBurst=maxIoBurst
        self.totalTimeLeft=totalCpuTimeNeeded
#

# for num in reversed(a):
#     print(a,num)
#     if num==20:
#         a.pop(a.index(20))

# for i in range(0,len(a)):
#     if a[i]==20:
#         a.pop(i)


# file=open('input-7.txt', mode='r')
# a=file.read()
# print(a)
# a=a.replace('    ','   ')
# print(a)
#
# arr=a.split(sep='  ')
# print(arr)
