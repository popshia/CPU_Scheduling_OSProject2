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
		* 先依arrival time排序所有process
		* 執行CheckProcess()將抵達的process放進Waiting_Queue
		* 執行RunProcess()dispatch並執行Waiting_Queue中的process
    * 2：RR (Round Robin)
		* 先依arrival time排序所有process
		* 執行CheckProcess()將抵達的process放進Waiting_Queue
			* 如果Running_Process將自己的Time_Slice用完，則放入Waiting_Queue之後
		* 執行RunProcess()執行目前Running_Process或dispatch並執行Waiting_Queue中的process
			* 如果Running_Process執行完畢，則放入Done_List
    * 3：PSJF (Preemptive Shortest Job First)
		* 先依CPU_Burst排序所有process
		* 執行CheckProcess()將抵達的process放進Waiting_Queue
			* 如果下一個process的CPU_Burst小於先前Running_Process則搶奪
		* 執行RunProcess()執行目前Running_Process或dispatch並執行Waiting_Queue中的process
			* 如果Running_Process執行完畢，則放入Done_List
    * 4：NSJF (Non-preemptive Shortest Job First)
		* 先依CPU_Burst排序所有process
		* 執行CheckProcess()將抵達的process放進Waiting_Queue
		* 執行RunProcess()執行目前Running_Process或dispatch並執行Waiting_Queue中的process
			* 如果Running_Process執行完畢，則放入Done_List
    * 5：PP (Preemptive Priority)
		* 先依Priority排序所有process
		* 執行CheckProcess()將抵達的process放進Waiting_Queue
			* 如果下一個process的priority大於先前Running_Process則搶奪
		* 執行RunProcess()執行目前Running_Process或dispatch並執行Waiting_Queue中的process
			* 如果Running_Process執行完畢，則放入Done_List
    * 6：ALL Methods
    * 將function執行完的Gantt Chart, Waiting Time, Turnaround Time output到⼀個新的檔案（input檔名_output.txt）
	
3. 使⽤的資料結構
	```Python
	class FCFS():
    	def __init__(self, processList):
        	self.Process_List = processList
        	self.Gantt_Chart = "-"
        	self.Running_Process = None
        	self.Waiting_Queue = []
        	self.Done_List = []
        	self.Process_Quantity = len(processList)
        	self.Current_Time = 1
		def CheckProcess(self):
		def RunProcess(self):
		def Start():
	```
	```Python
    class FCFS ( FCFS_Simulate )
        * list: Process_List
        * string: Gantt_Chart
        * Process: Running_Process
        * list: Waiting_Queue
        * list: Done_List
        * int: Process_Quantity
        * int: Current_Time
        * function: CheckProcess()
        * function: RunProcess()
        * function: Start()
	```
	```Python
    class RR ( RR_Simulate )
    	* list: Process_List
    	* int: Time_Slice
    	* string: Gantt_Chart
    	* Process: Running_Process
    	* list: Waiting_Queue
    	* list: Done_List
    	* int: Process_Quantity
    	* int: Current_Time
    	* function: CheckProcess()
    	* function: RunProcess()
    	* function: Start()
	```
	```Python
    class PSJF ( PSJF_Simulate )
    	* variable: Process_List
    	* variable: Gantt_Chart
    	* variable: Running_Process
    	* variable: Waiting_Queue
    	* variable: Done_List
    	* variable: Process_Quantity
    	* variable: Current_Time
    	* function: CheckProcess()
    	* function: RunProcess()
    	* function: Start()
	```
	```Python
    class NPSJF ( NPSJF_Simulate )
    	* variable: Process_List
    	* variable: Gantt_Chart
    	* variable: Running_Process
    	* variable: Waiting_Queue
    	* variable: Done_List
    	* variable: Process_Quantity
    	* variable: Current_Time
    	* function: CheckProcess()
    	* function: RunProcess()
    	* function: Start()
	```
	```Python
    class PP ( PP_Simulate )
    	* variable: Process_List
    	* variable: Gantt_Chart
    	* variable: Running_Process
    	* variable: Waiting_Queue
    	* variable: Done_List
    	* variable: Process_Quantity
    	* variable: Current_Time
    	* function: CheckProcess()
    	* function: RunProcess()
    	* function: Start()
	```

4. 未完成的功能
  	* 無（全數完成）
