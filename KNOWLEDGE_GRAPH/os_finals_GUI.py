import wx
import wx.grid
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import time
import sys
import copy
import re


user_processes = []
class ReadOnlyDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        for key, value in args[0].items():
            if key not in self:
                super().__setitem__(key, value)

    def __delitem__(self, key):
        # Ignore deletion
        return


class Process:
    def __init__(self, process_id, arrival_time, execution_time, color):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.begin_exec_time = 0
        self.preempted_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.overstayed = False
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.alloted_time = 0
        self.color = color
        self.is_input_output = False
        self.currentQueue = "_"

    def execute(self, time_quantum=None):
        if time_quantum is None:
            self.remaining_time = 0
        else:
            self.remaining_time -= time_quantum
            self.alloted_time = time_quantum
            if self.remaining_time < 0:
                self.remaining_time = 0
        self.waiting_time += 1


##Round Robbin
class RoundRobin_Scheduler:
    def __init__(self, time_quantum):
        self.ready_queue = []
        self.waiting_queue = []
        self.time_quantum = time_quantum
        self.clock = 0
        self.current_process = None
        self.final_stats = ReadOnlyDict()


    def add_process(self, process):
        self.waiting_queue.append(process)
        self.waiting_queue.sort(key=lambda x: x.arrival_time)

    def execute_next_process(self):        
        self.waiting_queue.sort(key=lambda p: p.arrival_time)
        index = 0
        while index < len(self.waiting_queue):
            if self.waiting_queue[index].arrival_time <= self.clock:  
                self.ready_queue.append(self.waiting_queue.pop(index))
            else:
                index += 1
        
        for process in self.ready_queue:  
            if process.remaining_time < 1:
                self.ready_queue.remove(process)

        if(self.current_process == None):
            if len(self.ready_queue) == 0:
                self.clock += 1
                self.current_process = Process(0, 0, 0, 'White')
                return self.current_process
            if len(self.ready_queue) > 0:
                self.current_process = self.ready_queue.pop(0)
                self.clock = self.current_process.arrival_time
                self.current_process.begin_exec_time = self.clock
                self.clock += (min(self.current_process.remaining_time, self.time_quantum))
                self.current_process.execute(min(self.current_process.remaining_time, self.time_quantum))
                return self.current_process

        elif(self.current_process.process_id == 0 and len(self.ready_queue) == 0):
            self.clock +=1
            return self.current_process
        
        elif(self.current_process.process_id == 0 and len(self.ready_queue) > 0):
            self.current_process = self.ready_queue.pop(0)
            self.current_process.begin_exec_time = self.clock
            self.clock += (min(self.current_process.remaining_time, self.time_quantum))
            self.current_process.execute(min(self.current_process.remaining_time, self.time_quantum))
            return self.current_process
        
        if (self.current_process.remaining_time > 0):
                if len(self.ready_queue) > 0:
                   ##Removing from ready queue
                   self.current_process.preempted_time = self.clock
                   self.ready_queue.append(self.current_process)

                   ##Setting a new current process
                   self.current_process = self.ready_queue.pop(0)
                   self.current_process.begin_exec_time = self.clock
                   
                   self.clock = self.clock + (min(self.time_quantum, self.current_process.remaining_time))
                   self.current_process.execute(min(self.time_quantum, self.current_process.remaining_time))
                   return self.current_process

                elif(len(self.ready_queue) == 0 and len(self.waiting_queue) > 0):
                    self.current_process.begin_exec_time = self.clock
                    self.current_process.execute(1)
                    self.clock +=1
                    return self.current_process

                elif(len(self.ready_queue) == 0 and len(self.waiting_queue) == 0):
                    self.current_process.begin_exec_time = self.clock
                    self.clock += self.current_process.remaining_time
                    self.current_process.execute(self.current_process.remaining_time)
                    return self.current_process


        if (self.current_process.remaining_time == 0):
                ##Updating final statistics once the process is done
                process_id = f"P{self.current_process.process_id}"
                process_information = {
                    "arrival_time" :  self.current_process.arrival_time,
                    "execution_time" : self.current_process.execution_time,
                    "completion_time" : self.clock
                }
                self.final_stats[process_id] = process_information

                if len(self.ready_queue) > 0:
                   self.current_process.preempted_time = self.clock
                   self.ready_queue.append(self.current_process)
                   ##Setting a new current process
                   self.current_process = self.ready_queue.pop(0)
                   self.current_process.begin_exec_time = self.clock
                   self.clock += (min(self.time_quantum, self.current_process.remaining_time))
                   self.current_process.execute(min(self.time_quantum, self.current_process.remaining_time))
                   return self.current_process
                    
                elif(len(self.ready_queue) == 0 and len(self.waiting_queue) > 0):
                    self.current_process.begin_exec_time = self.clock
                    self.current_process.execute(0)
                    self.clock +=1
                    return self.current_process

                elif(len(self.ready_queue)==0 and len(self.waiting_queue)==0):
                    return None


    def calculate_statistics(self):
        total_waiting_time = sum(process.waiting_time for process in self.final_stats)
        average_waiting_time = total_waiting_time / len(self.final_stats) if len(self.final_stats) > 0 else 0
        return total_waiting_time, average_waiting_time

    def create_gantt_chart_panel(self, parent):
        return GanttPanel(parent, self)
    
    def print_final_stats(self):
        return self.final_stats


