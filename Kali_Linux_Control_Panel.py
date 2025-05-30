import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import random
import platform
import socket
import tkinter as tk
from tkinter import ttk
import re
import subprocess
import webbrowser
import threading
import webbrowser
import time
#------------------------------------------------------
# Δημιουργία του GUI για τον έλεγχο του Kali Linux
class Application(tk.Frame):
#------------------------------------------------------
    # Αρχικοποίηση της εφαρμογής
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Kali Linux Control Panel")  
        self.master.geometry("1000x700")              
        self.pack(fill="both", expand=True)
        self.custom_colored_buttons = [] 
        self.selected_interface = "wlan0"
        self.interface_mode = "managed"
        self.dark_mode = False
        self.menu_visible = True  # 
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(side="left", fill="y")
        self.create_widgets()
        self.update_firewall_status()
        self.update_interface_mode()
        self.apply_theme()    
#------------------------------------------------------
    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.place_forget()
            self.menu_visible = False
        else:
            self.menu_frame.place(relx=1.0, x=-40, y=68, anchor="ne", width=100)
            self.menu_visible = True

    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Scan Wifi")
        width, height = 600, 400
        tk.Label(settings_window, text="Select Interface:").pack(anchor="nw", padx=10, pady=(10,0))
        self.interface_var = tk.StringVar(value="wlan0")

        # Θέση και μέγεθος κλπ
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        x = main_x + (main_width - width) // 2
        y = main_y + (main_height - height) // 2

        settings_window.geometry(f"{width}x{height}+{x}+{y}")
         # Ρύθμιση σκούρου φόντου
        settings_window.configure(bg="#222222")
    
        # Πάρε θέση & μέγεθος main window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        # Υπολόγισε θέση για να κεντραριστεί το παράθυρο scan πάνω στο main
        x = main_x + (main_width - width) // 2
        y = main_y + (main_height - height) // 2

        settings_window.geometry(f"{width}x{height}+{x}+{y}")

        # Λίστα interfaces (με την υπάρχουσα μέθοδο σου)
        interfaces = self.get_wireless_interfaces()

        # Δημιουργία combobox
        self.interface_var = tk.StringVar()
        interface_combo = ttk.Combobox(settings_window, textvariable=self.interface_var, values=interfaces, state="readonly")
        interface_combo.place(x=10, y=10)  # πάνω αριστερά, 10px padding

        # Προαιρετικά, ορίζουμε default επιλογή αν υπάρχουν interfaces
        if interfaces:
            interface_combo.current(0)
#------------------------------------------------------
        button_width = 16
        button_height = 2
        spacing = 10
        btn_pixel_height = button_height * 20
        bg_color = "#34495e"
        fg_color = "white"
        font_style = ("Arial", 9, "bold")
#-------------------------------------------------------
        airdum_btn = tk.Button(settings_window, text="Start Airdump Scan",
                            command=self.start_airdump_scan,
                            width=button_width, height=button_height,
                            bg=bg_color, fg=fg_color, font=font_style)
        airdum_btn.place(x=18, y=36)
#-------------------------------------------------------
        nmap_btn = tk.Button(settings_window, text="Start Nmap Scan",
                            command=self.start_nmap_scan,
                            width=button_width, height=button_height,
                            bg=bg_color, fg=fg_color, font=font_style)
        nmap_btn.place(x=18, y=36 + btn_pixel_height + spacing)
#-------------------------------------------------------
        arp_scan_btn = tk.Button(settings_window, text="ARP Scan       ",  # κενά για να ταιριάξει το μήκος
                                command=self.arp_scan,
                                width=button_width, height=button_height,
                                bg=bg_color, fg=fg_color, font=font_style)
        arp_scan_btn.place(x=18, y=36 + 2*(btn_pixel_height + spacing))
#-------------------------------------------------------
        masscan_btn = tk.Button(settings_window, text="Masscan Scan",
                        command=self.masscan_scan,
                        width=button_width, height=button_height,
                        bg=bg_color, fg=fg_color, font=font_style)
        masscan_btn.place(x=18, y=36 + 3*(btn_pixel_height + spacing))
#-------------------------------------------------------
        kismet_btn = tk.Button(settings_window, text="Kismet Scan", 
                       command=self.start_kismet,
                       width=button_width, height=button_height,
                       bg=bg_color, fg=fg_color, font=font_style)
        kismet_btn.place(x=18, y=36 + 4*(btn_pixel_height + spacing))  # κάτω από το Masscan

