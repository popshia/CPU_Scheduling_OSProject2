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

currentTime = 1

class Process():
    def __init__(self, ID, CPU_Burst, arrivalTime, priority):
        self.ID = ID
        self.CPU_Burst = CPU_Burst
        self.Arrival_Time = arrivalTime
        self.Priority = priority
        self.Complete_Time = 0
        self.Waiting_Time = 0
        self.Turnaround_Time = 0
        self.Done = False

class FCFS():
    def __init__(self, processList, timeSlice):
        self.Process_List = processList
        self.Time_Slice = timeSlice
        self.Gantt_Chart = ""
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_Queue = []

    def CheckProcess(self):
        for process in self.Process_List:
            if process.Arrival_Time <= currentTime:
                self.Waiting_Queue.append(self.Process_List.pop(self.Process_List.index(process)))

    def RunProcess(self):
        if not self.Running_Process:
            self.Running_Process = self.Waiting_Queue.pop(0)


    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID))
        while self.ProcessList:
            CheckProcess()
            

    def Print(self):
        print("==    FCFS==")

def ReadProcess(input, processList):
    input.readline() # read the labels
    tempArray = input.readline().split()
    while tempArray != []:
        singleProcess = Process(int(tempArray[0]), int(tempArray[1]), int(tempArray[2]), int(tempArray[3]))
        # print(singleProcess.ID, "\t", singleProcess.CPU_Burst, "\t", singleProcess.Arrival_Time, "\t", singleProcess.Priority)
        processList.append(singleProcess)
        tempArray = input.readline().split()

def main():
    inputFile = open(input("Please enter the file name you want to simulate the scheduling...\n"), 'r')
    method, timeSlice = [int(token) for token in inputFile.readline().split()]
    processList = []
    ReadProcess(inputFile, processList)
    FCFS_Simulate = FCFS(processList, timeSlice)
    FCFS_Result = FCFS_Simulate.Start()

    

if __name__ == "__main__":
    main()