class Preemptive_SJF_Scheduler:
    def __init__(self):
        self.ready_queue = []
        self.serviced = []
        self.waiting_queue = []
        self.current_process = None
        self.final_stats = ReadOnlyDict()
        self.clock = 0

    def execute_next_process(self):
        self.waiting_queue.sort(key=lambda p: p.arrival_time)
        index = 0
        while index < len(self.waiting_queue):
            if self.waiting_queue[index].arrival_time <= self.clock:  
                self.ready_queue.append(self.waiting_queue.pop(index))
            else:
                index += 1

        # if(self.current_process == None):
        #     self.current_process = self.ready_queue.pop(0)
        #     self.clock = self.current_process.arrival_time
        #     self.current_process.execute(1)
        #     self.current_process.begin_exec_time = self.clock
        #     self.clock +=1
        #     return self.current_process
        
        if(self.current_process == None):
            if len(self.ready_queue) == 0:
                self.clock += 1
                self.current_process = Process(0, 0, 0, 'White')
                return self.current_process
            if len(self.ready_queue) > 0:
                self.current_process = self.ready_queue.pop(0)
                self.current_process.execute(1)
                self.current_process.begin_exec_time = self.clock
                self.clock +=1
                return self.current_process
                
        elif(self.current_process.process_id == 0 and len(self.ready_queue) == 0):
            self.clock +=1
            return self.current_process
        
        elif(self.current_process.process_id == 0 and len(self.ready_queue) > 0):
            self.current_process = self.ready_queue.pop(0)
            self.current_process.execute(1)
            self.current_process.begin_exec_time = self.clock
            self.clock +=1
            return self.current_process 

        if(self.current_process.remaining_time == 0):
                ##Updating final statistics once the process is done
                process_id = f"P{self.current_process.process_id}"
                process_information = {
                    "arrival_time" :  self.current_process.arrival_time,
                    "execution_time" : self.current_process.execution_time,
                    "completion_time" : self.clock
                }
                self.final_stats[process_id] = process_information
                self.ready_queue.extend(self.serviced)
                self.serviced.clear()

                if(len(self.ready_queue) == 0 and len(self.waiting_queue)!= 0):
                    self.current_process.begin_exec_time = self.clock
                    self.current_process.execute(0)
                    self.clock +=1
                    return self.current_process
                                
                if(len(self.ready_queue) > 0):
                    self.current_process = min(self.ready_queue, key=lambda x: x.remaining_time)
                    for process in self.ready_queue:
                        if process.process_id == self.current_process.process_id:
                            self.ready_queue.remove(process)

                    #self.current_process = self.ready_queue.pop(0)
                    self.current_process.begin_exec_time = self.clock
                    self.current_process.execute(1)
                    self.clock +=1
                    return self.current_process
    
        elif self.current_process.remaining_time > 0 and len(self.ready_queue) > 0:
                new_min = min(self.ready_queue, key=lambda x: x.remaining_time)
                if(self.current_process.remaining_time > new_min.remaining_time):
                        print("I got here")
                        self.serviced.append(self.current_process)
                        self.current_process = new_min
                        for process in self.ready_queue:
                            if process.process_id == self.current_process.process_id:
                                self.ready_queue.remove(process)
                        self.current_process.execute(1)
                        self.current_process.begin_exec_time = self.clock
                        self.clock +=1
                        return self.current_process

                elif(self.current_process.remaining_time <= new_min.remaining_time):
                        self.current_process.begin_exec_time = self.clock
                        self.current_process.execute(1)
                        self.clock +=1
                        return self.current_process
        
        elif self.current_process.remaining_time > 0 and len(self.ready_queue) == 0:
             self.current_process.begin_exec_time = self.clock
             self.current_process.execute(1)
             self.clock +=1
             return self.current_process
        
        elif(len(self.ready_queue) == 0 and len(self.waiting_queue) == 0):
                return None
    

    def add_process(self, process):
        self.waiting_queue.append(process)


    def calculate_statistics(self):
        total_waiting_time = sum(process.waiting_time for process in self.final_stats)
        average_waiting_time = total_waiting_time / len(self.final_stats) if len(self.final_stats) > 0 else 0
        return total_waiting_time, average_waiting_time


    def create_gantt_chart_panel(self, parent):
        return GanttPanel(parent, self)




