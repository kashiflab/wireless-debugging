import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import time

class WirelessDebugGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireless Debugging Tool")
        self.root.geometry("450x550")  # Increased height for platform tools path
        self.root.resizable(False, False)  # Allow resizing for better usability
        
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)

        # Platform Tools Path Frame
        self.platform_frame = ttk.LabelFrame(root, text="Platform Tools Path", padding=10)
        self.platform_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.platform_frame, text="ADB Platform Tools Path:").pack()
        self.platform_tools_path = ttk.Entry(self.platform_frame, width=40)
        
        # Load saved path from JSON if exists
        self.config_file = "config.json"
        saved_path = self.load_platform_path()
        if saved_path:
            self.platform_tools_path.insert(0, saved_path)
        else:
            self.platform_tools_path.insert(0, r"C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools")
        
        self.platform_tools_path.pack()
        
        # Add Save button
        self.save_button = ttk.Button(self.platform_frame, text="Save Path", command=self.save_platform_path)
        self.save_button.pack(pady=5)
        
        # Pairing Frame
        self.pair_frame = ttk.LabelFrame(root, text="Device Pairing", padding=10)
        self.pair_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.pair_frame, text="Pairing IP:Port (e.g. 192.168.1.100:37000)").pack()
        self.pair_ip = ttk.Entry(self.pair_frame, width=40)
        self.pair_ip.pack()
        
        ttk.Label(self.pair_frame, text="Pairing Code").pack()
        self.pair_code = ttk.Entry(self.pair_frame, width=40)
        self.pair_code.pack()
        
        self.pair_button = ttk.Button(self.pair_frame, text="Pair Device", command=self.pair_device)
        self.pair_button.pack(pady=10)
        
        # Connection Frame
        self.connect_frame = ttk.LabelFrame(root, text="Device Connection", padding=10)
        self.connect_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.connect_frame, text="Connection IP:Port (e.g. 192.168.1.100:5555)").pack()
        self.connect_ip = ttk.Entry(self.connect_frame, width=40)
        self.connect_ip.pack()
        
        self.connect_button = ttk.Button(self.connect_frame, text="Connect Device", 
                                       command=self.connect_device)
        self.connect_button.pack(pady=10)
        
        # Status Label
        self.status_label = ttk.Label(root, text="Ready", anchor="center")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def load_platform_path(self):
        try:
            import json
            import os
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('platform_tools_path')
        except Exception as e:
            print(f"Error loading config: {str(e)}")
        return None

    def save_platform_path(self):
        try:
            import json
            path = self.platform_tools_path.get().strip()
            if path:
                with open(self.config_file, 'w') as f:
                    json.dump({'platform_tools_path': path}, f)
                self.status_label.config(text="Path saved successfully!")
                messagebox.showinfo("Success", "Platform tools path saved successfully!")
            else:
                messagebox.showerror("Error", "Platform tools path cannot be empty")
        except Exception as e:
            self.status_label.config(text="Error saving path!")
            messagebox.showerror("Error", f"Error saving path: {str(e)}")

    def pair_device(self):
        ip = self.pair_ip.get().strip()
        code = self.pair_code.get().strip()
        platform_path = self.platform_tools_path.get().strip()
        
        if not ip or not code:
            messagebox.showerror("Error", "Please enter both IP and pairing code")
            return
            
        if not platform_path:
            messagebox.showerror("Error", "Platform tools path cannot be empty")
            return
            
        try:
            self.status_label.config(text="Pairing device...")
            self.root.update()
            
            pair_command = f"cd {platform_path} && adb pair {ip} {code}"
            result = subprocess.run(pair_command, shell=True, capture_output=True, text=True)
            
            if "Successfully paired" in result.stdout:
                self.status_label.config(text="Device paired successfully!")
                messagebox.showinfo("Success", "Device paired successfully!")
            else:
                self.status_label.config(text="Pairing failed!")
                messagebox.showerror("Error", f"Pairing failed: {result.stderr}")
                
        except Exception as e:
            self.status_label.config(text="Error occurred!")
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def connect_device(self):
        ip = self.connect_ip.get().strip()
        platform_path = self.platform_tools_path.get().strip()
        
        if not ip:
            messagebox.showerror("Error", "Please enter connection IP")
            return
            
        if not platform_path:
            messagebox.showerror("Error", "Platform tools path cannot be empty")
            return
            
        try:
            self.status_label.config(text="Connecting to device...")
            self.root.update()
            
            connect_command = f"cd {platform_path} && adb connect {ip}"
            result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
            
            if "connected" in result.stdout.lower():
                self.status_label.config(text="Connected to device successfully!")
                messagebox.showinfo("Success", "Connected to device successfully!")
            else:
                self.status_label.config(text="Connection failed!")
                messagebox.showerror("Error", f"Connection failed: {result.stderr}")
                
        except Exception as e:
            self.status_label.config(text="Error occurred!")
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = WirelessDebugGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