#------------------------------------------------------
        kill_btn = tk.Button(settings_window, text="Kill Processes", 
                     command=self.kill_wlan0_processes,
                     width=button_width, height=button_height,
                     bg="red", fg="white", font=font_style)
        kill_btn.place(x=18, y=36 + 5*(btn_pixel_height + spacing))  # κάτω από το Kismet
#-------------------------------------------------
    def get_wireless_interfaces(self):
        import subprocess
        try:
            result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            interfaces = []
            for line in lines:
                line = line.strip()
                if line.startswith("Interface"):
                    iface = line.split()[1]
                    interfaces.append(iface)
            return interfaces
        except Exception as e:
            print(f"Error getting wireless interfaces: {e}")
            return []

        def start_move(event):
            settings_window.x = event.x
            settings_window.y = event.y

        def do_move(event):
            x = event.x_root - settings_window.x
            y = event.y_root - settings_window.y
            settings_window.geometry(f"+{x}+{y}")

        settings_window.bind("<Button-1>", start_move)
        settings_window.bind("<B1-Motion>", do_move)

    def start_airdump_scan(self):
        import subprocess
        interface = getattr(self, "interface_var", None)
        if interface is None or not self.interface_var.get():
            print("interface")
            return
        iface = self.interface_var.get()
        try:
            subprocess.Popen(["xfce4-terminal", "--hold", "-e", f"sudo airodump-ng {iface}"])
        except Exception as e:
            print(f"Error starting airodump-ng: {e}")
#------------------------------------------------------
    def start_nmap_scan(self):
        scan_window = tk.Toplevel(self.master)
        scan_window.title("Nmap Scan Options")
        scan_window.geometry("400x250")

        tk.Label(scan_window, text="Target IP or Domain:").pack(pady=5)
        target_entry = tk.Entry(scan_window, width=40)
        target_entry.pack()

        scan_type = tk.StringVar(value="normal")  # default scan type

        tk.Radiobutton(scan_window, text="Normal Scan", variable=scan_type, value="normal").pack(anchor="w", padx=20)
        tk.Radiobutton(scan_window, text="Deep Scan", variable=scan_type, value="deep").pack(anchor="w", padx=20)
        tk.Radiobutton(scan_window, text="Vulnerability Scan", variable=scan_type, value="vuln").pack(anchor="w", padx=20)

        def run_scan(scan_type_value):
            target = target_entry.get().strip()
            if not target:
                messagebox.showwarning("Input Required", "Please enter an IP or domain.")
                return

            # Remove protocol prefix
            target = re.sub(r'^https?://', '', target)

            if scan_type_value == "normal":
                cmd = f"nmap {target}"
            elif scan_type_value == "deep":
                cmd = f"nmap -A -T4 {target}"
            elif scan_type_value == "vuln":
                cmd = f"nmap --script vuln {target}"
            else:
                return

            try:
                subprocess.Popen(["xfce4-terminal", "--hold", "-e", cmd])
            except FileNotFoundError:
                try:
                    subprocess.Popen(["xterm", "-hold", "-e", cmd])
                except FileNotFoundError:
                    messagebox.showerror("Error", "No compatible terminal found.")

            scan_window.destroy()  # σωστό όνομα παραθύρου!

        # ➕ Προσθήκη κουμπιού εκκίνησης
        tk.Button(scan_window, text="Run Scan Wifi", command=lambda: run_scan(scan_type.get())).pack(pady=15)
#------------------------------------------------------
    def arp_scan(self):
        try:
            # Ανοίγει terminal και τρέχει την εντολή arp-scan στο interface wlan0 π.χ.
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                "bash -c 'sudo arp-scan --interface=wlan0 --localnet; echo \"Press any key to exit...\"; read -n 1'"
            ])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")
           
