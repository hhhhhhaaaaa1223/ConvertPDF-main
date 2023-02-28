import PyPDF2
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import fitz
class PDF():
    def __init__(self):
        super().__init__()
        
    def open_pdf(self,path):
        pdf_file = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        return pdf_reader
    def copy_pdf(self, pdf_reader):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.appendPagesFromReader(pdf_reader)
        
    
    def highlight_coordinates(coordinates, pdf_file_path, output_file_path):
        with fitz.open(pdf_file_path) as pdf_file:
            for page_num, x0, y0, x1, y1 in coordinates:
                page = pdf_file[page_num]
                highlight = page.add_highlight_annot(fitz.Rect(x0, y0, x1, y1))
                highlight.update()
            pdf_file.save(output_file_path, incremental=True)
    
    def find_coordinates_text_in_pdf(self,start_text, end_text, pdf_file_path):
        pdf_reader = self.open_pdf(pdf_file_path)
        num_pages = pdf_reader.getNumPages()
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            page_text = page.extractText()
            start_index = page_text.find(start_text)
            if start_index != -1:
                # Tìm vị trí kết thúc cần tìm
                end_index = page_text.find(end_text, start_index + len(start_text))
                if end_index != -1:
                    # Lấy tọa độ của khoảng text cần tìm trên trang
                    bbox = page_text[start_index:end_index].strip()
                    bbox = bbox.split('\n')[0]
                    bbox = bbox.split(',')
                    x0 = float(bbox[0])
                    y0 = float(bbox[1])
                    x1 = float(bbox[2])
                    y1 = float(bbox[3])
                    yield (page_num, x0, y0, x1, y1)
        
    def highlight_pdf(self,pdf_writer):
        page_number = 0  # Trang PDF bắt đầu từ 0
        page = pdf_writer.getPage(page_number)
        pdf_canvas = canvas.Canvas('new.pdf', page.mediaBox.getWidth(), page.mediaBox.getHeight())