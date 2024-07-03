import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.upload_button = tk.Button(self.frame, text="Upload Image", command=self.upload_image, bg="blue", fg="white", font=("Arial", 12))
        self.upload_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.canvas = tk.Canvas(self.frame, width=800, height=600, bg="gray")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=10)

        self.left_label = tk.Label(self.frame, text="Left:", font=("Arial", 10))
        self.left_label.grid(row=2, column=0, sticky="e")
        self.left_entry = tk.Entry(self.frame)
        self.left_entry.grid(row=2, column=1, sticky="w")

        self.upper_label = tk.Label(self.frame, text="Upper:", font=("Arial", 10))
        self.upper_label.grid(row=3, column=0, sticky="e")
        self.upper_entry = tk.Entry(self.frame)
        self.upper_entry.grid(row=3, column=1, sticky="w")

        self.right_label = tk.Label(self.frame, text="Right:", font=("Arial", 10))
        self.right_label.grid(row=4, column=0, sticky="e")
        self.right_entry = tk.Entry(self.frame)
        self.right_entry.grid(row=4, column=1, sticky="w")

        self.lower_label = tk.Label(self.frame, text="Lower:", font=("Arial", 10))
        self.lower_label.grid(row=5, column=0, sticky="e")
        self.lower_entry = tk.Entry(self.frame)
        self.lower_entry.grid(row=5, column=1, sticky="w")

        self.crop_button = tk.Button(self.frame, text="Crop Image", command=self.crop_image, bg="green", fg="white", font=("Arial", 12))
        self.crop_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(self.frame, text="Save Cropped Image", command=self.save_image, bg="orange", fg="white", font=("Arial", 12))
        self.save_button.grid(row=6, column=1, columnspan=2, pady=10)

        self.image = None
        self.cropped_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        image.thumbnail((800, 600))  # Resize the image to fit the canvas
        self.imgtk = ImageTk.PhotoImage(image)
        self.canvas.create_image(400, 300, image=self.imgtk, anchor=tk.CENTER)

    def crop_image(self):
        try:
            if self.image:
                left = int(self.left_entry.get() or 0)
                upper = int(self.upper_entry.get() or 0)
                right = int(self.right_entry.get() or 0)
                lower = int(self.lower_entry.get() or 0)

                width, height = self.image.size

                # Adjust right and lower to be relative to width and height if zero is entered
                if right == 0:
                    right = width
                else:
                    right = width - right

                if lower == 0:
                    lower = height
                else:
                    lower = height - lower

                # Ensure cropping dimensions are valid
                if left < 0 or upper < 0 or right <= left or lower <= upper or right > width or lower > height:
                    messagebox.showerror("Error", "Invalid cropping dimensions.")
                    return

                self.cropped_image = self.image.crop((left, upper, right, lower))
                self.display_image(self.cropped_image)
            else:
                messagebox.showerror("Error", "No image uploaded.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_image(self):
        if self.cropped_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.cropped_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
        else:
            messagebox.showerror("Error", "No cropped image to save.")

root = tk.Tk()
app = ImageCropper(root)
root.mainloop()
