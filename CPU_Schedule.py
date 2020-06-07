# Method Description:
# 1: FCFS ( First Come First Serve )
#   • 依arrival time先後次序處理
#   • 若arrival time相同時，則依ProcessID由小至大依序處理。
# 2: RR ( Round Robin )
#   • 先依arrival time先後次序處理，時候未到的Process不能Run。
#   • 若arrival time相同時，則依ProcessID由小至大依序處理。
#   • Time out時，若有新來的Process，則讓新來的Process排在前面。
#   • 某個Process Time slice未用完就結束時，必須讓下一個Process執行。
# 3: PSJF ( Preemptive Shortest Job First )
#   • 由剩餘CPU Burst最小的Process先處理。
#   • 若剩餘的CPU Burst相同，讓沒有用過CPU的先使用，無法分別時則依arrival time小的先處理。
#   • 若剩餘CPU Burst相同且arrival time相同，則依ProcessID由小至大依序處理。
# 4: NSJF ( Non-preemptive Shortest Job First ) 
#   • 由CPU Burst最小的Process先處理
#   • 若CPU Burst最少的Process不只一個，則依 arrival time小的先處理
#   • 若CPU Burst及arrival time相同，則依 ProcessID由小至大依序處理。
# 5: PP ( Preemptive Priority )
#   • Priority number小的代表Priority大
#   • 依Priority由大致小依序處理
#   • 若Priority相同，讓沒有用過CPU的先使用，無法分別時則依arrival time小的先處理
#   • 若Priority及arrival time均相同，則依ProcessID由小至大依序處理。
# 6: ALL

# Waiting Time = Turnaround Time – Burst Time
# Turnaround Time = Complete Time – Arrival Time

import queue
import copy
from collections import deque

class Process(): # process data structure
    def __init__(self, ID, CPU_Burst, arrivalTime, priority):
        self.ID = ID
        self.CPU_Burst = CPU_Burst
        self.CPU_Burst_Minus = 0
        self.Arrival_Time = arrivalTime
        self.Priority = priority
        self.Time_Slice = 0
        self.Complete_Time = 0
        self.Waiting_Time = 0
        self.Turnaround_Time = 0
        self.Has_Use_CPU = False

class FCFS(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                self.Waiting_Queue.append(process) # put the process in the waiting queue
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: # if can't find
                pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process 
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: return # if there's no more process in queue  
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==    FCFS==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID)) # sort the process first by arrival time second by process ID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Print() # print the gantt chart
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class RR(): # buggy
    def __init__(self, processList, timeSlice):
        self.Process_List = processList
        self.Time_Slice = timeSlice
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = deque()
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1
        self.Time_Out = False

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                if self.Time_Out: # if there's time out
                    self.Waiting_Queue.appendleft(self.Process_List.pop(self.Process_List.index(process))) # put the process in the front of the waiting queue
                else: # if there's no time out
                    self.Waiting_Queue.append(self.Process_List.pop(self.Process_List.index(process))) # put the process in the waiting queue
        self.Time_Out = False # reset time out boolean

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.popleft() # get the first process in waiting queue
            else: # if there's no more process in queue
                return # return
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu burst time
        self.Running_Process.Time_Slice -= 1 # minus the time slice by one
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.Time_Slice == 0: # if the current running process has run out of time slice
            if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
                self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
                self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
                self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
                self.Done_List.append(self.Running_Process) # append the complete process into done list
                self.Running_Process = None # set running process to none
                self.Time_Out = True
                return # return
            else: # if the process hasn't complete
                self.Running_Process.Time_Slice = self.Time_Slice # reset the time slice
                self.Waiting_Queue.append(self.Running_Process) # put the process back to the waiting queue
                self.Running_Process = None # set running process to none
                self.Time_Out = True
                return # return
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==      RR==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID)) # sort the process first by arrival time second by process ID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Print() # print the gantt chart
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class PSJF(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                if self.Running_Process: # if there's a current running process
                    if process.CPU_Burst_Minus <= self.Running_Process.CPU_Burst_Minus: # if the upcoming process cpu burst is smaller or equal to the current running process
                        self.Waiting_Queue.append(self.Running_Process) # append the current running process
                        self.Running_Process = process # snatched the current process
                    else: # if the upcoming process cpu burst is greater to the current running process
                        self.Waiting_Queue.append(process) # put the process in the waiting queue
                else: # no current running process
                    self.Waiting_Queue.append(process) # put the process in the waiting queue
        try: # try  
            self.Process_List.pop(self.Process_List.index(self.Running_Process)) # remove the unpoped process due to the snatching
        except: pass # pass
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process 
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: # if there's no more process in queue
                return # return
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        self.Running_Process.Has_Use_CPU = True
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==    PSJF==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.CPU_Burst, process.ID)) # sort the process first by cpu burst second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.CPU_Burst_Minus, process.Has_Use_CPU, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Print() # print the gantt chart
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class NSJF(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                self.Waiting_Queue.append(process) # put the process in the waiting queue
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: # if can't find
                pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process 
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: return # if there's no more process in queue
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==    NSJF==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.CPU_Burst, process.ID)) # sort the process first by cpu burst second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.CPU_Burst, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Print() # print the gantt chart
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class PP():
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                if self.Running_Process: # if there's a current running process
                    if process.Priority <= self.Running_Process.Priority: # if the upcoming process cpu burst is smaller or equal to the current running process
                        self.Waiting_Queue.append(self.Running_Process) # append the current running process
                        self.Running_Process = process # snatched the current process
                    else: # if the upcoming process cpu burst is greater to the current running process
                        self.Waiting_Queue.append(process) # put the process in the waiting queue
                else: # no current running process
                    self.Waiting_Queue.append(process) # put the process in the waiting queue
        try: # try  
            self.Process_List.pop(self.Process_List.index(self.Running_Process)) # remove the unpoped process due to the snatching
        except: pass # pass
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process 
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: # if there's no more process in queue
                return # return
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        self.Running_Process.Has_Use_CPU = True # set this process has used CPU
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += ord(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Print(self):
        print("==      PP==") # print label
        print(self.Gantt_Chart) # print gantt chart

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.Priority, process.ID)) # sort the process first by priority second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.Priority, process.Has_Use_CPU, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Print() # print the gantt chart
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

