import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from pdf_operations import PDFEditor


class PDFEditorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor Application")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="PDF Editor Application",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Manage, edit, and convert your PDF files",
            font=("Arial", 11)
        )
        subtitle.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=25)

        buttons = [
            ("Merge PDFs", self.merge_pdfs),
            ("Split PDF", self.split_pdf),
            ("Rotate PDF", self.rotate_pdf),
            ("Delete Pages", self.delete_pages),
            ("Reorder Pages", self.reorder_pages),
            ("Extract Text", self.extract_text),
            ("Images to PDF", self.images_to_pdf),
            ("PDF to Images", self.pdf_to_images)
        ]

        for index, (text, command) in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=22,
                height=2,
                font=("Arial", 11)
            )
            button.grid(
                row=index // 2,
                column=index % 2,
                padx=12,
                pady=10
            )

        footer = tk.Label(
            self.root,
            text="PDF Editor Project | Python and Tkinter",
            font=("Arial", 9)
        )
        footer.pack(side="bottom", pady=15)

    def run_operation(self, operation, *args):
        try:
            operation(*args)
            messagebox.showinfo(
                "Success",
                "Operation completed successfully!"
            )
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Operation failed:\n{error}"
            )

    def merge_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not files:
            return

        output = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output:
            self.run_operation(
                PDFEditor.merge_pdfs, files, output
            )

    def split_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        folder = filedialog.askdirectory(
            title="Select output folder"
        )
        if folder:
            self.run_operation(
                PDFEditor.split_pdf, file, folder
            )

    def rotate_pdf(self):
        file = filedialog.askopenfilename(
            title="Select PDF to rotate",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        angle = simpledialog.askinteger(
            "Rotate PDF",
            "Enter rotation angle (90, 180, or 270):",
            minvalue=90,
            maxvalue=270
        )
        if angle is None:
            return

        if angle not in (90, 180, 270):
            messagebox.showerror(
                "Invalid Angle",
                "Enter 90, 180, or 270 degrees."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Save rotated PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output:
            self.run_operation(
                PDFEditor.rotate_pdf, file, output, angle
            )

    def delete_pages(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        pages_text = simpledialog.askstring(
            "Delete Pages",
            "Enter page numbers to delete, separated by commas:\n"
            "Example: 2,4,5"
        )
        if not pages_text:
            return

        try:
            pages = [
                int(number.strip())
                for number in pages_text.split(",")
            ]
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter page numbers separated by commas."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Save edited PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output:
            self.run_operation(
                PDFEditor.delete_pages, file, output, pages
            )

    def reorder_pages(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        order_text = simpledialog.askstring(
            "Reorder Pages",
            "Enter the new page order separated by commas.\n"
            "Example: 3,1,2"
        )
        if not order_text:
            return

        try:
            order = [
                int(number.strip())
                for number in order_text.split(",")
            ]
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter page numbers separated by commas."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Save reordered PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output:
            self.run_operation(
                PDFEditor.reorder_pages, file, output, order
            )

    def extract_text(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        output = filedialog.asksaveasfilename(
            title="Save extracted text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if output:
            self.run_operation(
                PDFEditor.extract_text, file, output
            )

    def images_to_pdf(self):
        files = filedialog.askopenfilenames(
            title="Select images",
            filetypes=[
                (
                    "Image files",
                    "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"
                )
            ]
        )
        if not files:
            return

        output = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output:
            self.run_operation(
                PDFEditor.images_to_pdf, files, output
            )

    def pdf_to_images(self):
        file = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file:
            return

        folder = filedialog.askdirectory(
            title="Select output folder"
        )
        if folder:
            self.run_operation(
                PDFEditor.pdf_to_images, file, folder
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditorApp(root)
    root.mainloop()