
import os
import re
from urllib.parse import urlparse

import tkinter as tk
from tkinter import filedialog, messagebox

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageTk


# ---------- Helpers ----------
def normalize_url(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    u = urlparse(s)
    if not u.scheme:  # add https:// if they typed example.com
        s = "https://" + s
        u = urlparse(s)
    return s if u.netloc else ""


def safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")
    return text or "link"


def build_qr_jpg(data: str, box_size: int = 12, border: int = 4) -> Image.Image:
    """Return a PIL Image (RGB) for the QR code."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


# ---------- GUI ----------
class QRGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("650x750")  # larger window
        self.resizable(False, False)

        # State
        self.current_img = None
        self.preview_photo = None

        # --- Title ---
        tk.Label(self, text="QR Code Generator", font=(
            "Arial", 24, "bold")).pack(pady=(20, 10))

        # --- Row 0: URL ---
        tk.Label(self, text="Link (https://...):",
                 font=("Arial", 14)).pack(pady=(5, 5))
        self.var_url = tk.StringVar()
        ent = tk.Entry(self, textvariable=self.var_url,
                       width=60, font=("Arial", 14))
        ent.pack(pady=(0, 15))
        ent.focus()

        # --- Row 1: Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Generate", font=("Arial", 12),
                  command=self.on_generate).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Save JPG", font=("Arial", 12),
                  command=self.on_save_jpg).grid(row=0, column=1, padx=10)

        # --- Row 2: Preview ---
        self.preview = tk.Label(
            self, bd=2, relief="sunken", width=500, height=500)
        self.preview.pack(padx=10, pady=20)

        # Enter key = Generate
        self.bind("<Return>", lambda e: self.on_generate())

    def on_generate(self):
        url = normalize_url(self.var_url.get())
        if not url:
            messagebox.showerror(
                "Invalid link", "Please enter a valid link (e.g., https://example.com)")
            return

        try:
            pil_img = build_qr_jpg(url)
            self.current_img = pil_img

            max_side = 500
            scale = min(max_side / pil_img.width, max_side / pil_img.height)
            disp = pil_img.resize(
                (int(pil_img.width * scale), int(pil_img.height * scale)), Image.NEAREST)
            self.preview_photo = ImageTk.PhotoImage(disp)
            self.preview.configure(image=self.preview_photo)
        except Exception as e:
            messagebox.showerror("Generation failed", str(e))

    def on_save_jpg(self):
        if self.current_img is None:
            messagebox.showinfo("No QR yet", "Click Generate first.")
            return

        url = normalize_url(self.var_url.get())
        host = urlparse(url).netloc if url else "qr"
        default_name = f"qr_{safe_filename(host)}.jpg"

        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG image", "*.jpg"), ("JPEG image", "*.jpeg")],
            initialfile=default_name,
            title="Save QR Code (JPG)",
        )
        if not path:
            return

        try:
            img = self.current_img.convert("RGB")
            img.save(path, format="JPEG", quality=95, optimize=True)
            messagebox.showinfo("Saved", f"Saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))


if __name__ == "__main__":
    app = QRGUI()
    app.mainloop()
