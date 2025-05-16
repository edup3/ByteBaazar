from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .report_generator import ReportGenerator
from io import BytesIO
from django.http import FileResponse

class PDFReportGenerator(ReportGenerator):
    def generate(self, products):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Reporte de Productos")

        y = 720
        for product in products:
            p.drawString(100, y, f"{product.name} - ${product.price} - Stock: {product.stock}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="productos.pdf")
