# Method Description:
# 1: FCFS ( First Come First Serve )
#   • 依arrival time先後次序處理
#   • 若arrival time相同時，則依ProcessID由小至大依序處理。
# 2: RR ( Round Robin )
#   • 先依arrival time先後次序處理，時候未到的Process不能Run。
#   • 若arrival time相同時，則依ProcessID由小至大依序處理。
#   • Time out時，若有新來的Process，則讓新來的Process排在前面。
#   • 某個ProcessTime slice未用完就結束時，必須讓下一個Process執行。
# 3: PSJF ( Preemptive Shortest Job First )
#   • 由剩餘CPU Burst最小的Process先處理。
#   • 若剩餘的CPU Burst相同，讓沒有用過CPU 的先使用，無法分別時則依arrival time小的先處理。
#   • 若剩餘CPU Burst相同且arrival time相同，則依ProcessID由小至大依序處理。
# 4: NSJF ( Non-preemptive Shortest Job First )
#   • 由CPU Burst最小的Process先處理
#   • 若CPU Burst最少的Process不只一個，則依 arrival time小的先處理
#   • 若CPU Burst及arrival time相同，則依 ProcessID由小至大依序處理。
# 5: PP ( Preemptive Priority )
#   • Priority number小的代表Priority大
#   • 依Priority由大致小依序處理
#   • 若Priority相同,讓沒有用過CPU的先使用，無法分別時則依arrival time小的先處理
#   • 若Priority及arrival time均相同，則依ProcessID由小至大依序處理。
# 6: ALL

# Waiting Time = Turnaround Time – Burst Time
# Turnaround Time = Complete Time – Arrival Time

import queue

currentTime = 1

class Process():
    def __init__(self, ID, CPU_Burst, arrivalTime, priority):
        self.ID = ID
        self.CPU_Burst = CPU_Burst
        self.CPU_Burst_Minus = CPU_Burst
        self.Arrival_Time = arrivalTime
        self.Priority = priority
        self.Complete_Time = 0
        self.Waiting_Time = 0
        self.Turnaround_Time = 0

class FCFS():
    def __init__(self, processList, timeSlice):
        self.Process_List = processList
        self.Time_Slice = timeSlice
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = queue.Queue()
        self.Done_List = []

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= currentTime: # if the process have arrived
                self.Waiting_Queue.put(process) # put the process in the waiting queue

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process 
            self.Running_Process = self.Waiting_Queue.get() # get the first process in waiting queue
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = currentTime # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==    FCFS==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID)) # sort the process first by arrival time second by process ID
        while len(self.Done_List) < len(self.Process_List): # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.RunProcess() # run the current process or dispatch from waiting queue
        return self.Done_List.sort(key=lambda process: process.ID) # return done list

def ReadProcess(input, processList):
    input.readline() # read the labels
    tempArray = input.readline().split() # split every variables
    while tempArray != []: # while temp array is empty
        singleProcess = Process(int(tempArray[0]), int(tempArray[1]), int(tempArray[2]), int(tempArray[3])) # assign the four values
        processList.append(singleProcess) # append this process to process list
        tempArray = input.readline().split() # read next process

def main():
    inputFile = open(input("Please enter the file name you want to simulate the scheduling...\n"), 'r') # open file
    method, timeSlice = [int(token) for token in inputFile.readline().split()] # read method and time slice
    processList = [] # create an empty process list
    ReadProcess(inputFile, processList) # read the processes
    FCFS_Simulate = FCFS(processList, timeSlice) # create a new FCFS class
    FCFS_Result = FCFS_Simulate.Start() # start the FCFS class and return the result

    

if __name__ == "__main__":
    main()