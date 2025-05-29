import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import random
import platform
import socket

#------------------------------------------------------
# Δημιουργία του GUI για τον έλεγχο του Kali Linux
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.selected_interface = "wlan0"  # Προεπιλεγμένο interface
        self.interface_mode = "managed"    # Προεπιλεγμένο mode
        self.create_widgets()
        self.update_firewall_status()
        self.update_interface_mode()

    #------------------------------------------------------
    # Δημιουργία των γραφικών στοιχείων του GUI
    def create_widgets(self):
        # Προσπάθεια φόρτωσης εικόνας - αν δεν υπάρχει, συνέχισε χωρίς αυτή
        try:
            self.image = Image.open("kalilinux.png")
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(self, image=self.photo)
            self.label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Warning: kalilinux.png not found, continuing without background image")
            self.configure(bg="#2c3e50")

        # Ετικέτα με το λογότυπο Kali Linux
        self.kali_label = tk.Label(self, text="Kali Linux Control Panel", 
                                  font=("Arial", 24, "bold"), fg="#e74c3c", 
                                  bg=self.cget("bg") if hasattr(self, 'cget') else "#2c3e50")
        self.kali_label.place(x=200, y=10)

        # System Info Button
        self.system_info_button = tk.Button(self, text="System Info", 
                                          command=self.show_system_info, 
                                          bg="#3498db", fg="white", 
                                          font=("Arial", 10, "bold"))
        self.system_info_button.place(relx=1.0, rely=0.0, anchor="ne", relwidth=0.25)
        
        # Interface Selection
        self.interface_select_button = tk.Button(self, text=f"Interface: {self.selected_interface}", 
                                                command=self.select_interface,
                                                bg="#9b59b6", fg="white", font=("Arial", 10, "bold"))
        self.interface_select_button.place(relx=0.165, rely=0.80, relwidth=0.33, anchor=tk.S)

        # Monitor/Managed buttons
        self.monitor_btn = tk.Button(self, text="Monitor", 
                                   command=lambda: self.set_interface_mode('monitor'),
                                   bg="#e67e22", fg="white", font=("Arial", 10, "bold"))
        self.monitor_btn.place(relx=0.5, rely=0.80, relwidth=0.33, anchor=tk.S)

        self.managed_btn = tk.Button(self, text="Managed", 
                                   command=lambda: self.set_interface_mode('managed'),
                                   bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        self.managed_btn.place(relx=0.835, rely=0.80, relwidth=0.33, anchor=tk.S)

        # Interface Mode Status Button
        self.create_interface_mode_button()
        
        # System management buttons
        self.create_update_button()
        self.create_upgrade_button()
        self.create_fix_broken_button()
        self.create_reset_buttons()
        self.create_clean_button()

    #------------------------------------------------------
    def create_update_button(self):
        self.update_button = tk.Button(self, text="Update", command=self.update_system,
                                     bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.update_button.place(x=10, y=50, width=70, height=30)

    def update_system(self):
        try:
            messagebox.showinfo("Info", "Starting system update...")
            result = subprocess.run(["sudo", "apt", "update"], 
                                  capture_output=True, text=True, check=True)
            messagebox.showinfo("Success", "System updated successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    #------------------------------------------------------
    def create_upgrade_button(self):
        self.upgrade_button = tk.Button(self, text="Upgrade", command=self.upgrade_system,
                                      bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.upgrade_button.place(x=90, y=50, width=70, height=30)

    def upgrade_system(self):
        try:
            messagebox.showinfo("Info", "Starting system upgrade... This may take a while.")
            result = subprocess.run(["sudo", "apt", "full-upgrade", "-y"], 
                                  capture_output=True, text=True, check=True)
            messagebox.showinfo("Success", "System upgraded successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Upgrade failed: {e}")

    #------------------------------------------------------
    def create_fix_broken_button(self):
        self.fix_broken_button = tk.Button(self, text="Fix Broken", command=self.fix_broken,
                                         bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.fix_broken_button.place(x=170, y=50, width=80, height=30)

    def fix_broken(self):
        try:
            messagebox.showinfo("Info", "Fixing broken packages...")
            result = subprocess.run(["sudo", "apt", "--fix-broken", "install", "-y"], 
                                  capture_output=True, text=True, check=True)
            messagebox.showinfo("Success", "Broken packages fixed!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Fix failed: {e}")

    #------------------------------------------------------
    def create_clean_button(self):
        self.clean_system_button = tk.Button(self, text="Clean System", command=self.clean_system,
                                           bg="#16a085", fg="white", font=("Arial", 10, "bold"))
        self.clean_system_button.place(relx=0.00, rely=0.86, relwidth=0.33, anchor=tk.SW)

    def clean_system(self):
        try:
            messagebox.showinfo("Info", "Cleaning system...")
            subprocess.run(["sudo", "apt", "autoclean"], check=True)
            subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
            subprocess.run(["sudo", "apt", "clean"], check=True)
            # Πιο ασφαλής καθαρισμός temp files
            subprocess.run(["sudo", "find", "/var/tmp", "-type", "f", "-delete"], check=True)
            subprocess.run(["sudo", "find", "/tmp", "-type", "f", "-delete"], check=True)
            messagebox.showinfo("Success", "System cleaned successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Clean failed: {e}")

    #------------------------------------------------------
    # Δημιουργία κουμπιών επανεκκίνησης και ελέγχου του συστήματος
    def create_reset_buttons(self):
        # Network Interface Controls
        self.reset_wifi_button = tk.Button(self, text="Restart Interface", command=self.reset_wifi,
                                         bg="#d35400", fg="white", font=("Arial", 9, "bold"))
        self.reset_wifi_button.place(relx=0.00, rely=0.98, relwidth=0.33, anchor=tk.SW)

        self.restart_manager_button = tk.Button(self, text="Restart Manager", command=self.restart_manager,
                                              bg="#d35400", fg="white", font=("Arial", 9, "bold"))
        self.restart_manager_button.place(relx=0.33, rely=0.98, relwidth=0.33, anchor=tk.SW)

        self.reset_system_button = tk.Button(self, text="Reset System", command=self.reset_system,
                                           bg="#c0392b", fg="white", font=("Arial", 9, "bold"))
        self.reset_system_button.place(relx=0.66, rely=0.98, relwidth=0.33, anchor=tk.SW)

        # Firewall Controls
        self.restart_firewall_button = tk.Button(self, text="Restart Firewall", command=self.reset_firewall,
                                                bg="#8e44ad", fg="white", font=("Arial", 9, "bold"))
        self.restart_firewall_button.place(relx=0.00, rely=0.92, relwidth=0.33, anchor=tk.SW)

        self.firewall_toggle_button = tk.Button(self, text="Toggle Firewall", command=self.toggle_firewall,
                                              bg="#8e44ad", fg="white", font=("Arial", 9, "bold"))
        self.firewall_toggle_button.place(relx=0.33, rely=0.92, relwidth=0.33, anchor=tk.SW)

        self.firewall_status_button = tk.Button(self, text="Firewall: Unknown", bg="gray",
                                              font=("Arial", 9, "bold"))
        self.firewall_status_button.place(relx=0.66, rely=0.92, relwidth=0.33, anchor=tk.SW)
        
        # Network Configuration
        self.change_mac_button = tk.Button(self, text="Change MAC", command=self.show_mac_options,
                                         bg="#2980b9", fg="white", font=("Arial", 10, "bold"))
        self.change_mac_button.place(relx=0.33, rely=0.86, relwidth=0.33, anchor=tk.SW)

        self.change_ip_button = tk.Button(self, text="Change IP", command=self.show_ip_options,
                                        bg="#2980b9", fg="white", font=("Arial", 10, "bold"))
        self.change_ip_button.place(relx=0.66, rely=0.86, relwidth=0.33, anchor=tk.SW)

    #------------------------------------------------------
    # Επανεκκίνηση της ασύρματης διεπαφής
    def reset_wifi(self):
        try:
            messagebox.showinfo("Info", f"Restarting interface {self.selected_interface}...")
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "down"], check=True)
            subprocess.run(["sudo", "rfkill", "block", "wifi"], check=True)
            subprocess.run(["sudo", "rfkill", "unblock", "wifi"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "up"], check=True)
            messagebox.showinfo("Success", f"Interface {self.selected_interface} restarted successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to restart interface: {e}")

    #------------------------------------------------------
    def restart_manager(self):
        try:
            messagebox.showinfo("Info", "Restarting NetworkManager...")
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
            messagebox.showinfo("Success", "NetworkManager restarted successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to restart NetworkManager: {e}")

    #------------------------------------------------------
    def reset_firewall(self):
        try:
            if messagebox.askokcancel("Confirm", "This will reset all firewall rules. Continue?"):
                subprocess.run(["sudo", "ufw", "--force", "reset"], check=True)
                messagebox.showinfo("Success", "Firewall reset successfully!")
                self.update_firewall_status()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to reset firewall: {e}")

    def toggle_firewall(self):
        try:
            current_text = self.firewall_status_button.cget("text")
            if "Inactive" in current_text or "OFF" in current_text:
                subprocess.run(["sudo", "ufw", "enable"], check=True)
                messagebox.showinfo("Success", "Firewall enabled!")
            else:
                subprocess.run(["sudo", "ufw", "disable"], check=True)
                messagebox.showinfo("Success", "Firewall disabled!")
            self.update_firewall_status()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to toggle firewall: {e}")

    def update_firewall_status(self):
        try:
            result = subprocess.run(["sudo", "ufw", "status"], stdout=subprocess.PIPE, text=True, check=True)
            if "Status: active" in result.stdout:
                self.firewall_status_button.config(text="Firewall: Active", bg="#27ae60", fg="white")
            else:
                self.firewall_status_button.config(text="Firewall: Inactive", bg="#e74c3c", fg="white")
        except subprocess.CalledProcessError:
            self.firewall_status_button.config(text="Firewall: Error", bg="gray", fg="white")
        
        # Update every 5 seconds
        self.after(5000, self.update_firewall_status)

    #------------------------------------------------------
    def reset_system(self):
        if messagebox.askokcancel("Confirm Reboot", "This will reboot the system. Continue?"):
            try:
                subprocess.run(["sudo", "reboot"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to reboot: {e}")

    #------------------------------------------------------ 
    def show_mac_options(self):
        choice = messagebox.askquestion("Αλλαγή MAC", "Θες αυτόματη αλλαγή MAC; (Random)")
        if choice == 'yes':
            self.change_mac_random()
        else:
            custom_mac = simpledialog.askstring("Custom MAC", "Εισάγετε νέο MAC address (π.χ. 00:11:22:33:44:55):")
            if custom_mac:
                self.change_mac_manual(custom_mac)

    def change_mac_random(self):
        try:
            mac = "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "address", mac], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "up"], check=True)
            messagebox.showinfo("Success", f"New random MAC set: {mac}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to change MAC: {e}")

    def change_mac_manual(self, mac):
        try:
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "address", mac], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.selected_interface, "up"], check=True)
            messagebox.showinfo("Success", f"New MAC set: {mac}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to change MAC: {e}")

    #------------------------------------------------------
    def show_ip_options(self):
        choice = messagebox.askquestion("Αλλαγή IP", "Θες αυτόματη αλλαγή IP (μέσω DHCP);")
        if choice == 'yes':
            self.set_ip_dhcp()
        else:
            custom_ip = simpledialog.askstring("Custom IP", "Εισάγετε νέα IP (π.χ. 192.168.1.100):")
            if custom_ip:
                custom_netmask = simpledialog.askstring("Custom Netmask", "Εισάγετε subnet mask (π.χ. 255.255.255.0 ή 24):")
                custom_gateway = simpledialog.askstring("Gateway", "Εισάγετε gateway (π.χ. 192.168.1.1):")
                if custom_ip and custom_netmask and custom_gateway:
                    self.set_ip_manual(custom_ip, custom_netmask, custom_gateway)
                else:
                    messagebox.showerror("Σφάλμα", "Πρέπει να συμπληρώσετε και τις 3 τιμές.")

    def set_ip_dhcp(self):
        try:
            messagebox.showinfo("Info", "Renewing IP via DHCP...")
            subprocess.run(["sudo", "dhclient", "-r", self.selected_interface], check=True)
            subprocess.run(["sudo", "dhclient", self.selected_interface], check=True)
            messagebox.showinfo("Success", "IP renewed via DHCP!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"DHCP renewal failed: {e}")

    def set_ip_manual(self, ip, netmask, gateway):
        try:
            # Convert netmask if needed (e.g., 255.255.255.0 to /24)
            if "." in netmask:
                # Convert dotted decimal to CIDR
                cidr = sum([bin(int(x)).count('1') for x in netmask.split('.')])
            else:
                cidr = int(netmask)
            
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", self.selected_interface], check=True)
            subprocess.run(["sudo", "ip", "addr", "add", f"{ip}/{cidr}", "dev", self.selected_interface], check=True)
            subprocess.run(["sudo", "ip", "route", "add", "default", "via", gateway], check=True)
            messagebox.showinfo("Success", f"New IP set: {ip} with gateway {gateway}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set IP: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid netmask format: {e}")

    #------------------------------------------------------
    # Εμφάνιση πληροφοριών συστήματος
    def show_system_info(self):
        info_window = tk.Toplevel(self)
        info_window.title("System Information")
        info_window.geometry("650x500")
        info_window.configure(bg="#34495e")

        # Κύριο frame
        frame = tk.Frame(info_window, bg="#34495e")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Text box με σύνδεση στο scrollbar
        text = tk.Text(frame, wrap="word", font=("Courier", 10), 
                      yscrollcommand=scrollbar.set, bg="#2c3e50", 
                      fg="#ecf0f1", insertbackground="#ecf0f1")
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        # Συλλογή πληροφοριών
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            hostname = "Άγνωστο"
            local_ip = "Άγνωστο"

        try:
            public_ip = subprocess.check_output(["curl", "-s", "https://ipinfo.io/ip"], timeout=10).decode().strip()
        except:
            public_ip = "Άγνωστο"

        try:
            mac_output = subprocess.check_output(["cat", f"/sys/class/net/{self.selected_interface}/address"]).decode().strip()
        except:
            mac_output = "Άγνωστο"

        try:
            cpu_info = subprocess.check_output("lscpu", shell=True).decode().split('\n')
            ram_info = subprocess.check_output("free -h", shell=True).decode()
            disk_info = subprocess.check_output("df -h /", shell=True).decode()
            firewall_status = subprocess.check_output(["sudo", "ufw", "status"]).decode().strip()
        except:
            cpu_info = ["CPU Info not available"]
            ram_info = "RAM Info not available"
            disk_info = "Disk Info not available"
            firewall_status = "Firewall status not available"

        # Εμφάνιση πληροφοριών
        text.insert(tk.END, f"🖥️  Hostname: {hostname}\n")
        text.insert(tk.END, f"💻 OS: {platform.system()} {platform.release()}\n")
        text.insert(tk.END, f"🌐 Local IP: {local_ip}\n")
        text.insert(tk.END, f"🌍 Public IP: {public_ip}\n")
        text.insert(tk.END, f"🧭 MAC Address ({self.selected_interface}): {mac_output}\n")
        text.insert(tk.END, f"🔥 Firewall Status:\n{firewall_status}\n\n")

        text.insert(tk.END, "🧠 CPU Info:\n")
        for line in cpu_info[:10]:  # Limit output
            if line.strip():
                text.insert(tk.END, f"   {line}\n")

        text.insert(tk.END, "\n🧠 RAM Info:\n")
        text.insert(tk.END, f"{ram_info}\n")

        text.insert(tk.END, "💾 Disk Usage:\n")
        text.insert(tk.END, f"{disk_info}\n")

        # Make text read-only
        text.config(state='disabled')

    #----------------------------------------------------
    def create_interface_mode_button(self):
        self.interface_mode_button = tk.Button(
            self,
            text="Mode: Unknown",
            command=self.update_interface_mode,
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            relief="raised",
            bd=3,
            font=("Arial", 10, "bold")
        )
        self.interface_mode_button.place(relx=1.0, rely=0.1, anchor="ne", relwidth=0.25)
        
    def update_interface_mode(self):
        try:
            result = subprocess.run(["iw", self.selected_interface, "info"], capture_output=True, text=True, check=True)
            output = result.stdout.lower()
            if "type monitor" in output:
                mode = "Monitor"
                self.interface_mode = "monitor"
            else:
                mode = "Managed"
                self.interface_mode = "managed"
            self.interface_mode_button.config(text=f"Mode: {mode}")
            self.update_mode_buttons()
        except subprocess.CalledProcessError:
            self.interface_mode_button.config(text="Mode: Error")
        
        # Update every 5 seconds
        self.after(5000, self.update_interface_mode)

    #-------------------------------------------------------
    def select_interface(self):
        interfaces = self.get_interfaces()
        if not interfaces:
            messagebox.showerror("Error", "No interfaces found!")
            return

        # Create selection dialog
        interface_text = "Available interfaces:\n" + "\n".join([f"{i+1}. {iface}" for i, iface in enumerate(interfaces)])
        selected = simpledialog.askstring("Interface Selection", 
                                        f"{interface_text}\n\nEnter interface name:")

        if selected and selected in interfaces:
            self.selected_interface = selected
            self.interface_select_button.config(text=f"Interface: {selected}")
            self.monitor_btn.config(state='normal')
            self.managed_btn.config(state='normal')
            self.update_interface_mode()
            messagebox.showinfo("Success", f"Interface changed to: {selected}")
        elif selected:
            messagebox.showwarning("Warning", "Invalid interface selected.")

    def get_interfaces(self):
        try:
            output = subprocess.check_output(['ip', 'link', 'show'], text=True)
            interfaces = []
            for line in output.split('\n'):
                if ": " in line and not line.strip().startswith(' '):
                    iface = line.split(': ')[1].split('@')[0]
                    if iface != 'lo':  # Αποκλείουμε loopback
                        interfaces.append(iface)
            return interfaces
        except Exception as e:
            print(f"Error getting interfaces: {e}")
            return ["wlan0", "eth0"]  # Fallback interfaces

    def set_interface_mode(self, mode):
        if not self.selected_interface:
            messagebox.showwarning("Warning", "Please select an interface first.")
            return

        try:
            messagebox.showinfo("Info", f"Setting interface {self.selected_interface} to {mode} mode...")
            
            # Κατεβάζουμε την διεπαφή
            subprocess.run(['sudo', 'ip', 'link', 'set', self.selected_interface, 'down'], check=True)

            if mode == 'monitor':
                # Kill processes that might interfere
                subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], capture_output=True)
                # Set monitor mode
                subprocess.run(['sudo', 'iw', self.selected_interface, 'set', 'monitor', 'none'], check=True)
            elif mode == 'managed':
                # Set managed mode
                subprocess.run(['sudo', 'iw', self.selected_interface, 'set', 'type', 'managed'], check=True)

            # Ανέβασε την διεπαφή πάλι
            subprocess.run(['sudo', 'ip', 'link', 'set', self.selected_interface, 'up'], check=True)

            self.interface_mode = mode
            self.update_mode_buttons()
            self.update_interface_mode()
            
            messagebox.showinfo("Success", f"Interface {self.selected_interface} set to {mode} mode!")
            
            if mode == 'managed':
                # Restart NetworkManager for managed mode
                subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set interface mode: {e}")

    def update_mode_buttons(self):
        # Αλλαγή εμφάνισης κουμπιών ανάλογα με το ενεργό mode
        if self.interface_mode == 'monitor':
            self.monitor_btn.config(relief='sunken', bg='#c0392b', fg='white')
            self.managed_btn.config(relief='raised', bg='#27ae60', fg='white')
        elif self.interface_mode == 'managed':
            self.managed_btn.config(relief='sunken', bg='#c0392b', fg='white')
            self.monitor_btn.config(relief='raised', bg='#e67e22', fg='white')
        else:
            self.monitor_btn.config(relief='raised', bg='#e67e22', fg='white')
            self.managed_btn.config(relief='raised', bg='#27ae60', fg='white')

#------------------------------------------------------
# Εκκίνηση του GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Kali Linux Control Panel")
    root.configure(bg="#2c3e50")
    
    # Check if running as root
    if os.geteuid() != 0:
        messagebox.showwarning("Warning", "Some features require root privileges. Run with sudo for full functionality.")
    
    app = Application(master=root)
    app.mainloop()