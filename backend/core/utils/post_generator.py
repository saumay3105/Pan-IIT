from io import BytesIO
from typing import Dict, Any
from dataclasses import dataclass
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pdf2image import convert_from_path
import os


@dataclass
class TextStyle:
    x: int
    y: int
    font_name: str
    font_size: int
    color: tuple[float, float, float]


@dataclass
class ImageConfig:
    url: str
    x: int
    y: int
    width: int
    height: int


@dataclass
class TemplateStyle:
    heading: TextStyle
    subtitle: TextStyle
    button: TextStyle
    description: TextStyle
    email: TextStyle
    image: ImageConfig


@dataclass
class TemplateContent:
    heading: str
    subtitle: str
    button: str
    description: str
    email: str
    image_url: str


# Define template styles (positioning and formatting)
TEMPLATE_STYLES = {
    "2": TemplateStyle(
        heading=TextStyle(
            x=40, y=668, font_name="Playfair", font_size=85, color=(0.25, 0.25, 0.17)
        ),
        subtitle=TextStyle(
            x=50, y=620, font_name="Rubik", font_size=35, color=(0.25, 0.25, 0.17)
        ),
        button=TextStyle(
            x=120, y=379, font_name="Rubik", font_size=25, color=(1, 1, 1)
        ),
        description=TextStyle(
            x=50, y=559, font_name="Rubik", font_size=25, color=(0.25, 0.25, 0.17)
        ),
        email=TextStyle(
            x=110, y=330, font_name="Rubik", font_size=25, color=(0.25, 0.25, 0.17)
        ),
        image=ImageConfig(
            url="", x=300, y=200, width=450, height=250  # Will be overridden by content
        ),
    ),
    "3": TemplateStyle(
        heading=TextStyle(
            x=60, y=700, font_name="Playfair", font_size=55, color=(0.97, 0.72, 0.19)
        ),
        subtitle=TextStyle(
            x=70, y=650, font_name="Rubik", font_size=30, color=(0.97, 0.72, 0.19)
        ),
        button=TextStyle(
            x=340, y=110, font_name="Rubik", font_size=22, color=(1, 1, 1)
        ),
        description=TextStyle(
            x=70, y=580, font_name="Rubik", font_size=22, color=(0.97, 0.72, 0.19)
        ),
        email=TextStyle(
            x=300, y=50, font_name="Rubik", font_size=22, color=(0.3, 0.3, 0.3)
        ),
        image=ImageConfig(
            url="", x=260, y=220, width=300, height=300  # Will be overridden by content
        ),
    ),
}


def register_fonts():
    """Register all required fonts."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define font files with complete paths
    font_files = {
        "PinyonScript-Regular": os.path.join(current_dir, "PinyonScript-Regular.ttf"),
        "Playfair": os.path.join(current_dir, "Playfair.ttf"),
        "Rubik": os.path.join(current_dir, "Rubik.ttf"),
    }

    for font_name, font_path in font_files.items():
        pdfmetrics.registerFont(TTFont(font_name, font_path))


def draw_text_element(canvas_obj: canvas.Canvas, text: str, style: TextStyle):
    """Draw a text element on the canvas using the provided style."""
    canvas_obj.setFont(style.font_name, style.font_size)
    canvas_obj.setFillColorRGB(*style.color)
    canvas_obj.drawString(style.x, style.y, text)


def add_text_to_design_template(
    input_pdf: str, output_pdf: str, template_id: str, content: TemplateContent
):
    """Generate a PDF using the specified template style and content."""
    if template_id not in TEMPLATE_STYLES:
        raise ValueError(f"Template ID {template_id} not found in styles")

    style = TEMPLATE_STYLES[template_id]

    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()
    page = pdf_reader.pages[0]

    # Create canvas for overlay
    packet = BytesIO()
    canvas_obj = canvas.Canvas(packet)

    # Register fonts
    register_fonts()

    # Draw all text elements
    draw_text_element(canvas_obj, content.heading, style.heading)
    draw_text_element(canvas_obj, content.subtitle, style.subtitle)
    draw_text_element(canvas_obj, content.button, style.button)
    draw_text_element(canvas_obj, content.description, style.description)
    draw_text_element(canvas_obj, content.email, style.email)

    # Draw image
    image = ImageReader(content.image_url)
    canvas_obj.drawImage(
        image,
        x=style.image.x,
        y=style.image.y,
        width=style.image.width,
        height=style.image.height,
        preserveAspectRatio=True,
    )

    canvas_obj.save()
    packet.seek(0)

    # Merge overlay with certificate
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]
    page.merge_page(overlay_page)
    pdf_writer.add_page(page)

    # Add remaining pages
    for page in pdf_reader.pages[1:]:
        pdf_writer.add_page(page)

    # Write output
    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"Design {template_id} Completed!")

    pages = convert_from_path(output_pdf, 500)

    for count, page in enumerate(pages):
        page.save(f"{output_pdf}.jpg", "JPEG")
