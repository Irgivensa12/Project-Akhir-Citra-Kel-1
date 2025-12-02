import os
import tkinter as tk
from tkinter import filedialog, messagebox
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
        self.root.geometry("850x650")
        self.root.configure(bg="#E8EDF5")   # background soft

        self.img = None
        self.preprocess_steps = 0

        # ================================
        # CARD CONTAINER (WHITE BOX)
        # ================================
        self.card = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=650, height=520)

        # TITLE
        self.title = tk.Label(self.card, text="Image Processing System",
                              bg="white", fg="#1A1A1A",
                              font=("Segoe UI", 22, "bold"))
        self.title.pack(pady=(20, 5))

        self.subtitle = tk.Label(self.card,
                                 text="Upload an image to begin preprocessing",
                                 bg="white", fg="#6A6A6A",
                                 font=("Segoe UI", 11))
        self.subtitle.pack()

        # ========================
        # UPLOAD BOX
        # ========================
        self.upload_box = tk.Frame(self.card, bg="#F3F5F7", bd=2, relief="ridge")
        self.upload_box.pack(pady=25)
        self.upload_box.config(width=500, height=160)

        self.upload_box.bind("<Button-1>", lambda e: self.upload_image())

        self.upload_text = tk.Label(self.upload_box, text="⬆\nClick to Upload Image",
                                    bg="#F3F5F7", fg="#808080",
                                    font=("Segoe UI", 14))
        self.upload_text.place(relx=0.5, rely=0.5, anchor="center")

        # ============================
        # PREVIEW IMAGE
        # ============================
        self.preview_label = tk.Label(self.card, bg="white")
        self.preview_label.pack()

        # ============================
        # BUTTON AREA
        # ============================
        self.button_frame = tk.Frame(self.card, bg="white")
        self.button_frame.pack(pady=15)

        self.btn_resize = self.make_button("Resize 299x299", self.do_resize)
        self.btn_norm = self.make_button("Normalize", self.do_normalize)
        self.btn_aug = self.make_button("Augment", self.do_augment)

        # Disable all first
        self.disable_buttons()

        # PROCESS DATA BUTTON
        self.btn_process_dataset = self.make_button("Process Dataset", self.process_dataset)
        self.btn_process_dataset.config(state="disabled")
        self.btn_process_dataset.pack(pady=(15, 0))

    # ======================================================
    # BEAUTIFUL BUTTON MAKER
    # ======================================================
    def make_button(self, text, command):
        btn = tk.Button(self.button_frame, text=text, command=command,
                        bg="#4A79FF", fg="white",
                        font=("Segoe UI", 10, "bold"),
                        relief="flat", width=20, height=1,
                        bd=0, activebackground="#3A63D1",
                        cursor="hand2")
        btn.pack(pady=5)
        return btn

    def disable_buttons(self):
        self.btn_resize.config(state="disabled")
        self.btn_norm.config(state="disabled")
        self.btn_aug.config(state="disabled")

    # ======================================================
    # UPLOAD IMAGE
    # ======================================================
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if not path:
            return

        self.img = Image.open(path)
        self.show_preview()

        # Enable preprocessing buttons
        self.btn_resize.config(state="normal")
        self.btn_norm.config(state="normal")
        self.btn_aug.config(state="normal")

        # Reset state
        self.preprocess_steps = 0
        self.btn_process_dataset.config(state="disabled")

    # ======================================================
    # SHOW PREVIEW
    # ======================================================
    def show_preview(self):
        preview = self.img.copy()
        preview.thumbnail((350, 350))
        self.tk_preview = ImageTk.PhotoImage(preview)
        self.preview_label.config(image=self.tk_preview)

    # ======================================================
    # PREPROCESS ACTIONS
    # ======================================================
    def step_done(self):
        self.preprocess_steps += 1
        if self.preprocess_steps >= 3:
            self.btn_process_dataset.config(state="normal")

    def do_resize(self):
        self.img = resize_image(self.img)
        self.show_preview()
        self.step_done()

    def do_normalize(self):
        self.img = normalize_image(self.img)
        self.show_preview()
        self.step_done()

    def do_augment(self):
        self.img = augment_image(self.img)
        self.show_preview()
        self.step_done()

    # ======================================================
    # PROCESS DATASET
    # ======================================================
    def process_dataset(self):
        if not os.path.exists(DATASET_DIR):
            messagebox.showerror("Error", f"Folder '{DATASET_DIR}' not found!")
            return

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
                except:
                    pass

        messagebox.showinfo("Done", "Dataset processed successfully!")


# ========= RUN ==========
root = tk.Tk()
App(root)
root.mainloop()