class MLFQ_Scheduler:
    def __init__(self):
        self.rr_queue1 = RoundRobin_Scheduler(2)
        self.rr_queue2 = RoundRobin_Scheduler(4)
        self.fcfs_queue = []
        self.final_stats = ReadOnlyDict()
        self.fcfs_final_stats = {}
        self.clock = 0
        self.received_quantum_rr1 = []
        self.received_quantum_rr2 = []

    def add_process(self, process):
        self.rr_queue1.add_process(process)
        for process in self.rr_queue1.waiting_queue:
            process.currentQueue = 1

    def move_processes_queue1(self):
        ##Ordering First RR queue
        if len(self.received_quantum_rr1) > 0:
            for process in self.received_quantum_rr1:
                if process is not None  and process.remaining_time > 0:
                    self.demote_process(process, 2, 1)

    def move_processes_queue2(self):
        ##Ordering Second RR Queue
        if len(self.received_quantum_rr2) > 0:
            for process in self.received_quantum_rr2:
                if process is not None  and process.remaining_time > 0:
                    self.demote_process(process, 3, 2)


    def move_processes_fcfs_queue(self):
        for process in self.fcfs_queue:
                if process.is_input_output == True:
                    self.promote_process(process, 1, 3)

    def promote_process(self, promoted_process, new_queue_index, old_queue_index):
        if new_queue_index == 1:
            promoted_process.currentQueue = new_queue_index
            self.rr_queue1.ready_queue.append(promoted_process)
        if old_queue_index == 3:
            for process in self.fcfs_queue:
                if  (process.process_id == promoted_process.process_id):
                     self.fcfs_queue.remove(process)


    def demote_process(self, demoted_process,  new_queue_index, old_queue_index):
        if new_queue_index == 2:
            demoted_process.currentQueue = new_queue_index
            self.rr_queue2.ready_queue.append(demoted_process)
            if old_queue_index == 1:
                for process in self.rr_queue1.ready_queue:
                    if  (process.process_id == demoted_process.process_id):
                        self.rr_queue1.ready_queue.remove(process)

        if new_queue_index == 3:
            demoted_process.currentQueue = new_queue_index
            self.fcfs_queue.append(demoted_process)
            if old_queue_index == 2:
                for process in self.rr_queue2.ready_queue:
                    if  (process.process_id == demoted_process.process_id):
                        self.rr_queue2.ready_queue.remove(process)


    def execute_next_process(self):
        self.move_processes_queue1()
        self.move_processes_queue2()
        self.move_processes_fcfs_queue()
        
        if  (self.clock == 0  or len(self.rr_queue1.ready_queue) > 0):
            process_to_exec = self.rr_queue1.execute_next_process()
            self.received_quantum_rr1.append(process_to_exec)
            self.clock = self.rr_queue1.clock
            if process_to_exec != None:
                return process_to_exec 
        
        elif(len(self.rr_queue1.ready_queue) == 0) and (len(self.rr_queue1.waiting_queue) > 0):
            process_to_exec = self.rr_queue1.execute_next_process()
            self.received_quantum_rr1.append(process_to_exec)
            self.clock = self.rr_queue1.clock
            if process_to_exec != None:
                return process_to_exec
          
        elif(len(self.rr_queue1.ready_queue) == 0 and len(self.rr_queue1.waiting_queue) == 0) and (len(self.rr_queue2.ready_queue) > 0):
            self.rr_queue2.clock = self.clock  
            self.rr_queue2.current_process = self.rr_queue2.ready_queue.pop(0)
            process_to_exec = self.rr_queue2.execute_next_process()
            self.received_quantum_rr2.append(process_to_exec)
            self.clock = self.rr_queue2.clock
            if process_to_exec != None:  
                return process_to_exec
            if process_to_exec == None:

                if(len(self.fcfs_queue) > 0):
                    process_to_exec = self.fcfs_queue[0]


                    if self.clock < process_to_exec.arrival_time:
                        process_to_exec.begin_exec_time = self.clock
                        process_to_exec.execute(0)
                        self.clock += 1
                        return process_to_exec
                    

                    if  self.clock >= process_to_exec.arrival_time:
                        process_to_exec.begin_exec_time = self.clock
                        self.clock += process_to_exec.remaining_time
                        process_id = f"P{process_to_exec.process_id}"
                        process_information = {
                            "arrival_time" :  process_to_exec.arrival_time,
                            "execution_time" : process_to_exec.execution_time,
                            "completion_time" : self.clock
                        }

                        self.fcfs_final_stats[process_id] = process_information
                        process_to_exec.execute(process_to_exec.remaining_time)
                        self.fcfs_queue.pop(0)

                        self.final_stats.update(self.rr_queue1.final_stats)
                        self.final_stats.update(self.rr_queue2.final_stats)
                        self.final_stats.update(self.fcfs_final_stats)

                        if process_to_exec != None:  
                            return process_to_exec
                else:
                    return None
          
    def create_gantt_chart_panel(self, parent):
        return GanttPanel(parent, self)



class ProcessInputDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER)

        self.colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000']

        self.SetSize((600, 400))  

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.grid.Grid(self)
        grid.CreateGrid(10, 2) 
        grid.SetColLabelValue(0, "Arrival Time")
        grid.SetColLabelValue(1, "Execution Time")

        font = grid.GetDefaultCellFont()
        font.SetPointSize(14)
        grid.SetDefaultCellFont(font)
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        grid.SetColSize(0, 150)  
        grid.SetColSize(1, 150)  

        for i in range(10):
            grid.SetRowSize(i, 40)  

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, border=5)

        btn_ok = wx.Button(self, wx.ID_OK, label="OK")
        btn_ok.SetBackgroundColour(wx.Colour(0, 255, 0))  
        btn_ok.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        btn_cancel = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        btn_cancel.SetBackgroundColour(wx.Colour(255, 0, 255))  
        btn_cancel.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_box.Add(btn_ok, 0, wx.ALL, 5)
        btn_box.Add(btn_cancel, 0, wx.ALL, 5)

        sizer.Add(btn_box, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.grid = grid
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)


    def show_error_dialog(self, message):
        dlg = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()


    def on_ok(self, event):
        for i in range(10):
            arrival_text = self.grid.GetCellValue(i, 0).strip() 
            execution_text = self.grid.GetCellValue(i, 1).strip()
            if not arrival_text or not execution_text:
                continue
            
            # Validating arrival and execution times using regular expressions
            if not re.match(r'^\d*$', arrival_text) or not re.match(r'^\d*$', execution_text):
                error_message = "Arrival and execution times should only contain digits and spaces."
                self.show_error_dialog(error_message)
                raise ValueError(error_message)
            
            arrival = int(arrival_text)
            execution = int(execution_text)
            if arrival < 0 or execution < 0:
                error_message = "Arrival and execution times cannot be negative."
                self.show_error_dialog(error_message)
                raise ValueError(error_message)
            
            color = self.colors[i]
            user_processes.append(Process(len(user_processes) + 1, arrival, execution, color))
            self.EndModal(wx.ID_OK)


    def on_cancel(self, event):
            self.GetParent().Close()  
            self.EndModal(wx.ID_CANCEL)  
            sys.exit()


