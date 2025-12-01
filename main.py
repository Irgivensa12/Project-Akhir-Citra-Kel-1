import os
import tkinter as tk # tkinter untuk GUI
from tkinter import filedialog # untuk dialog file
from PIL import Image, ImageTk # untuk manipulasi gambar

from preprocessing.resize import resize_image  # mengimpor fungsi resize_image dari kelas resize dalam modul preprocessing
from preprocessing.normalisasi import normalize_image # mengimpor fungsi normalize_image dari kelas normalisasi dalam modul preprocessing
from preprocessing.augmentasi import augment_image # mengimpor fungsi augment_image dari kelas augmentasi dalam modul preprocessing
from tkinter import messagebox # untuk menampilkan pesan dialog

DATASET_DIR = "Dayak's Animal" # folder dataset
OUTPUT_DIR = "hasil_olah_dataset" # folder output hasil preprocessing


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Preprocessing Citra")

        self.image_label = tk.Label(root, text="Belum ada gambar")
        self.image_label.pack()

        # tombol untuk upload image manual
        btn_upload = tk.Button(root, text="Upload Gambar", command=self.upload_image)
        btn_upload.pack()

        btn_resize = tk.Button(root, text="Resize 299x299", command=self.do_resize)
        btn_resize.pack()

        btn_norm = tk.Button(root, text="Normalize", command=self.do_normalize)
        btn_norm.pack()

        btn_aug = tk.Button(root, text="Augment", command=self.do_augment)
        btn_aug.pack()

        # tombol untuk dataset processing
        btn_dataset = tk.Button(root, text="Proses Dataset", command=self.process_dataset)
        btn_dataset.pack()

    # mode upload gambar manual 

    def upload_image(self):
        path = filedialog.askopenfilename()
        self.img = Image.open(path)
        self.show(self.img)

    def show(self, img):
        img_tk = img.copy()
        img_tk.thumbnail((300, 300))
        self.tk_img = ImageTk.PhotoImage(img_tk)
        self.image_label.config(image=self.tk_img)

    def do_resize(self):
        self.img = resize_image(self.img)
        self.show(self.img)

    def do_normalize(self):
        self.img = normalize_image(self.img)
        self.show(self.img)

    def do_augment(self):
        self.img = augment_image(self.img)
        self.show(self.img)

    # Mode dataset processing

    def process_dataset(self):
        if not os.path.exists(DATASET_DIR):
            messagebox.showerror("Error", f"Folder '{DATASET_DIR}' tidak ditemukan!")
            return
        
        for class_name in os.listdir(DATASET_DIR):
            class_path = os.path.join(DATASET_DIR, class_name)

            if not os.path.isdir(class_path):
                continue

            output_class_dir = os.path.join(OUTPUT_DIR, class_name)
            os.makedirs(output_class_dir, exist_ok=True)

            for file in os.listdir(class_path):
                img_path = os.path.join(class_path, file)

                try:
                    img = Image.open(img_path)

                    # pipeline preprocessing
                    img = resize_image(img)
                    img = normalize_image(img)
                    img = augment_image(img)

                    save_path = os.path.join(output_class_dir, file)
                    img.save(save_path)

                except Exception as e:
                    print(f"Error memproses {file}: {e}")

        messagebox.showinfo("Selesai", "Dataset berhasil diproses!")


# ============================
# RUN GUI
# ============================

root = tk.Tk()
app = App(root)
root.mainloop()