#------------------------------------------------------
    def masscan_scan(self):
    # Δημιουργούμε ένα popup παράθυρο για να πάρουμε IP ή IP range
        def run_scan():
            ip_range = ip_entry.get().strip()
            if not ip_range:
                messagebox.showwarning("Warning", "Please enter an IP or IP range")
                return
            scan_window.destroy()

            # Τρέχουμε το masscan με το ip_range
            try:
                subprocess.Popen([
                    "x-terminal-emulator",
                    "-e",
                    f"bash -c 'sudo masscan -p1-65535 {ip_range} --rate=1000; echo Press any key to exit; read -n 1'"
                ])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start Masscan: {e}")

        scan_window = tk.Toplevel(self)
        scan_window.title("Masscan Scan")
        scan_window.geometry("300x100")
        scan_window.resizable(False, False)

        label = tk.Label(scan_window, text="Enter IP or IP range:")
        label.pack(pady=5)

        ip_entry = tk.Entry(scan_window, width=30)
        ip_entry.pack(pady=5)
        ip_entry.focus()

        btn_frame = tk.Frame(scan_window)
        btn_frame.pack(pady=5)

        ok_btn = tk.Button(btn_frame, text="Start Scan", command=run_scan)
        ok_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=scan_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
#--------------------------------------
    def start_kismet(self):
        def run_kismet():
            try:
                # Εκτελεί το kismet σε νέο terminal
                subprocess.Popen([
                    "x-terminal-emulator",
                    "-e",
                    "bash -c 'sudo kismet'"
                ])
                # Καθυστέρηση πριν το άνοιγμα του browser
                import time
                time.sleep(5)
                webbrowser.get('firefox').open("http://127.0.0.1:2501")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run Kismet or open browser: {e}")

        threading.Thread(target=run_kismet).start()
#---------------------------------------

    def kill_wlan0_processes(self):
        try:
            # Βρίσκει διεργασίες που χρησιμοποιούν wlan0
            cmd = "lsof -n | grep wlan0 | awk '{print $2}' | sort -u"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            pids = result.stdout.strip().split('\n')

            if not pids or pids == ['']:
                messagebox.showinfo("Καθαρισμός", "Δεν βρέθηκαν διεργασίες που χρησιμοποιούν το wlan0.")
                return

            # Kill κάθε PID που σχετίζεται με wlan0
            for pid in pids:
                subprocess.run(["sudo", "kill", "-9", pid])

            messagebox.showinfo("Επιτυχία", f"Τερματίστηκαν {len(pids)} διεργασίες που χρησιμοποιούσαν το wlan0.")

        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία καθαρισμού: {e}")