class GanttPanel(wx.Panel):
    def __init__(self, parent, scheduler):
        super().__init__(parent)
        self.scheduler = scheduler
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


    def update_gantt_chart(self, gantt_data):
        ax = self.figure.add_subplot(111)
        ax.clear()
        yticks = [0.5]
        labels = ['']
        colors = []
        total_duration = sum(p['duration'] for p in gantt_data)

   
        ax.set_xticks(range(0, total_duration+1, 1))
        ax.set_xticklabels(range(0, total_duration+1, 1))

        for i, p in enumerate(gantt_data):
            color = p['color']
            colors.append(color)
            ax.broken_barh([(p['start'], p['duration'])], (i, 1), facecolors=color)


            text_x = p['start'] + p['duration'] / 2
            text_y = i + 0.5
            ax.text(text_x, text_y, f'P{p["process_id"]}:Q{p["queue"]}', color='black', fontsize=6,  ha='center', va='center')
            yticks.append(i + 1)
            labels.append(f'P{p["process_id"]}')  
            
            # Drawing the current process
            ax.set_yticks(yticks)
            ax.set_yticklabels(labels)
            ax.set_xlabel('Time')
            ax.set_ylabel('Processes')
            ax.set_title('Gantt Chart')
            ax.grid(True)
            self.canvas.draw()
            
            time.sleep(0.3) 



