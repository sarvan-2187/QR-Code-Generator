import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Set application icon
        try:
            self.root.iconbitmap("qricon.ico")
        except:
            pass
        
        self.qr_image = None
        self.tk_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="QR Code Generator", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Text input
        ttk.Label(input_frame, text="Enter text or URL:").pack(anchor="w", pady=5)
        self.text_input = tk.Text(input_frame, height=5, width=50, wrap=tk.WORD)
        self.text_input.pack(fill=tk.X, pady=5)
        
        # QR code options frame
        options_frame = ttk.LabelFrame(main_frame, text="QR Code Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Size options
        size_frame = ttk.Frame(options_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Size:").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.IntVar(value=10)
        size_scale = ttk.Scale(size_frame, from_=1, to=20, variable=self.size_var, 
                            orient=tk.HORIZONTAL, length=200)
        size_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        size_label = ttk.Label(size_frame, textvariable=self.size_var, width=3)
        size_label.pack(side=tk.LEFT, padx=5)
        
        # Color options
        color_frame = ttk.Frame(options_frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_frame, text="Fill Color:").pack(side=tk.LEFT, padx=5)
        self.fill_color = tk.StringVar(value="black")
        fill_combo = ttk.Combobox(color_frame, textvariable=self.fill_color, 
                                values=["black", "blue", "red", "green", "purple", "brown"])
        fill_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(color_frame, text="Background:").pack(side=tk.LEFT, padx=5)
        self.bg_color = tk.StringVar(value="white")
        bg_combo = ttk.Combobox(color_frame, textvariable=self.bg_color, 
                              values=["white", "lightgray", "yellow", "lightblue", "pink"])
        bg_combo.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        generate_btn = ttk.Button(btn_frame, text="Generate QR Code", command=self.generate_qr)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(btn_frame, text="Save QR Code", command=self.save_qr)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Result frame for displaying QR code
        self.result_frame = ttk.LabelFrame(main_frame, text="Generated QR Code", padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.qr_label = ttk.Label(self.result_frame)
        self.qr_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def generate_qr(self):
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text or URL!")
            return
        
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.size_var.get(),
                border=4
            )
            
            # Add data to the QR code
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create an image from the QR code
            self.qr_image = qr.make_image(fill_color=self.fill_color.get(), 
                                         back_color=self.bg_color.get())
            
            # Convert to PhotoImage for display
            self.tk_image = ImageTk.PhotoImage(self.qr_image)
            
            # Update the label with the new QR code
            self.qr_label.configure(image=self.tk_image)
            self.qr_label.image = self.tk_image
            
            self.status_var.set(f"QR Code generated for: {text[:30]}...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            self.status_var.set("Error generating QR code")
    
    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return
        
        try:
            # Ask for file name and location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save QR Code"
            )
            
            if file_path:
                self.qr_image.save(file_path)
                self.status_var.set(f"QR Code saved to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
            self.status_var.set("Error saving QR code")
    
    def clear_all(self):
        self.text_input.delete("1.0", tk.END)
        self.size_var.set(10)
        self.fill_color.set("black")
        self.bg_color.set("white")
        self.qr_label.configure(image="")
        self.qr_image = None
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()