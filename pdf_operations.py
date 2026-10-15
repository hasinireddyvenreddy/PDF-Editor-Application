import fitz
from pathlib import Path
from PIL import Image


class PDFEditor:

    @staticmethod
    def merge_pdfs(files, output):
        """Merge multiple PDF files into one PDF."""
        if not files:
            raise ValueError("Please select PDF files.")

        merged_pdf = fitz.open()

        try:
            for file in files:
                with fitz.open(file) as pdf:
                    merged_pdf.insert_pdf(pdf)

            merged_pdf.save(output)

        finally:
            merged_pdf.close()

    @staticmethod
    def split_pdf(file, output_folder):
        """Split a PDF into separate one-page PDF files."""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        with fitz.open(file) as pdf:
            if len(pdf) == 0:
                raise ValueError("The PDF contains no pages.")

            for page_number in range(len(pdf)):
                new_pdf = fitz.open()

                try:
                    new_pdf.insert_pdf(
                        pdf,
                        from_page=page_number,
                        to_page=page_number
                    )

                    output_file = (
                        output_folder /
                        f"page_{page_number + 1}.pdf"
                    )

                    new_pdf.save(str(output_file))

                finally:
                    new_pdf.close()

    @staticmethod
    def rotate_pdf(file, output, angle):
        """Rotate every page in a PDF."""
        with fitz.open(file) as pdf:
            if len(pdf) == 0:
                raise ValueError("The PDF contains no pages.")

            for page in pdf:
                page.set_rotation(
                    (page.rotation + angle) % 360
                )

            pdf.save(output)

    @staticmethod
    def extract_text(file, output):
        """Extract text from a PDF into a text file."""
        extracted_text = []

        with fitz.open(file) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                extracted_text.append(
                    f"--- Page {page_number} ---\n"
                )
                extracted_text.append(page.get_text())
                extracted_text.append("\n\n")

        with open(output, "w", encoding="utf-8") as text_file:
            text_file.write("".join(extracted_text))

    @staticmethod
    def delete_pages(file, output, pages):
        """Delete selected pages using 1-based page numbers."""
        pages_to_delete = sorted(set(pages))

        with fitz.open(file) as pdf:
            page_count = len(pdf)

            if not pages_to_delete:
                raise ValueError("Please enter page numbers.")

            if any(
                page < 1 or page > page_count
                for page in pages_to_delete
            ):
                raise ValueError(
                    f"Enter page numbers between 1 and {page_count}."
                )

            if len(pages_to_delete) >= page_count:
                raise ValueError(
                    "You cannot delete every page in the PDF."
                )

            for page_number in reversed(pages_to_delete):
                pdf.delete_page(page_number - 1)

            pdf.save(output)

    @staticmethod
    def reorder_pages(file, output, order):
        """Reorder pages using a list of page numbers."""
        with fitz.open(file) as source_pdf:
            page_count = len(source_pdf)

            if (
                len(order) != page_count
                or sorted(order) != list(range(1, page_count + 1))
            ):
                raise ValueError(
                    f"Enter every page number from 1 to {page_count} "
                    "exactly once."
                )

            new_pdf = fitz.open()

            try:
                for page_number in order:
                    new_pdf.insert_pdf(
                        source_pdf,
                        from_page=page_number - 1,
                        to_page=page_number - 1
                    )

                new_pdf.save(output)

            finally:
                new_pdf.close()

    @staticmethod
    def images_to_pdf(image_files, output):
        """Convert multiple images into one PDF."""
        if not image_files:
            raise ValueError("Please select at least one image.")

        images = []

        try:
            for image_file in image_files:
                with Image.open(image_file) as image:
                    images.append(image.convert("RGB"))

            first_image = images[0]

            first_image.save(
                output,
                "PDF",
                save_all=True,
                append_images=images[1:]
            )

        finally:
            for image in images:
                image.close()

    @staticmethod
    def pdf_to_images(file, output_folder):
        """Convert each PDF page into a PNG image."""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        with fitz.open(file) as pdf:
            if len(pdf) == 0:
                raise ValueError("The PDF contains no pages.")

            for page_number, page in enumerate(pdf, start=1):
                pixmap = page.get_pixmap(dpi=150)

                output_file = (
                    output_folder / f"page_{page_number}.png"
                )

                pixmap.save(str(output_file))