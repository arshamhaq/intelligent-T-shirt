import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import socket			 
import sys
import time
import threading

flag = 0
Workers = {10 : 
            {
                'Heart_rate' : [],
                'Temp' : [],
                'Acceleration' : []
            }
          }


# ## --------------------------- First try-except block -- create socket
# try:
#     # next create a socket object 
#     s = socket.socket()		 
#     print ("Socket successfully created")

# except socket.error as e:
#         print("Error creating socket: %s" % e)
#         sys.exit(1)

        
# #----------------------------- Second try-except block -- connect to given host/port
# try:
#     # reserve a port on your computer in our 
#     port = 1000			
#     s.bind(('', port))		 
#     print ("socket binded to %s" %(port)) 

# except socket.gaierror as e:
#     print("Address-related error connecting to server: %s" % e)
#     sys.exit(1)

# except socket.error as e:
#     print("Connection error: %s" % e)
#     sys.exit(1)

# #----------------------------- put the socket into listening mode 
# s.listen(5)	 
# print ("socket is listening")



class WorkerPlotApp:
    def __init__(self, root, worker_name):
        self.root = root
        self.root.title(worker_name)

        self.fig1, self.ax1 = plt.subplots(figsize=(8, 2))
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 2))
        self.fig3, self.ax3 = plt.subplots(figsize=(8, 2))

        plt.style.use('dark_background')

        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=root)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=root)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.x_data = []
        self.y_data1 = []
        self.y_data2 = []
        self.y_data3 = []

        self.update_plot()

    def update_plot(self):
        global Workers
        data1 = Workers[10]['Heart_rate'][-1]
        data2 = Workers[10]['Temp'][-1]
        data3 = Workers[10]['Acceleration'][-1]

        x_data = time.time()

        self.x_data.append(x_data)
        self.y_data1.append(data1)
        self.y_data2.append(data2)
        self.y_data3.append(data3)

        if len(self.x_data) > 30:
            self.x_data = self.x_data[-30:]
            self.y_data1 = self.y_data1[-30:]
            self.y_data2 = self.y_data2[-30:]
            self.y_data3 = self.y_data3[-30:]

        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y_data1, color='orange', linewidth=2)
        self.ax1.set_title('Heat')

        self.ax2.clear()
        self.ax2.plot(self.x_data, self.y_data2, color='red', linewidth=2)
        self.ax2.set_title('Heart rate')

        self.ax3.clear()
        self.ax3.plot(self.x_data, self.y_data3, color='blue', linewidth=2)
        self.ax3.set_title('Acceleration')

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

        self.root.after(200, self.update_plot)

    
class WorkersMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workers Menu")
        self.root.geometry("800x600")  # Larger window size
        self.root.configure(bg='black')  # Set the background color to black

        self.buttons_frame = tk.Frame(root, bg='black')  # Set the background color to black
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)

        self.workers = ['Worker 1', 'Worker 2', 'Worker 3', 'Worker 4', 'Worker 5']

        self.worker_buttons = []
        for worker in self.workers:
            button = tk.Button(self.buttons_frame, text=worker,
                               bg='orange', fg='white',  # Orange button with white text
                               command=lambda w=worker: self.open_worker_window(w))
            button.pack(pady=10, fill=tk.BOTH, expand=True)
            self.worker_buttons.append(button)

    def open_worker_window(self, worker_name):
        self.root.withdraw()
        worker_window = tk.Toplevel(self.root)
        worker_app = WorkerPlotApp(worker_window, worker_name)
        back_button = tk.Button(worker_window, text="Back", bg='orange', fg='white',  # Orange button with white text
                                command=lambda: self.close_worker_window(worker_window), height=1, font=('Helvetica', 18))
        back_button.pack(fill=tk.BOTH, expand=True )

        danger_button = tk.Button(worker_window, text="Danger!", bg='red', fg='white',  # red button with white text
                                command=lambda: self.alarm(), height=2, width= 2,font=('Helvetica', 24))
        danger_button.pack(fill=tk.BOTH, expand=True)

    def close_worker_window(self, window):
        window.destroy()
        self.root.deiconify()
    
    def alarm(self):
        global flag
        flag = 1

def server(port = 2222):
    
    global Workers
    global flag
    # First try-except block -- create socket
    try:
        # next create a socket object 
        s = socket.socket()		 
        print ("Socket successfully created")

    except socket.error as e:
            print("Error creating socket: %s" % e)
            sys.exit(1)


    # Second try-except block -- connect to given host/port
    try:
        # reserve a port on your computer in our 			
        s.bind(('', port))		 
        print ("socket binded to %s" %(port)) 

    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)

    except socket.error as e:
        print("Connection error: %s" % e)
        sys.exit(1)



    # put the socket into listening mode 
    s.listen(5)	 
    print ("socket is listening")		 

    
    # a forever loop until we interrupt it or an error occurs 
    while True: 

        # Establish connection with client. 
        c, addr = s.accept()	
        print(c,addr)
        print("--------------") 
        print ('Got connection from', addr )


        while True: 
            # Fourth tr-except block -- waiting to receive data from remote host
            try:
                data = c.recv(1024)
                print('data' , len(data))
                data = data.decode()
            except socket.error as e:
                print("Error receiving data: %s" % e)
                sys.exit(1)
            if not len(data):
                break

            print(data.split('_'))
            _ , Herat_rate_temp, Temp_temp, Accelaration_temp, _ = data.split('_') 
            
            Workers[10]['Heart_rate'].append(float(Herat_rate_temp))
            Workers[10]['Temp'].append(float(Temp_temp))
            Workers[10]['Acceleration'].append(float(Accelaration_temp))
            
            # global flag
            if ( flag):
                danger_str = "DANGER!"
                c.send(danger_str.encode())
                flag = 0

            # Wokers = {10 : 
            # {
            #     'Heart_rate' : [],
            #     'Temp' : [],
            #     'Acceleration' : []
            # }
            # }

            #data.decode('utf-8')
            # data = data.replace(" ", "")
            # data = data.replace("\n", "")
            # first_dash = data.find('_')
            # dict_data["ID"] = float(data[:first_dash])
            # second_dash = data.find('_',first_dash+1)
            # dict_data["HeartRate"] = float(data[first_dash+1:second_dash])
            # dict_data["Temp"] = float(data[second_dash+1:])
            # print(dict_data)

        c.close()
        break

def GUI():
    root = tk.Tk()
    app = WorkersMenuApp(root)
    root.mainloop()

# def danger_sender(c):
#     global flag
#     danger_str = "DANGER!"
#     c.send(danger_str.encode())
#     flag = 0

if __name__ == "__main__":
    t1 = threading.Thread(target = server )
    t1.start()
    t2 = threading.Thread(target = GUI)
    t2.start()
