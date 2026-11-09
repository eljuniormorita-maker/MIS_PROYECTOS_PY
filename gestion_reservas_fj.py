import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
import logging
import re
from datetime import datetime

logging.basicConfig(
    filename='audit_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

class InvalidDataError(Exception): pass
class ServiceUnavailableError(Exception): pass
class InvalidReservationError(Exception): pass

class GeneralEntity(ABC):
    @abstractmethod
    def get_info(self): pass

class Client(GeneralEntity):
    def __init__(self, name, email):
        self.__name = None
        self.__email = None
        self.name = name
        self.email = email

    @property
    def name(self): return self.__name
    @name.setter
    def name(self, v):
        if not v or len(v.strip()) < 3: raise InvalidDataError("Name must have at least 3 characters")
        self.__name = v.strip()
    @property
    def email(self): return self.__email
    @email.setter
    def email(self, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v): raise InvalidDataError(f"Invalid email: {v}")
        self.__email = v
    def get_info(self): return f"Client: {self.__name} - {self.__email}"

class AbstractService(GeneralEntity):
    def __init__(self, name): self.name = name
    @abstractmethod
    def calculate_cost(self, duration): pass
    @abstractmethod
    def describe(self): pass
    @abstractmethod
    def validate_params(self, duration): pass
    def calculate_cost_with_tax(self, duration, tax=0.19, discount=0):
        return self.calculate_cost(duration) * (1+tax) * (1-discount)
    def get_info(self): return self.describe()

class RoomService(AbstractService):
    def __init__(self): super().__init__("Room Reservation")
    def validate_params(self, d):
        if d <=0: raise InvalidReservationError("Duration must be >0")
    def calculate_cost(self, d): return 50000 * d
    def describe(self): return "Room Reservation - Hall - $50k/day"
class RentalService(AbstractService):
    def __init__(self): super().__init__("Rental")
    def validate_params(self, d):
        if d>10: raise ServiceUnavailableError("Max 10 equipments")
        if d<=0: raise InvalidReservationError("Invalid quantity")
    def calculate_cost(self, d): return 30000 * d
    def describe(self): return "Equipment Rental - $30/each (Max. 10)"
class ConsultingService(AbstractService):
    def __init__(self): super().__init__("Consulting")
    def validate_params(self, d):
        if d<1: raise InvalidReservationError("Consulting min 1 hour")
    def calculate_cost(self, d): return 80000 * d 
    def describe(self): return "Consulting - Advisory - $80k/hour"

class Reservation:
    def __init__(self, client, service, duration):
        self.client=client; self.service=service; self.duration=duration; self.status="Pending"
        self.service.validate_params(duration)
    def confirm(self):
        try:
            self.status="Confirmed"
            return self.service.calculate_cost_with_tax(self.duration)
        except Exception as e:
            raise InvalidReservationError("Error confirming reservation") from e
    def cancel(self): 
        self.status="Cancelled"
    

class AbstractReservation(ABC):
    @abstractmethod
    def calculate_cost(self): pass
        
class StandardReservation(AbstractReservation):
    def __init__(self, service_type, duration):
        self.service_type = service_type
        self.duration = duration
        self.prices = {"Room Reservation": 50000, "Rental": 30000, "Consulting": 80000}

    def calculate_cost(self):
        return self.prices.get(self.service_type, 0) * self.duration

class MainWindow:
    def __init__(self, root):
        self.root = root 
        self.root.title("Software FJ - Integrated Management System")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")
        self.counter = 0
        self.clients = []
        self.reservations = []
        self.service_map = {
            "Room Reservation - Hall - $50k/day": RoomService(),
            "Equipment Rental - $30k/each (max. 10)": RentalService(),
            "Consulting - Advisory - $80k/hour": ConsultingService()
        }

        self.create_widgets()
        self.update_clock()

    def update_clock(self):
        date_str = datetime.now().strftime("%d/%m/%Y")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.lbl_clock.config(text=f"Date: {date_str}\nTime: {time_str}")
        self.root.after(1000, self.update_clock)
    
    def create_widgets(self):

        self.lbl_clock = tk.Label(self.root, text="", font=("Consolas", 9, "bold"), bg="#f0f0f0", fg="#2563eb", anchor="e", justify="right")
        self.lbl_clock.pack(fill="x", padx=15, pady=(5,0))

        tk.Label(self.root, text="Software FJ - Client, Service and Reservation Management",
                font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=10)

        frame_client = tk.LabelFrame(self.root, text=" Client Data ", padx=10, pady=10, bg="#f0f0f0")
        frame_client.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_client, text="Name:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=3)
        self.txt_name = tk.Entry(frame_client, width=35)
        self.txt_name.grid(row=0, column=1, pady=3)

        tk.Label(frame_client, text="Email:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=3)
        self.txt_email = tk.Entry(frame_client, width=35)
        self.txt_email.grid(row=1, column=1, pady=3)

        frame_service = tk.LabelFrame(self.root, text=" Service Details ", padx=10, pady=10, bg="#f0f0f0")
        frame_service.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_service, text="Service Type:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=3)
        self.combo_service = ttk.Combobox(frame_service, values=list(self.service_map.keys()), width=40, state="readonly")
        self.combo_service.grid(row=0, column=1, pady=3)

        tk.Label(frame_service, text="Duration / Quantity:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=3)
        self.txt_duration = tk.Entry(frame_service, width=12)
        self.txt_duration.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(frame_service, text="VAT 19% included - Tax will be added to total", font=("Arial", 8), fg="#64748b", bg="#f0f0f0").grid(row=2, column=1, sticky="w", pady=(2,0))
        tk.Button(self.root, text="Process and Confirm Reservation", bg="#2563eb", fg="white",
                  font=("Arial", 9, "bold"), padx=10, pady=5, command=self.process_reservation).pack(pady=15)

        tk.Label(self.root, text="Reservation History:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", padx=15)
        self.txt_history = tk.Text(self.root, height=12, width=120, bg="#ffffff")
        self.txt_history.pack(padx=15, pady=5)

    def process_reservation(self):
        try:
            name = self.txt_name.get().strip()
            email = self.txt_email.get().strip()
            duration_text = self.txt_duration.get().strip()
            service_type = self.combo_service.get()
            if not duration_text.isdigit(): raise InvalidDataError("Duration must be numeric")
            duration = int(duration_text)
            client_obj = Client(name, email)
        except InvalidDataError as e:
            messagebox.showerror("Validation Error", str(e))
            logging.warning(f"Validation failed: {e}")
        try:
            service_obj = self.service_map.get(service_type)
            if not service_obj: raise ServiceUnavailableError("Service not available")
            reservation_obj = Reservation(client_obj, service_obj, duration)
            total_cost = reservation_obj.confirm()
        except (ServiceUnavailableError, InvalidReservationError) as e:
            messagebox.showerror("Service Error", str(e))
            logging.error(f"Service error: {e}")
            return
        else:
            self.clients.append(client_obj)
            self.reservations.append(reservation_obj)
            self.counter += 1
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_entry = f"[{self.counter}] {now} | {client_obj.get_info()} | {service_obj.describe()} | Duration: {duration} | Total with tax: ${total_cost:.0f} | Status: {reservation_obj.status}\n"
            self.txt_history.insert(tk.END, log_entry)
            messagebox.showinfo("Success", f"Reservation confirmed!\nTotal with tax: ${total_cost:.0f}")
            logging.info(log_entry)
            self.txt_name.delete(0, tk.END)
            self.txt_email.delete(0, tk.END)
            self.txt_duration.delete(0, tk.END)

        finally:
            print(f"Reservation process finished. Total: {len(self.reservations)} - Check audit_fj.log")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()