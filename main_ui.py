import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from manager import Manager
from metro_manager import MetroManager

class BusQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Manager")
        self.root.geometry("1100x750")
        
        self.colors = {
            "bg": "#f0f2f5",
            "panel": "#ffffff",
            "primary": "#1a237e",
            "accent": "#3949ab",
            "secondary": "#5c6bc0",
            "danger": "#d32f2f",
            "success": "#388e3c",
            "border": "#e0e0e0",
            "text": "#212121",
            "text_light": "#757575"
        }
        
        self.root.configure(bg=self.colors["bg"])
        self.manager = Manager()
        self.metro_manager = MetroManager()
        self._setup_styles()
        self._create_layout()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["panel"])
        
        style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Inter", 10))
        style.configure("Header.TLabel", background=self.colors["bg"], foreground=self.colors["primary"], font=("Inter", 24, "bold"))
        style.configure("CardHeader.TLabel", background=self.colors["panel"], foreground=self.colors["primary"], font=("Inter", 14, "bold"))
        style.configure("Stat.TLabel", background=self.colors["panel"], foreground=self.colors["accent"], font=("Inter", 10, "bold"))

        style.configure("TButton", 
                        background=self.colors["accent"], 
                        foreground="white", 
                        font=("Inter", 10, "bold"),
                        borderwidth=0, 
                        focuscolor=self.colors["bg"])
        style.map("TButton", background=[("active", self.colors["primary"])])

        style.configure("Action.TButton", background=self.colors["success"])
        style.map("Action.TButton", background=[("active", "#2e7d32")])
        
        style.configure("Danger.TButton", background=self.colors["danger"])
        style.map("Danger.TButton", background=[("active", "#b71c1c")])

        style.configure("Treeview", 
                        background="white",
                        foreground=self.colors["text"], 
                        rowheight=30,
                        fieldbackground="white",
                        font=("Inter", 9))
        style.configure("Treeview.Heading", 
                        background="#eeeeee",
                        foreground=self.colors["primary"],
                        font=("Inter", 10, "bold"))
        style.map("Treeview", background=[("selected", self.colors["accent"])])

    def _create_layout(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=25, pady=25)

        header_frame = ttk.Frame(container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(header_frame, text="Logistics Dashboard", style="Header.TLabel").pack(side="left")
        ttk.Button(header_frame, text="Refresh Status", command=self.refresh_ui).pack(side="right")

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.tab_bus = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_bus, text=" Bus Fleet ")

        self.tab_metro = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_metro, text=" Metro Lines ")

        bus_content = ttk.Frame(self.tab_bus)
        bus_content.pack(fill="both", expand=True)

        bus_left = ttk.Frame(bus_content)
        bus_left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        bus_right = ttk.Frame(bus_content)
        bus_right.pack(side="right", fill="both", expand=True)

        self._create_card(bus_left, "Passenger Entry", self._build_passenger_form)
        self._create_card(bus_left, "Fleet Addition", self._build_bus_form)
        self.queue_card = self._create_card(bus_left, "Active Queue", self._build_queue_view, expand=True)

        self._create_card(bus_right, "Operational Status", self._build_fleet_view, expand=True)
        self._create_card(bus_right, "System Log", self._build_log_view, height=180)

        metro_content = ttk.Frame(self.tab_metro)
        metro_content.pack(fill="both", expand=True)

        metro_left = ttk.Frame(metro_content)
        metro_left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        metro_right = ttk.Frame(metro_content)
        metro_right.pack(side="right", fill="both", expand=True)

        self._create_card(metro_left, "Passenger Priority Entry", self._build_metro_passenger_form)
        self._create_card(metro_left, "Wagon Configuration", self._build_metro_wagon_form)
        self._create_card(metro_left, "Platform Status", self._build_metro_queue_view, expand=True)

        self._create_card(metro_right, "Train Monitoring", self._build_metro_train_view, expand=True)
        self._create_card(metro_right, "Control Center", self._build_metro_actions, height=120)

        self.refresh_ui()

    def _create_card(self, parent, title, build_func, expand=False, height=None):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        
        if expand:
            card.pack(fill="both", expand=True, pady=(0, 20))
        else:
            card.pack(fill="x", pady=(0, 20))
            if height:
               card.configure(height=height)

        ttk.Label(card, text=title, style="CardHeader.TLabel").pack(anchor="w", pady=(0, 15))
        
        content_area = ttk.Frame(card, style="Card.TFrame")
        content_area.pack(fill="both", expand=True)
        
        build_func(content_area)
        return card

    def _build_passenger_form(self, parent):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill="x")
        
        ttk.Label(f, text="Name").pack(side="left", padx=(0, 10))
        self.ent_passenger = ttk.Entry(f, font=("Inter", 10))
        self.ent_passenger.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.ent_passenger.bind("<Return>", lambda e: self.add_passenger())

        ttk.Button(f, text="Add", width=10, command=self.add_passenger).pack(side="right")

    def _build_bus_form(self, parent):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill="x")

        ttk.Label(f, text="ID").pack(side="left", padx=(0, 5))
        self.ent_bus_id = ttk.Entry(f, width=12, font=("Inter", 10))
        self.ent_bus_id.pack(side="left", padx=(0, 15))

        ttk.Label(f, text="Cap").pack(side="left", padx=(0, 5))
        self.ent_bus_cap = ttk.Spinbox(f, from_=1, to=100, width=5, font=("Inter", 10))
        self.ent_bus_cap.set(15)
        self.ent_bus_cap.pack(side="left", padx=(0, 15))
        
        ttk.Button(f, text="New Bus", width=12, command=self.add_new_bus).pack(side="right")

    def _build_metro_passenger_form(self, parent):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill="x")
        
        ttk.Label(f, text="Name").pack(side="left", padx=(0, 10))
        self.ent_metro_passenger = ttk.Entry(f)
        self.ent_metro_passenger.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        ttk.Label(f, text="Type").pack(side="left", padx=(0, 5))
        
        self.priority_map = {
            "Special Needs": 1,
            "Elderly": 2,
            "Pregnant": 3,
            "Standard": 10
        }
        self.combo_metro_priority = ttk.Combobox(f, values=list(self.priority_map.keys()), state="readonly", width=15)
        self.combo_metro_priority.set("Standard")
        self.combo_metro_priority.pack(side="left", padx=(0, 15))
        
        ttk.Button(f, text="Add", width=10, command=self.add_metro_passenger).pack(side="right")

    def _build_metro_wagon_form(self, parent):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill="x")

        ttk.Label(f, text="ID").pack(side="left", padx=(0, 5))
        self.ent_wagon_id = ttk.Entry(f, width=10)
        self.ent_wagon_id.pack(side="left", padx=(0, 15))

        ttk.Label(f, text="Cap").pack(side="left", padx=(0, 5))
        self.spn_wagon_cap = ttk.Spinbox(f, from_=1, to=100, width=5)
        self.spn_wagon_cap.set(10)
        self.spn_wagon_cap.pack(side="left", padx=(0, 15))

        ttk.Button(f, text="Add", width=8, command=self.add_metro_wagon).pack(side="left")
        ttk.Button(f, text="Remove Last", style="Danger.TButton", command=self.remove_last_wagon).pack(side="right")

    def _build_metro_queue_view(self, parent):
        self.metro_queue_list = tk.Listbox(parent, font=("Inter", 10), bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
        self.metro_queue_list.pack(fill="both", expand=True)

    def _build_metro_train_view(self, parent):
        cols = ("id", "cap", "pass")
        self.metro_wagon_tree = ttk.Treeview(parent, columns=cols, show="headings", selectmode="none")
        
        self.metro_wagon_tree.heading("id", text="Wagon ID")
        self.metro_wagon_tree.heading("cap", text="Capacity")
        self.metro_wagon_tree.heading("pass", text="Occupancy")
        
        self.metro_wagon_tree.column("id", width=100, anchor="center")
        self.metro_wagon_tree.column("cap", width=100, anchor="center")
        self.metro_wagon_tree.column("pass", width=100, anchor="center")
        
        self.metro_wagon_tree.pack(fill="both", expand=True)

    def _build_metro_actions(self, parent):
        btn = ttk.Button(parent, text="Process Next Boarding", style="Action.TButton", command=self.board_metro_passenger)
        btn.pack(fill="both", expand=True, pady=10)

    def _build_queue_view(self, parent):
        self.queue_list = tk.Listbox(parent, font=("Inter", 10), bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
        self.queue_list.pack(fill="both", expand=True)

    def _build_fleet_view(self, parent):
        cols = ("id", "cap", "onboard", "status")
        self.tree_buses = ttk.Treeview(parent, columns=cols, show="headings", selectmode="browse")
        
        self.tree_buses.heading("id", text="Bus ID")
        self.tree_buses.heading("cap", text="Capacity")
        self.tree_buses.heading("onboard", text="Onboard")
        self.tree_buses.heading("status", text="Status")

        self.tree_buses.column("id", width=100, anchor="center")
        self.tree_buses.column("cap", width=80, anchor="center")
        self.tree_buses.column("onboard", width=80, anchor="center")
        self.tree_buses.column("status", width=120, anchor="center")
        
        self.tree_buses.pack(fill="both", expand=True, pady=(0, 15))
        
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Board Queue", style="Action.TButton", command=self.board_passengers).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(btn_frame, text="Unload Select", command=self.unload_selected_bus).pack(side="right", fill="x", expand=True, padx=(5, 0))

    def _build_log_view(self, parent):
        self.log_area = scrolledtext.ScrolledText(parent, font=("Inter", 9), bg="#f8f9fa", state="disabled", relief="flat")
        self.log_area.pack(fill="both", expand=True)

    def add_passenger(self):
        name = self.ent_passenger.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Enter a name.")
            return

        if self.manager.add_passenger_to_queue(name):
            self.log_info(f"Queued: {name}")
            self.ent_passenger.delete(0, 'end')
            self.refresh_ui()
        else:
            messagebox.showerror("Limit Reached", "Queue is currently full.")

    def add_new_bus(self):
        bid = self.ent_bus_id.get().strip()
        cap_val = self.ent_bus_cap.get().strip()
        
        if not bid or not cap_val:
            messagebox.showwarning("Input Required", "ID and Capacity are mandatory.")
            return
        
        try:
            capacity = int(cap_val)
            if capacity <= 0: raise ValueError
        except ValueError:
             messagebox.showerror("Invalid Input", "Capacity must be a positive number.")
             return

        for b in self.manager.buses:
            if b.bus_ID == bid:
                messagebox.showerror("Conflict", "Bus ID already exists.")
                return

        self.manager.add_bus(bid, capacity)
        self.log_info(f"Fleet expanded: {bid}")
        self.ent_bus_id.delete(0, 'end')
        self.ent_bus_cap.set(15)
        self.refresh_ui()

    def add_metro_passenger(self):
        name = self.ent_metro_passenger.get().strip()
        selected_text = self.combo_metro_priority.get()
        prio = self.priority_map.get(selected_text, 10)
            
        if not name:
            messagebox.showwarning("Input Required", "Enter a name.")
            return
            
        self.metro_manager.add_passenger(name, prio)
        self.ent_metro_passenger.delete(0, 'end')
        self.refresh_ui()

    def add_metro_wagon(self):
        wid = self.ent_wagon_id.get().strip()
        try:
            cap = int(self.spn_wagon_cap.get())
            if cap < 1: raise ValueError
        except:
            messagebox.showerror("Invalid Input", "Capacity must be positive.")
            return
            
        if not wid:
             messagebox.showwarning("Input Required", "Enter Wagon ID.")
             return

        self.metro_manager.add_wagon(wid, cap)
        self.ent_wagon_id.delete(0, 'end')
        self.refresh_ui()

    def remove_last_wagon(self):
        if self.metro_manager.remove_last_wagon():
            self.refresh_ui()
        else:
            messagebox.showinfo("Status", "No wagons available.")

    def board_metro_passenger(self):
        if self.metro_manager.board_passenger():
            messagebox.showinfo("Success", "Boarding completed.")
        else:
            messagebox.showwarning("Failed", "No space available or queue is empty.")
        self.refresh_ui()

    def unload_selected_bus(self):
        selected = self.tree_buses.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Select a bus to unload.")
            return
        
        item = self.tree_buses.item(selected[0])
        bus_id = str(item['values'][0])
        
        if messagebox.askyesno("Confirm Action", f"Arrive and unload {bus_id}?"):
            log = self.manager.unload_bus_by_id(bus_id)
            self.log_info(log)
            self.refresh_ui()

    def board_passengers(self):
        logs = self.manager.board_passenger()
        if logs:
            for l in logs:
                self.log_info(l)
            messagebox.showinfo("Boarded", f"{len(logs)} boarded.")
        else:
            messagebox.showinfo("Status", "Cannot board: Queue empty or buses full.")
        self.refresh_ui()

    def log_info(self, msg):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"> {msg}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def refresh_ui(self):
        qdata = self.manager.get_queue_status()
        self.queue_list.delete(0, 'end')
        for p in qdata['items']:
            self.queue_list.insert('end', f" {p}")
        
        for i in self.tree_buses.get_children():
            self.tree_buses.delete(i)
            
        for b in self.manager.get_buses_status():
            rem = b['Remaining Seats']
            status = "FULL" if rem == 0 else f"{rem} Seats"
            self.tree_buses.insert("", "end", values=(b['Bus ID'], b['Capacity'], b['Current Passengers'], status))

        if hasattr(self, 'metro_queue_list') and self.metro_queue_list:
            self.metro_queue_list.delete(0, 'end')
            for p in self.metro_manager.get_queue_data():
                self.metro_queue_list.insert('end', f" {p}")

        if hasattr(self, 'metro_wagon_tree') and self.metro_wagon_tree:
            for item in self.metro_wagon_tree.get_children():
                self.metro_wagon_tree.delete(item)
            
            for w in self.metro_manager.get_metro_data():
                 self.metro_wagon_tree.insert("", "end", values=(w['id'], w['capacity'], w['passengers']))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BusQueueApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
