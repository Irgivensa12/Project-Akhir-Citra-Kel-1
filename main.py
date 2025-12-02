import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from preprocessing.resize import resize_image
from preprocessing.normalisasi import normalize_image
from preprocessing.augmentasi import augment_image

DATASET_DIR = "Dayak's Animal"
OUTPUT_DIR = "hasil_olah_dataset"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#F0F2F5")

        self.images = {
            'original': None,
            'resized': None,
            'normalized': None,
            'augmented': None
        }
        
        self.tk_images = {}
        self.preprocess_steps = 0

        # ================================
        # HEADER
        # ================================
        header = tk.Frame(root, bg="#FFFFFF", height=80)
        header.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(header, text="Image Processing System",
                        bg="#FFFFFF", fg="#1A1A1A",
                        font=("Segoe UI", 24, "bold"))
        title.pack(pady=20)

        # ================================
        # MAIN CONTAINER
        # ================================
        main_container = tk.Frame(root, bg="#F0F2F5")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # LEFT PANEL - Upload & Controls
        left_panel = tk.Frame(main_container, bg="#FFFFFF", width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)

        # Upload Section
        upload_label = tk.Label(left_panel, text="Upload Image",
                               bg="#FFFFFF", fg="#1A1A1A",
                               font=("Segoe UI", 14, "bold"))
        upload_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.upload_box = tk.Frame(left_panel, bg="#F8F9FA", 
                                   bd=2, relief="solid", cursor="hand2")
        self.upload_box.pack(pady=10, padx=20, fill="x")
        self.upload_box.bind("<Button-1>", lambda e: self.upload_image())

        upload_icon = tk.Label(self.upload_box, text="📁",
                              bg="#F8F9FA", font=("Segoe UI", 32))
        upload_icon.pack(pady=(20, 5))

        self.upload_text = tk.Label(self.upload_box, 
                                    text="Click to Upload Image\n(JPG, JPEG, PNG)",
                                    bg="#F8F9FA", fg="#6C757D",
                                    font=("Segoe UI", 10))
        self.upload_text.pack(pady=(0, 20))

        # Separator
        separator = ttk.Separator(left_panel, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=20)

        # Preprocessing Section
        preprocess_label = tk.Label(left_panel, text="Preprocessing Steps",
                                    bg="#FFFFFF", fg="#1A1A1A",
                                    font=("Segoe UI", 14, "bold"))
        preprocess_label.pack(pady=(0, 15), padx=20, anchor="w")

        # Buttons
        self.btn_resize = self.make_button(left_panel, "1. Resize to 299×299", 
                                          self.do_resize, "🔲")
        self.btn_norm = self.make_button(left_panel, "2. Normalize Image", 
                                         self.do_normalize, "✨")
        self.btn_aug = self.make_button(left_panel, "3. Augment Image", 
                                        self.do_augment, "🔄")

        # Separator
        separator2 = ttk.Separator(left_panel, orient="horizontal")
        separator2.pack(fill="x", padx=20, pady=20)

        # Process Dataset Button
        self.btn_process_dataset = tk.Button(
            left_panel,
            text="⚡ Process Entire Dataset",
            command=self.process_dataset,
            bg="#28A745", fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat", height=2,
            bd=0, activebackground="#218838",
            cursor="hand2", state="disabled"
        )
        self.btn_process_dataset.pack(pady=10, padx=20, fill="x")

        # Status Label
        self.status_label = tk.Label(left_panel, 
                                     text="Upload an image to start",
                                     bg="#FFFFFF", fg="#6C757D",
                                     font=("Segoe UI", 9, "italic"))
        self.status_label.pack(pady=(10, 20), padx=20)

        # ================================
        # RIGHT PANEL - Image Display Grid
        # ================================
        right_panel = tk.Frame(main_container, bg="#F0F2F5")
        right_panel.pack(side="right", fill="both", expand=True)

        # Grid for images (2x2)
        self.grid_frames = {}
        positions = [
            ('original', 'Original Image', 0, 0),
            ('resized', 'Resized (299×299)', 0, 1),
            ('normalized', 'Normalized', 1, 0),
            ('augmented', 'Augmented', 1, 1)
        ]

        for key, label_text, row, col in positions:
            frame = self.create_image_card(right_panel, label_text)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.grid_frames[key] = frame

        # Configure grid weights
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_columnconfigure(1, weight=1)

    def create_image_card(self, parent, title):
        """Create a card for displaying an image"""
        card = tk.Frame(parent, bg="#FFFFFF", relief="solid", bd=1)
        
        # Title
        title_label = tk.Label(card, text=title,
                              bg="#FFFFFF", fg="#1A1A1A",
                              font=("Segoe UI", 11, "bold"))
        title_label.pack(pady=(10, 5))

        # Image container
        img_container = tk.Frame(card, bg="#F8F9FA", width=400, height=280)
        img_container.pack(pady=10, padx=10, fill="both", expand=True)
        img_container.pack_propagate(False)

        # Placeholder
        placeholder = tk.Label(img_container, 
                              text="No image",
                              bg="#F8F9FA", fg="#CED4DA",
                              font=("Segoe UI", 10))
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # Store references
        card.img_label = tk.Label(img_container, bg="#F8F9FA")
        card.placeholder = placeholder
        
        # Download button (initially hidden)
        card.download_btn = tk.Button(card, text="💾 Download",
                                     bg="#17A2B8", fg="white",
                                     font=("Segoe UI", 9, "bold"),
                                     relief="flat", height=1,
                                     bd=0, activebackground="#138496",
                                     cursor="hand2", state="disabled")
        card.download_btn.pack(pady=(5, 10), padx=10)

        return card

    def make_button(self, parent, text, command, icon):
        """Create a styled button"""
        btn = tk.Button(parent, text=f"{icon}  {text}", 
                       command=command,
                       bg="#007BFF", fg="white",
                       font=("Segoe UI", 10, "bold"),
                       relief="flat", height=2,
                       bd=0, activebackground="#0056B3",
                       cursor="hand2", state="disabled")
        btn.pack(pady=5, padx=20, fill="x")
        return btn

    def upload_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if not path:
            return

        self.images['original'] = Image.open(path)
        
        # Reset other images
        self.images['resized'] = None
        self.images['normalized'] = None
        self.images['augmented'] = None

        # Display original image
        self.display_image('original')
        
        # Clear other displays
        for key in ['resized', 'normalized', 'augmented']:
            self.clear_display(key)

        # Enable buttons
        self.btn_resize.config(state="normal")
        self.btn_norm.config(state="disabled")
        self.btn_aug.config(state="disabled")

        # Reset state
        self.preprocess_steps = 0
        self.btn_process_dataset.config(state="disabled")
        self.status_label.config(text="✓ Image uploaded successfully")

    def display_image(self, key):
        """Display image in the corresponding grid position"""
        if self.images[key] is None:
            return

        card = self.grid_frames[key]
        img = self.images[key].copy()
        img.thumbnail((380, 260))
        
        self.tk_images[key] = ImageTk.PhotoImage(img)
        card.img_label.config(image=self.tk_images[key])
        card.img_label.place(relx=0.5, rely=0.5, anchor="center")
        card.placeholder.place_forget()

    def clear_display(self, key):
        """Clear image display"""
        card = self.grid_frames[key]
        card.img_label.place_forget()
        card.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def do_resize(self):
        if self.images['original'] is None:
            return
        
        self.images['resized'] = resize_image(self.images['original'])
        self.display_image('resized')
        
        self.btn_resize.config(state="disabled", bg="#6C757D")
        self.btn_norm.config(state="normal")
        self.status_label.config(text="✓ Image resized to 299×299")
        self.preprocess_steps += 1
        self.check_enable_dataset()

    def do_normalize(self):
        source_img = self.images['original']
        
        self.images['normalized'] = normalize_image(source_img)
        self.display_image('normalized')
        
        self.btn_norm.config(state="disabled", bg="#6C757D")
        self.btn_aug.config(state="normal")
        self.status_label.config(text="✓ Image normalized")
        self.preprocess_steps += 1
        self.check_enable_dataset()

    def do_augment(self):
        source_img = self.images['original']
                     
        
        self.images['augmented'] = augment_image(source_img)
        self.display_image('augmented')
        
        self.btn_aug.config(state="disabled", bg="#6C757D")
        self.status_label.config(text="✓ All preprocessing steps completed!")
        self.preprocess_steps += 1
        self.check_enable_dataset()

    def check_enable_dataset(self):
        if self.preprocess_steps >= 3:
            self.btn_process_dataset.config(state="normal")

    def process_dataset(self):
        if not os.path.exists(DATASET_DIR):
            messagebox.showerror("Error", f"Folder '{DATASET_DIR}' not found!")
            return

        self.status_label.config(text="⏳ Processing dataset...")
        self.root.update()

        processed_count = 0
        for class_name in os.listdir(DATASET_DIR):
            class_path = os.path.join(DATASET_DIR, class_name)
            if not os.path.isdir(class_path):
                continue

            out_path = os.path.join(OUTPUT_DIR, class_name)
            os.makedirs(out_path, exist_ok=True)

            for file in os.listdir(class_path):
                try:
                    img = Image.open(os.path.join(class_path, file))
                    img = resize_image(img)
                    img = normalize_image(img)
                    img = augment_image(img)
                    img.save(os.path.join(out_path, file))
                    processed_count += 1
                except:
                    pass

        self.status_label.config(text=f"✓ Dataset processed! ({processed_count} images)")
        messagebox.showinfo("Success", 
                           f"Dataset processed successfully!\n{processed_count} images saved to '{OUTPUT_DIR}'")


# ========= RUN ==========
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()