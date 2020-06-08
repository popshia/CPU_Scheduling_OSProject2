# CPU_Scheduling_OSProject2
## 作業系統 期末Project_CPU_Scheduling（CPU排程模擬）

1. 使⽤開發環境
  * 作業系統：macOS 10.15.4 Catalina
  * 使⽤軟體：Visual Studio Code
  * 使⽤語⾔：Python

2. 流程
  * 先讀入input之第一行並儲存檔案開頭選⽤的method與timeSlice
  * 再將檔案剩下的process讀入⼀個list
  * 根據method去做執⾏不同function
  * 1：FCFS (First Come First Serve)
  * 2：RR (Round Robin)
  * 3：PSJF (Preemptive Shortest Job First)
  * 4：NSJF (Non-preemptive Shortest Job First)
  * 5：PP (Preemptive Priority)
  * 6：ALL Methods
  * 將function執行完的Gantt Chart, Waiting Time, Turnaround Time output到⼀個新的檔案（input檔名_output.txt）
	
3. 使⽤的資料結構
  * class Process ( Process Data Structure )
    * ID
    * CPU_Burst
    * CPU_Burst_Minus
    * Arrival_Time
    * Priority
    * Time_Slice
    * Complete_Time
    * Waiting_Time
    * Turnaround_Time
    * Has_Use_CPU
  * class FCFS ( FCFS_Simulate )
    *
  * queue.Queue()
  * multiprocessing.Process()
  * multiprocessing.Manager().list()
  * multiprocessing.Queue()
4. 完成的功能
  * 全數完成