#------------------------------------------------------
    def create_settings_window(self, window):
        try:
            image = Image.open("kalilinux.png")  # Η εικόνα πρέπει να είναι στον ίδιο φάκελο
            image = image.resize((400, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            image_label = tk.Label(window, image=photo)
            image_label.image = photo  # Κρατάμε αναφορά ώστε να μην "σβήσει" η εικόνα
            image_label.pack(expand=True)
        except Exception as e:
            tk.Label(window, text=f"Σφάλμα: {e}", fg="red").pack(pady=20)
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def themed_toplevel(self, title=""):
        top = tk.Toplevel(self.master)
        top.title(title)
        self.apply_theme_to_window(top)
        return top

    def apply_theme(self):
        if self.dark_mode:
            bg_color = "#2c3e50"  # σκούρο μπλε φόντο
        else:
            bg_color = "white"    # λευκό φόντο

        # Αλλάζουμε background στα βασικά container
        self.master.configure(bg=bg_color)
        self.configure(bg=bg_color)
        self.menu_frame.configure(bg=bg_color)

        # Αλλάζουμε το φόντο των frame και label (χωρίς να πειράζουμε κουμπιά)
        def recursive_bg_configure(widget):
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.configure(bg=bg_color)
            # Προχωράμε στα παιδιά του widget
            for child in widget.winfo_children():
                recursive_bg_configure(child)

        recursive_bg_configure(self)

        # Αλλάζουμε μόνο το κείμενο του κουμπιού θέματος
        if self.dark_mode:
            self.theme_btn.configure(text="Light Mode")
        else:
            self.theme_btn.configure(text="Dark Mode")

        def apply_theme_to_window(self, window):
            if self.dark_mode:
                bg_color = "#2c3e50"
                fg_color = "white"
            else:
                bg_color = "white"
                fg_color = "black"

            window.configure(bg=bg_color)

    # Αναδρομικά αλλάζουμε και όλα τα παιδιά του παραθύρου
            def recursive_configure(widget):
                if isinstance(widget, tk.Button):
                    widget.configure(bg="#34495e" if self.dark_mode else "SystemButtonFace",
                                    fg=fg_color,
                                    activebackground="#34495e" if self.dark_mode else "SystemButtonFace",
                                    activeforeground=fg_color)
                elif isinstance(widget, (tk.Frame, tk.Label)):
                    widget.configure(bg=bg_color, fg=fg_color if isinstance(widget, tk.Label) else None)

                for child in widget.winfo_children():
                    recursive_configure(child)

            recursive_configure(window)
#------------------------------------------------------
    def show_mac_address(self):
        try:
            interface = self.selected_interface
            with open(f"/sys/class/net/{interface}/address", "r") as f:
                output = f.read().strip()
            from tkinter import messagebox
            messagebox.showinfo("MAC Διεύθυνση", f"{interface} → {output}")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Σφάλμα", f"Αδυναμία ανάγνωσης MAC: {e}")
#------------------------------------------------------
# Δημιουργία των γραφικών στοιχείων του GUI
# Προσπάθεια φόρτωσης εικόνας - αν δεν υπάρχει, συνέχισε χωρίς αυτή
    def create_widgets(self):
        try:
            self.image = Image.open("kalilinux.png")
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(self, image=self.photo)
            self.label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Warning: kalilinux.png not found, continuing without background image")
            self.configure(bg="#2c3e50")
#-------------------------------------------------------
# Ετικέτα με το λογότυπο Kali Linux
        self.kali_label = tk.Label(self, text="Kali Linux Control Panel", 
                                  font=("Arial", 18, "bold"), fg="#e74c3c", 
                                  bg=self.cget("bg") if hasattr(self, 'cget') else "#2c3e50")
        self.kali_label.place(x=10, y=10)
#-------------------------------------------------------
        # System Info Button
#relx=Αριστερό, rely=Κάτω, relwidth=Πλατός,anchor=Νότος
        self.system_info_button = tk.Button(self, text="System Info", 
                                          command=self.show_system_info, 
                                          bg="#3498db", fg="white", 
                                          font=("Arial", 10, "bold"))
        self.system_info_button.place(relx=1.0, rely=0.0,anchor="ne", relwidth=0.25)
#-------------------------------------------------------
        # Interface Selection
        self.interface_select_button = tk.Button(self, text=f"Interface: {self.selected_interface}", 
                                                command=self.select_interface,
                                                bg="#9b59b6", fg="white", font=("Arial", 10, "bold"))
        self.interface_select_button.place(relx=0.165, rely=0.80, relwidth=0.33, anchor=tk.S)
#-------------------------------------------------------        
        # Monitor/Managed buttons
        self.monitor_btn = tk.Button(self, text="Monitor", 
                                   command=lambda: self.set_interface_mode('monitor'),
                                   bg="#e67e22", fg="white", font=("Arial", 10, "bold"))
        self.monitor_btn.place(relx=0.495, rely=0.80, relwidth=0.329, anchor=tk.S)

        self.managed_btn = tk.Button(self, text="Managed", 
                                   command=lambda: self.set_interface_mode('managed'),
                                   bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        self.managed_btn.place(relx=0.825,rely=0.800, relwidth=0.33, anchor=tk.S)
#-------------------------------------------------------
        # Public IP Check Button        
        self.ip_check_button = tk.Button(
    self, text="Check Public IP", command=self.show_public_ip,
    bg="#3498db", fg="white", font=("Arial", 10, "bold")
)
        self.ip_check_button.place(x=50,y=90) 
#-------------------------------------------------------
        # MAC Address Check Button
        self.mac_check_button = tk.Button(
        self, text="Check MAC ", command=self.show_mac_address,
    bg="#2980b9", fg="white", font=("Arial", 10, "bold")
)
        self.mac_check_button.place(x=50, y=120, width=128, height=30) 
#-------------------------------------------------------
         # Interface Mode 2 Button
        self.menu_button = tk.Button(self, text="☰", font=("Arial", 14), command=self.toggle_menu)
        self.menu_button.place(relx=1.0, x=-2, y=70, anchor="ne", width=30, height=30)

        # Απόκρυφο μενού ρυθμίσεων (που εμφανίζεται κάτω από το κουμπί)
        self.menu_frame = tk.Frame(self, bg="lightgray", bd=1, relief="raised")
        self.menu_visible = False
#-------------------------------------------------------
        # Δημιουργία κουμπιών στο μενού
        self.settings_btn = tk.Button(self.menu_frame, text="Scan Wifi", command=self.show_settings,
                              bg="#007acc", fg="white", activebackground="#005f99", activeforeground="white")
        self.settings_btn.pack(fill="x")
#-------------------------------------------------------
        self.theme_btn = tk.Button(self.menu_frame, text="Dark Mode", command=self.toggle_theme,
                           bg="#FFD700",  # χρυσό-κίτρινο
                           fg="black",   # μαύρο κείμενο για αντίθεση
                           activebackground="#E6C200",  # σκούρο κίτρινο για ενεργό πάτημα
                           activeforeground="black")
        self.theme_btn.pack(fill="x")

        self.dark_mode = False  # Default is Light Mode
        self.apply_theme()

#-------------------------------------------------------
        # Interface Mode Status Button
        self.create_interface_mode_button()
#-------------------------------------------------------        
        # System management buttons
        self.create_update_button()
        self.create_upgrade_button()
        self.create_fix_broken_button()
        self.create_reset_buttons()
        self.create_clean_button()
#------------------------------------------------------
#update buttons για την ενημέρωση και αναβάθμιση του συστήματος
    def create_update_button(self):
        self.update_button = tk.Button(self, text="Update", command=self.update_system,
                                     bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.update_button.place(x=10, y=50, width=70, height=30)

    def update_system(self):
        try:
            subprocess.Popen(["x-terminal-emulator", "-e", "bash -c 'sudo apt update; echo \"Press any key to exit...\"; read -n 1'"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")
#------------------------------------------------------
    def create_upgrade_button(self):
        self.upgrade_button = tk.Button(self, text="Upgrade", command=self.upgrade_system,
                                      bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.upgrade_button.place(x=90, y=50, width=70, height=30)

    def upgrade_system(self):
        try:
            subprocess.Popen(["x-terminal-emulator", "-e", "bash -c 'sudo apt upgrade -y; echo \"Press any key to exit...\"; read -n 1'"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")

#------------------------------------------------------
    def fix_broken(self):
        try:
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                "bash -c 'sudo apt --fix-broken install -y; echo \"Press any key to exit...\"; read -n 1'"
            ])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")

    def create_fix_broken_button(self):
        self.fix_broken_button = tk.Button(self, text="Fix Broken", command=self.fix_broken,
                                        bg="#34495e", fg="white", font=("Arial", 9, "bold"))
        self.fix_broken_button.place(x=170, y=50,width=100, height=30)

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
#-------------------------------------------------------
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
#-------------------------------------------------------        
        # Network Configuration
        self.change_mac_button = tk.Button(self, text="Change MAC", command=self.show_mac_options,
                                         bg="#2980b9", fg="white", font=("Arial", 10, "bold"))
        self.change_mac_button.place(relx=0.33, rely=0.86, relwidth=0.33, anchor=tk.SW)
#-------------------------------------------------------

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
        self.interface_mode_button.place(x=-0, y=32, anchor="ne", relwidth=0.25, relx=1.0)

        
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
    def show_public_ip(self):
        try:
            import socket
            import requests

            # ===== ΠΑΡΕ ΤΟΠΙΚΗ IP =====
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            # ===== ΠΑΡΕ ΔΗΜΟΣΙΑ IPv4 =====
            public_ip = "Άγνωστη"
            services = [
                "https://api.ipify.org?format=text",
                "https://ipv4.icanhazip.com",
                "https://ifconfig.me/ip",
            ]
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    ip = response.text.strip()
                    if "." in ip:  # IPv4 έλεγχος
                        public_ip = ip
                        break
                except requests.RequestException:
                    continue

            # ===== ΕΜΦΑΝΙΣΕ ΤΟ ΑΠΟΤΕΛΕΣΜΑ =====
            messagebox.showinfo(
                "Διευθύνσεις IP",
                f"🔹 Δημόσια IPv4: {public_ip}\n🔸 Τοπική LAN IP: {local_ip}"
            )
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα:\n{e}")
#------------------------------------------------------
# Εκκίνηση του GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()   
#-------------------------------------------------------
# Check if running as root
    if os.geteuid() != 0:
        messagebox.showwarning("Warning", "Some features require root privileges. Run with sudo for full functionality.")
        app = Application(master=root)
        app.mainloop()
