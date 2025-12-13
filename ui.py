import tkinter as tk
from tkinter import ttk, messagebox
from manager import Manager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Management System")
        self.root.geometry("850x550")
        
        self.manager = Manager()

        # design
        self.bg = "#f4f4f9"
        self.root.configure(bg=self.bg)
        
        # spilt screen
        self.left = tk.Frame(root, bg=self.bg, padx=20, pady=20)
        self.left.pack(side="left", fill="y")
        
        self.right = tk.Frame(root, bg=self.bg, padx=20, pady=20)
        self.right.pack(side="right", fill="both", expand=True)

        self.create_widgets()
        self.update_log()

    def create_widgets(self):
        # 1. Add Bus
        p1 = self.panel(" Add New Bus ")
        tk.Label(p1, text="ID:").pack(anchor="w")
        self.e_id = ttk.Entry(p1); self.e_id.pack(fill="x")
        tk.Label(p1, text="Capacity:").pack(anchor="w")
        self.e_cap = ttk.Entry(p1); self.e_cap.pack(fill="x")
        ttk.Button(p1, text="Add", command=self.add_bus).pack(fill="x", pady=5)

        # 2. queue
        p2 = self.panel(" Queue ")
        tk.Label(p2, text="Name:").pack(anchor="w")
        self.e_name = ttk.Entry(p2); self.e_name.pack(fill="x")
        ttk.Button(p2, text="Join", command=self.join_q).pack(fill="x", pady=5)

        # 3. Actions
        p3 = self.panel(" Actions ")
        ttk.Button(p3, text="Board Passengers", command=self.board).pack(fill="x")

        # 4. screen
        tk.Label(self.right, text="Dashboard", font=("Arial", 14), bg=self.bg).pack(anchor="w")
        self.log_box = tk.Text(self.right, height=20); self.log_box.pack(fill="both", expand=True)

    def panel(self, title):
        # Frame Builder
        f = ttk.LabelFrame(self.left, text=title, padding=10)
        f.pack(fill="x", pady=10)
        return f

    # logic
    def add_bus(self):
        try:
            self.manager.add_bus(self.e_id.get(), int(self.e_cap.get()))
            self.msg("Success", "Bus Added")
            self.update_log()
        except: messagebox.showerror("Error", "Check Inputs")

    def join_q(self):
        if self.manager.add_passenger_to_queue(self.e_name.get()):
            self.msg("Success", "Joined Queue")
            self.update_log()
        else: messagebox.showerror("Error", "Queue Full")

    def board(self):
        logs = self.manager.board_passenger()
        messagebox.showinfo("Info", "\n".join(logs) if logs else "No action")
        self.update_log()

    def update_log(self):
        self.log_box.delete(1.0, 'end')
        q = self.manager.get_queue_status()
        self.log_box.insert('end', f"Queue: {q['size']}\n{q['items']}\n\n")
        
        buses = self.manager.get_buses_status()
        self.log_box.insert('end', f"Buses: {len(buses)}\n")
        for b in buses:
            self.log_box.insert('end', f"Bus {b['Bus ID']} (Free: {b['Remaining Seats']})\n")

    def msg(self, title, txt):
        messagebox.showinfo(title, txt)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
