class Process:
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
a=[10,20,30,40,50]
a.extend([60,70])
print(a)
# for num in reversed(a):
#     print(a,num)
#     if num==20:
#         a.pop(a.index(20))

# for i in range(0,len(a)):
#     if a[i]==20:
#         a.pop(i)