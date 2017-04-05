# SchedulingLab
Simulation of an OS process scheduler 

There are two .py files, Scheduler.py and Process.py. 
*Process.py simply defines a class called "process".
*Scheduler.py is the program

To run program, type:
python3 Scheduler.py <input-filename> 
OR
python3 Scheduler.py --verbose <input-filename>

Note: In rare cases, the order of the processes in this program is DIFFERENT from the order in the professor's program. This is due to using the original input rather than the (sorted) input. For example, Process 0 in the program may correspond to Process 1 in the professor's.