class StatisticsPanel(wx.Panel):
    def __init__(self, parent, scheduler): 
        super().__init__(parent)
        self.scheduler = scheduler
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.create_statistics()

    def create_statistics(self):
        if self.scheduler is not None and self.scheduler.final_stats is not None:
            final_stats = self.scheduler.final_stats
            
            # Get headers
            headers = ['Process ID', 'Arrival Time', 'Execution Time', 'Completion Time', 'Waiting Time', 'Turnaround Time']
            
            # Get data
            data = []
            total_waiting_time = 0
            total_turnaround_time = 0
            for process_id, stats in final_stats.items():
                arrival_time = stats['arrival_time']
                execution_time = stats['execution_time']
                completion_time = stats['completion_time']
                waiting_time = completion_time - arrival_time - execution_time
                turnaround_time = completion_time - arrival_time
                data.append([process_id, arrival_time, execution_time, completion_time, waiting_time, turnaround_time])
                total_waiting_time += waiting_time
                total_turnaround_time += turnaround_time
            
            # Calculate overall average statistics
            num_processes = len(final_stats)
            overall_average_waiting_time = total_waiting_time / num_processes
            overall_average_turnaround_time = total_turnaround_time / num_processes
            
            # Create a grid
            grid = wx.grid.Grid(self)
            grid.CreateGrid(len(data) + 1, len(headers))  # +1 for the overall average row
            
            # Set headers
            for col, header in enumerate(headers):
                grid.SetColLabelValue(col, header)
            
            # Set data
            for row, row_data in enumerate(data):
                for col, value in enumerate(row_data):
                    grid.SetCellValue(row, col, str(value))
            
            # Set column sizes
            for col in range(len(headers)):
                grid.SetColSize(col, 100)  # Set the width to 200 pixels
            
            # Set overall average row
            grid.SetCellValue(len(data), 0, "Overall Average")
            grid.SetCellValue(len(data), 4, str(overall_average_waiting_time))
            grid.SetCellValue(len(data), 5, str(overall_average_turnaround_time))
            
            # Add grid to sizer
            self.sizer.Add(grid, 1, wx.EXPAND)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Scheduling Simulation", size=(1000, 800))
        self.panel = wx.Panel(self)
        self.main_box = wx.BoxSizer(wx.VERTICAL)

        dlg = ProcessInputDialog(self, "Process Input")
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()

        self.scheduler_buttons = []
        self.rr_button = wx.Button(self.panel, label="Round Robin")
        self.preemptive_sjf_button = wx.Button(self.panel, label="Preemptive SJF")
        self.mlfq_button = wx.Button(self.panel, label="Multi-level Feeback Queue")


        self.rr_button.Bind(wx.EVT_BUTTON, self.on_rr)
        self.preemptive_sjf_button.Bind(wx.EVT_BUTTON, self.on_preemptive_sjf)
        self.mlfq_button.Bind(wx.EVT_BUTTON, self.on_mlfq)

        self.scheduler_buttons.extend([self.rr_button, self.preemptive_sjf_button, self.mlfq_button])

        button_box = wx.BoxSizer(wx.HORIZONTAL)
        for button in self.scheduler_buttons:
            button_box.Add(button, 1, wx.EXPAND | wx.ALL, border=5)

        self.main_box.Add(button_box, 0, wx.EXPAND | wx.ALL, border=5)

        scrolled_window = wx.ScrolledWindow(self.panel)
        scrolled_window.SetScrollbars(1, 1, 1, 1)
        scrolled_window_sizer = wx.BoxSizer(wx.VERTICAL)

        self.gantt_panel = GanttPanel(scrolled_window, None)
        self.statistics_panel = StatisticsPanel(scrolled_window, None)

        scrolled_window_sizer.Add(self.gantt_panel, 0, wx.EXPAND | wx.ALL, border=5)
        scrolled_window_sizer.Add(self.statistics_panel, 0, wx.EXPAND | wx.ALL, border=5)

        scrolled_window.SetSizer(scrolled_window_sizer)

        self.main_box.Add(scrolled_window, 1, wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel.SetSizer(self.main_box)
        self.Layout()


    def on_close(self, event):
        print("Goodbye")
        sys.exit()

    def on_rr(self, event):
        processes = self.generate_processes()
        self.create_scheduler(lambda: RoundRobin_Scheduler(2), processes)

    def on_preemptive_sjf(self, event):
        processes = self.generate_processes()
        self.create_scheduler(Preemptive_SJF_Scheduler, processes)


    def on_mlfq(self, event):
        processes = self.generate_processes()
        self.create_scheduler(MLFQ_Scheduler, processes)


    def generate_processes(self):
        return copy.deepcopy(user_processes)


    def create_scheduler(self, scheduler_class, processes):
        if self.gantt_panel:
            self.gantt_panel.Destroy()
        if self.statistics_panel:
            self.statistics_panel.Destroy()
        self.current_scheduler = scheduler_class()
        for process in processes:
            self.current_scheduler.add_process(process)
        self.gantt_panel = self.current_scheduler.create_gantt_chart_panel(self.panel)
        self.main_box.Add(self.gantt_panel, 0, wx.EXPAND | wx.ALL, border=5)
        self.panel.Layout()
        self.update_gantt_chart()
        self.update_statistics()
     

    def update_gantt_chart(self):
        if self.current_scheduler and self.gantt_panel:
            gantt_data = []
            while True:
                current_process = self.current_scheduler.execute_next_process()
                if current_process is None:
                    break
                gantt_data.append({'start': current_process.begin_exec_time, 'duration': current_process.alloted_time, 'process_id': current_process.process_id, 'color': current_process.color, 'queue': current_process.currentQueue})
            self.gantt_panel.update_gantt_chart(gantt_data)


    def update_statistics(self):
            self.statistics_panel = StatisticsPanel(self.panel, self.current_scheduler)
            self.main_box.Add(self.statistics_panel, 0, wx.EXPAND | wx.ALL, border=5)
            self.panel.Layout()

        
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
