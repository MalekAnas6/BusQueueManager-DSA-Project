import tkinter as tk
from tkinter import ttk, messagebox
from manager import Manager  # Importing backend 

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Management System")
        self.root.geometry("930x620")
        
        # Backend
        self.manager = Manager()

        # Design and Colors
        self.bg = "#f4f4f9"
        self.root.configure(bg=self.bg)
        
        # --Split Screen Layout--

        # Left : Controls
        self.left = tk.Frame(root, bg=self.bg, padx=20, pady=20)
        self.left.pack(side="left", fill="y")
        
        # Right : Dashboard/Log
        self.right = tk.Frame(root, bg=self.bg, padx=20, pady=20)
        self.right.pack(side="right", fill="both", expand=True)

        # Build UI
        self.create_widgets()
        self.update_log()

    def create_widgets(self):
        # --- Bus Section ---
        p1 = self.panel(" Add New Bus ")
        
        tk.Label(p1, text="Bus ID:").pack(anchor="w")
        self.e_id = ttk.Entry(p1)
        self.e_id.pack(fill="x", pady=(0, 5))
        
        tk.Label(p1, text="Capacity:").pack(anchor="w")
        self.e_cap = ttk.Entry(p1)
        self.e_cap.pack(fill="x", pady=(0, 5))
        
        ttk.Button(p1, text="Add Bus", command=self.add_bus).pack(fill="x", pady=10)

        # --- Queue Section ---
        p2 = self.panel(" Queue Management ")
        
        tk.Label(p2, text="Passenger Name:").pack(anchor="w")
        self.e_name = ttk.Entry(p2)
        self.e_name.pack(fill="x", pady=(0, 5))
        
        ttk.Button(p2, text="Join Queue", command=self.join_q).pack(fill="x", pady=10)

        # --- Actions & Operations ---
        p3 = self.panel(" Operations ")
        
        # Boarding Button
        ttk.Button(p3, text="Board Passengers", command=self.board).pack(fill="x", pady=5)
        
        # Separator line
        ttk.Separator(p3, orient='horizontal').pack(fill='x', pady=10)
        
        # Unload Button
        tk.Label(p3, text="Unload Passenger:").pack(anchor="w")
        self.e_unload = ttk.Entry(p3)
        self.e_unload.pack(fill="x", pady=(0, 5))
        
        ttk.Button(p3, text="Unload", command=self.unload_p).pack(fill="x", pady=5)

        # --- Dashboard Section ---
        tk.Label(self.right, text="System Dashboard", font=("Arial", 14, "bold"), bg=self.bg).pack(anchor="w", pady=(0, 10))
        
        # Create a Frame to Text Box
        log_frame = tk.Frame(self.right)
        log_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        # Text Box
        self.log_box = tk.Text(log_frame, height=20, font=("Consolas", 10), state='disabled', yscrollcommand=scrollbar.set)
        self.log_box.pack(side="left", fill="both", expand=True)

        # Scrollbar to Text Box
        scrollbar.config(command=self.log_box.yview)

    def panel(self, title):
        frame = ttk.LabelFrame(self.left, text=title, padding=15)
        frame.pack(fill="x", pady=10)
        return frame

    # --- Logic ---

    def add_bus(self):
        bid = self.e_id.get().strip()
        cap_str = self.e_cap.get().strip()

        # if empty
        if not bid or not cap_str:
            messagebox.showwarning("Warning", "Please fill in both Bus ID and Capacity.")
            return

        try:
            capacity = int(cap_str)
            
            # Check positive
            if capacity <= 0:
                raise ValueError 

            self.manager.add_bus(bid, capacity)
            self.msg("Success", f"Bus '{bid}' added with capacity {capacity}.")
            
            # Clear
            self.e_id.delete(0, 'end')
            self.e_cap.delete(0, 'end')
            self.update_log()
            
        except ValueError:
            # Handle number errors 
            messagebox.showerror("Input Error", "Capacity must be a positive integer number!")

    def join_q(self):
        # remove spaces
        name = self.e_name.get().strip()
        
        # Check if empty
        if not name:
            messagebox.showwarning("Warning", "Name cannot be empty!")
            return 
            
        # Logic
        if self.manager.add_passenger_to_queue(name):
            self.msg("Success", f"Passenger '{name}' joined the queue.")
            self.e_name.delete(0, 'end')
            self.update_log()
        else: 
            messagebox.showerror("Error", "Queue is full!")

    def board(self):
        logs = self.manager.board_passenger()
        if logs:
            self.msg("Boarding Complete", "\n".join(logs))
        else:
            self.msg("Info", "No passengers boarded (Queue empty or Buses full).")
        self.update_log()

    def unload_p(self):
        # Get name to unload
        name = self.e_unload.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name to unload.")
            return

        # logic
        logs = self.manager.unload_passenger(name)
        
        if logs:
            self.msg("Unload Complete", "\n".join(logs))
            self.e_unload.delete(0, 'end')
            self.update_log()
        else:
            messagebox.showwarning("Not Found", f"Passenger '{name}' was not found on any bus.")

    def update_log(self):
        # Unlock the text box 
        self.log_box.config(state='normal')
        
        # Clear
        self.log_box.delete(1.0, 'end')
        
        # Queue Status
        q = self.manager.get_queue_status()
        self.log_box.insert('end', f"=== WAITING QUEUE ({q['size']}) ===\n")
        if q['items']:
            self.log_box.insert('end', f"Passengers: {', '.join(q['items'])}\n")
        else:
            self.log_box.insert('end', "Queue is empty.\n")
        self.log_box.insert('end', "\n")
        
        # Buses Status
        buses = self.manager.get_buses_status()
        self.log_box.insert('end', f"=== BUS FLEET ({len(buses)}) ===\n")
        
        if not buses:
            self.log_box.insert('end', "No buses active.\n")

        for b in buses:
            status_line = f"Bus [{b['Bus ID']}] | Cap: {b['Capacity']} | Free: {b['Remaining Seats']}\n"
            self.log_box.insert('end', status_line)
            
            if b['Passengers']:
                self.log_box.insert('end', f"  > On Board: {', '.join(b['Passengers'])}\n")
            else:
                self.log_box.insert('end', "  > (Empty)\n")
            self.log_box.insert('end', "-"*40 + "\n")

        # Lock text box Read-Only
        self.log_box.config(state='disabled')

    def msg(self, title, txt):
        messagebox.showinfo(title, txt)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()