def ReadProcess(input, processList):
    input.readline() # read the labels
    tempArray = input.readline().split() # split every variables
    while tempArray != []: # while temp array is empty
        singleProcess = Process(int(tempArray[0]), int(tempArray[1]), int(tempArray[2]), int(tempArray[3])) # assign the four values
        processList.append(singleProcess) # append this process to process list
        tempArray = input.readline().split() # read next process

def PrintResult(doneList):
    print("============\n")
    print("Waiting Time\nID      Time\n============")
    for index in range(len(doneList)): print( doneList[index].ID, "\t", doneList[index].Waiting_Time )
    print("============\n\nTurnaround Time\nID      Time\n============")
    for index in range(len(doneList)): print( doneList[index].ID, "\t", doneList[index].Turnaround_Time )
    print("============")

def main():
    #inputFile = open(input("Please enter the file name you want to simulate the scheduling...\n"), 'r') # open file
    inputFile = open("input.txt", 'r')
    method, timeSlice = [int(token) for token in inputFile.readline().split()] # read method and time slice
    processList = [] # create an empty process list
    ReadProcess(inputFile, processList) # read the processes
    for process in processList: process.Time_Slice = timeSlice # add time slice to eash process
    if method == 1: # FCFS (First Come First Serve)
        FCFS_Process_List = copy.deepcopy(processList) # create a FCFS process list
        FCFS_Simulate = FCFS(FCFS_Process_List) # create a new FCFS class
        FCFS_Simulate.Start() # start the FCFS class
        PrintResult(FCFS_Simulate.Done_List) # print results
    elif method == 2: # RR (Round Robin)
        RR_Process_List = copy.deepcopy(processList) # create a RR process list
        RR_Simulate = RR(RR_Process_List, timeSlice) # create a new RR class
        RR_Simulate.Start() # start the RR class
        PrintResult(RR_Simulate.Done_List) # print results
    elif method == 3: # PSJF (Preemptive Shortest Job First)
        PSJF_Process_List = copy.deepcopy(processList) # create a PSJF process list
        PSJF_Simulate = PSJF(PSJF_Process_List) # create a new PSJF class
        PSJF_Simulate.Start() # start the PSJF class
        PrintResult(PSJF_Simulate.Done_List) # print results
    elif method == 4: # NSJF (Non-preemptive Shortest Job First)
        NSJF_Process_List = copy.deepcopy(processList) # create a NSJF process list
        NSJF_Simulate = NSJF(NSJF_Process_List) # create a new NSJF class
        NSJF_Simulate.Start() # start the NJSF class
        PrintResult(NSJF_Simulate.Done_List) # print results
    elif method == 5: # PP (Preemptive Priority)
        PP_Process_List = copy.deepcopy(processList) # create a PP process list
        PP_Simulate = PP(PP_Process_List)     # create a new PP class
        PP_Simulate.Start() # start the PP class
        PrintResult(PP_Simulate.Done_List) # print results
    elif method == 6: # ALL
        FCFS_Process_List = copy.deepcopy(processList) # create a FCFS process list
        RR_Process_List   = copy.deepcopy(processList) # create a RR process list
        PSJF_Process_List = copy.deepcopy(processList) # create a PSJF process list
        NSJF_Process_List = copy.deepcopy(processList) # create a NSJF process list
        PP_Process_List   = copy.deepcopy(processList) # create a PP process list
        FCFS_Simulate = FCFS(FCFS_Process_List) # create a new FCFS class
        RR_Simulate   = RR(RR_Process_List, timeSlice)     # create a new RR class
        PSJF_Simulate = PSJF(PSJF_Process_List) # create a new PSJF class
        NSJF_Simulate = NSJF(NSJF_Process_List) # create a new NSJF class
        PP_Simulate   = PP(PP_Process_List)     # create a new PP class
        FCFS_Simulate.Start() # start the FCFS class
        RR_Simulate.Start()   # start the FCFS class
        PSJF_Simulate.Start() # start the PSJF class
        NSJF_Simulate.Start() # start the NJSF class
        PP_Simulate.Start()   # start the PP class
        # print results
        print("===========================================================\n")
        print("Waiting Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================")
        for index in range(len(processList)): print( FCFS_Simulate.Done_List[index].ID, "\t", FCFS_Simulate.Done_List[index].Waiting_Time, "\t", RR_Simulate.Done_List[index].Waiting_Time, "\t", PSJF_Simulate.Done_List[index].Waiting_Time, "\t", NSJF_Simulate.Done_List[index].Waiting_Time, "\t", PP_Simulate.Done_List[index].Waiting_Time )
        print("===========================================================\n\nTurnaround Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================")
        for index in range(len(processList)): print( FCFS_Simulate.Done_List[index].ID, "\t", FCFS_Simulate.Done_List[index].Turnaround_Time, "\t", RR_Simulate.Done_List[index].Turnaround_Time, "\t", PSJF_Simulate.Done_List[index].Turnaround_Time, "\t", NSJF_Simulate.Done_List[index].Turnaround_Time, "\t", PP_Simulate.Done_List[index].Turnaround_Time )
        print("===========================================================")

if __name__ == "__main__":
    main()