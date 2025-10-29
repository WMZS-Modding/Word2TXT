#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
import sys
from pathlib import Path

class DocumentProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word2TXT")
        self.root.geometry("1000x700")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_menu_bar()

        self.create_left_panel()
        self.create_right_panel()
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Bug reports/Feature Requests", 
                          command=lambda: self.open_url("https://github.com/WMZS-Modding/Word2TXT/issues"))
        about_menu.add_command(label="Pull Requests", 
                          command=lambda: self.open_url("https://github.com/WMZS-Modding/Word2TXT/pulls"))
        about_menu.add_command(label="Discord", 
                          command=lambda: self.open_url("https://discord.gg/5BWTwGf8Rt"))
        about_menu.add_command(label="YouTube", 
                          command=lambda: self.open_url("https://youtube.com/@SuperHero20102"))
        about_menu.add_separator()
        about_menu.add_command(label="Check for update",
                          command=lambda: self.open_url("https://github.com/WMZS-Modding/Word2TXT/releases"))
        about_menu.add_command(label="About", command=self.show_about)

    def open_url(self, url):
        """Open a URL in the default web browser"""
        import webbrowser
        try:
            webbrowser.open(url)
            self.log_to_console(f"Opened: {url}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")
    
    def create_left_panel(self):
        left_frame = ttk.LabelFrame(self.main_frame, text="Tools")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        notebook = ttk.Notebook(left_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_word2png_tab(notebook)

        self.create_jpeg2png_tab(notebook)

        self.create_ocr_tab(notebook)
    
    def create_word2png_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Word2PNG")

        title_label = ttk.Label(tab, text="Convert Word images to images", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)

        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input your DOCX:").pack(side=tk.LEFT)
        self.docx_input = ttk.Entry(input_frame)
        self.docx_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(input_frame, text="Browse", command=self.browse_docx).pack(side=tk.RIGHT, padx=(5, 0))

        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output folder:").pack(side=tk.LEFT)
        self.docx_output = ttk.Entry(output_frame)
        self.docx_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(output_frame, text="Browse", command=self.browse_docx_output).pack(side=tk.RIGHT, padx=(5, 0))

        ttk.Button(tab, text="Convert DOCX to Images", command=self.run_word2png).pack(pady=10)
    
    def create_jpeg2png_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="JPEG2PNG")

        title_label = ttk.Label(tab, text="JPEG to PNG or PNG to JPEG (optional)", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)

        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input your result folder:").pack(side=tk.LEFT)
        self.jpeg_input = ttk.Entry(input_frame)
        self.jpeg_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(input_frame, text="Browse", command=self.browse_jpeg_input).pack(side=tk.RIGHT, padx=(5, 0))

        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output your new result folder:").pack(side=tk.LEFT)
        self.jpeg_output = ttk.Entry(output_frame)
        self.jpeg_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(output_frame, text="Browse", command=self.browse_jpeg_output).pack(side=tk.RIGHT, padx=(5, 0))

        conv_frame = ttk.Frame(tab)
        conv_frame.pack(fill=tk.X, pady=5)
        ttk.Label(conv_frame, text="Conversion:").pack(side=tk.LEFT)
        self.conv_type = tk.StringVar(value="jpeg2png")
        ttk.Radiobutton(conv_frame, text="JPEG to PNG", variable=self.conv_type, value="jpeg2png").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(conv_frame, text="PNG to JPEG", variable=self.conv_type, value="png2jpeg").pack(side=tk.LEFT, padx=10)

        ttk.Button(tab, text="Convert Images", command=self.run_jpeg2png).pack(pady=10)
    
    def create_ocr_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="OCR Images")

        title_label = ttk.Label(tab, text="Convert images to TXT files", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)

        mode_frame = ttk.Frame(tab)
        mode_frame.pack(fill=tk.X, pady=5)
        ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
        self.ocr_mode = tk.StringVar(value="fast")
    
        def on_mode_change():
            if self.ocr_mode.get() == "slow":
                cpu_combo.config(state="disabled")
                cpu_label.config(state="disabled")
            else:
                cpu_combo.config(state="readonly")
                cpu_label.config(state="normal")
    
        ttk.Radiobutton(mode_frame, text="Fast", variable=self.ocr_mode, 
                      value="fast", command=on_mode_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Slow", variable=self.ocr_mode, 
                      value="slow", command=on_mode_change).pack(side=tk.LEFT, padx=10)

        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input your result folder:").pack(side=tk.LEFT)
        self.ocr_input = ttk.Entry(input_frame)
        self.ocr_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(input_frame, text="Browse", command=self.browse_ocr_input).pack(side=tk.RIGHT, padx=(5, 0))

        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output your TXT folder:").pack(side=tk.LEFT)
        self.ocr_output = ttk.Entry(output_frame)
        self.ocr_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        ttk.Button(output_frame, text="Browse", command=self.browse_ocr_output).pack(side=tk.RIGHT, padx=(5, 0))

        cpu_frame = ttk.Frame(tab)
        cpu_frame.pack(fill=tk.X, pady=5)
        cpu_label = ttk.Label(cpu_frame, text="CPU (recommend for fast export):")
        cpu_label.pack(side=tk.LEFT)
        self.cpu_count = tk.StringVar(value="4")
        cpu_combo = ttk.Combobox(cpu_frame, textvariable=self.cpu_count, 
                              values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"],
                              state="readonly", width=5)
        cpu_combo.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Button(tab, text="Run OCR", command=self.run_ocr).pack(pady=10)

        self.cpu_combo = cpu_combo
        self.cpu_label = cpu_label
    
    def create_right_panel(self):
        right_frame = ttk.LabelFrame(self.main_frame, text="Console Output")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.console_text = scrolledtext.ScrolledText(right_frame, height=30, width=60, font=('Consolas', 10))
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console_text.config(state=tk.DISABLED)

        ttk.Button(right_frame, text="Clear Console", command=self.clear_console).pack(pady=5)
    
    def browse_docx(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])
        if filename:
            self.docx_input.delete(0, tk.END)
            self.docx_input.insert(0, filename)
    
    def browse_docx_output(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.docx_output.delete(0, tk.END)
            self.docx_output.insert(0, folder)
    
    def browse_jpeg_input(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.jpeg_input.delete(0, tk.END)
            self.jpeg_input.insert(0, folder)
    
    def browse_jpeg_output(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.jpeg_output.delete(0, tk.END)
            self.jpeg_output.insert(0, folder)
    
    def browse_ocr_input(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.ocr_input.delete(0, tk.END)
            self.ocr_input.insert(0, folder)
    
    def browse_ocr_output(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory()
        if folder:
            self.ocr_output.delete(0, tk.END)
            self.ocr_output.insert(0, folder)
    
    def run_word2png(self):
        docx_file = self.docx_input.get()
        output_folder = self.docx_output.get()
        
        if not docx_file or not output_folder:
            messagebox.showerror("Error", "Please provide both input DOCX and output folder")
            return
        
        if not os.path.exists(docx_file):
            messagebox.showerror("Error", f"DOCX file not found: {docx_file}")
            return
        
        self.log_to_console(f"Running Word2PNG on: {docx_file}")
        self.log_to_console(f"Output folder: {output_folder}")
        
        try:
            cmd = [sys.executable, "Word2PNG-Method-2.py", "-i", docx_file, "-o", output_folder]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.log_to_console(result.stdout)
            if result.stderr:
                self.log_to_console(f"ERROR: {result.stderr}")
            
            self.log_to_console("Word2PNG conversion completed!")
            
        except Exception as e:
            self.log_to_console(f"Error running Word2PNG: {e}")
    
    def run_jpeg2png(self):
        input_folder = self.jpeg_input.get()
        output_folder = self.jpeg_output.get()
        conv_type = self.conv_type.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please provide both input and output folders")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("Error", f"Input folder not found: {input_folder}")
            return
        
        self.log_to_console(f"Running JPEG2PNG conversion")
        self.log_to_console(f"Input folder: {input_folder}")
        self.log_to_console(f"Output folder: {output_folder}")
        self.log_to_console(f"Conversion type: {conv_type}")
        
        try:
            cmd = [sys.executable, "JPEG_to_PNG.py", "-i", input_folder, "-o", output_folder]
            if conv_type == "png2jpeg":
                cmd.extend(["--to", "jpeg"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.log_to_console(result.stdout)
            if result.stderr:
                self.log_to_console(f"ERROR: {result.stderr}")
            
            self.log_to_console("Image conversion completed!")
            
        except Exception as e:
            self.log_to_console(f"Error running JPEG2PNG: {e}")
    
    def run_ocr(self):
        input_folder = self.ocr_input.get()
        output_folder = self.ocr_output.get()
        mode = self.ocr_mode.get()
        cpu = self.cpu_count.get()
    
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please provide both input and output folders")
            return
    
        if not os.path.exists(input_folder):
            messagebox.showerror("Error", f"Input folder not found: {input_folder}")
            return
    
        self.log_to_console(f"Running OCR in {mode} mode")
        self.log_to_console(f"Input folder: {input_folder}")
        self.log_to_console(f"Output folder: {output_folder}")
        self.log_to_console(f"CPU cores: {cpu}")
    
        try:
            if mode == "fast":
                script_name = "OCR_Images.py"
                cmd = [sys.executable, script_name, "-i", input_folder, "-o", output_folder, "--workers", cpu]
            else:
                script_name = "OCR_Images_slow.py"
                cmd = [sys.executable, script_name, "-i", input_folder, "-o", output_folder]

            if not os.path.exists(script_name):
                self.log_to_console(f"ERROR: Script file not found: {script_name}")
                messagebox.showerror("Error", f"Script file not found: {script_name}")
                return
        
            self.log_to_console(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
        
            self.log_to_console(result.stdout)
            if result.stderr:
                self.log_to_console(f"ERROR: {result.stderr}")
        
            self.log_to_console("OCR processing completed!")
        
        except Exception as e:
            self.log_to_console(f"Error running OCR: {e}")
            messagebox.showerror("Error", f"Failed to run OCR: {e}")

    def log_to_console(self, message):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_console(self):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)

    def show_bug_reports(self):
        messagebox.showinfo("Bug Reports/Feature Requests", "Please report bugs and feature requests on our GitHub repository.")
    
    def show_pull_requests(self):
        messagebox.showinfo("Pull Requests", "We welcome pull requests! Please contribute to our GitHub repository.")
    
    def show_discord(self):
        messagebox.showinfo("Discord", "Join our Discord community for discussions and support.")
    
    def show_youtube(self):
        messagebox.showinfo("YouTube", "Check our YouTube channel for tutorials and demonstrations.")
    
    def show_about(self):
        messagebox.showinfo("About", "Word2TXT v0.1\n\nA tool designed to convert DOCX files to TXT.\n\nCredits:\nSuperHero2010: Owner and Author of Word2TXT")

def main():
    root = tk.Tk()
    app = DocumentProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()