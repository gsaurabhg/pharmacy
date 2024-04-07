#pip install PyPDF2
#pip install reportlab


import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from PyPDF2 import PdfReader, PdfWriter

from pharmacyapp.models import Post, Bill, PatientDetail


def merge_pdf(existing_pdf_path, pdf_to_append_path):
  existing_pdf = open(existing_pdf_path, "rb")
  existing_pdf_reader = PdfReader(existing_pdf)

  # Create PdfWriter object to hold combined content
  writer = PdfWriter()

  # Append pages from existing PDF
  for page in existing_pdf_reader.pages:
    writer.add_page(page)

  # Open PDF to append
  pdf_to_append = open(pdf_to_append_path, "rb")
  pdf_to_append_reader = PdfReader(pdf_to_append)

  # Append pages from PDF to append
  for page in pdf_to_append_reader.pages:
    writer.add_page(page)

  # Write combined content to existing PDF file
  with open(pdf_to_append_path, "wb") as output_pdf:
    writer.write(output_pdf)

  # Close files
  existing_pdf.close()
  pdf_to_append.close()
  os.remove(existing_pdf_path)

def generate_pdf(bill_no):
  # Query the data using Django ORM
  billGeneration = Bill.objects.filter(billNo__exact=bill_no)

  # Define the name of the PDF file
  pdf_file = "temp.pdf"
  output = open(pdf_file, "wb")

  # Extract data from the queryset
  total=0
  data = [["Medicines", "Batch Number", "Expiry Date", "Unit Prise", "Quantity", "Price", "Discounted Price"]]  # Initialize with headers
  for obj in billGeneration:
      row = [obj.medicineName, obj.batchNo, obj.expiryDate,obj.pricePerTablet,obj.noOfTabletsOrdered,obj.totalPrice,obj.discountedPrice]
      total=total+obj.totalPrice
      data.append(row)

  #append the total bill value
  row= ["Total","","","","","",total]
  data.append(row)

  # Create PDF document
  doc = SimpleDocTemplate(output, pagesize=letter, mode='a')  # 'a' for append mode
  elements = []

  # Add heading
  styles = getSampleStyleSheet()
  heading_style = ParagraphStyle(name='Heading1', parent=styles['Heading1'], alignment=1)  # 1 = Center alignment
  heading = Paragraph("<b>Shree Sai Drug Shop</b>", heading_style)
  elements.append(heading)

  heading_style = ParagraphStyle(name='Heading2', parent=styles['Heading2'], alignment=2)  # 2 = Right alignment
  heading = Paragraph("<b>C1, Vikram Colony, Aligarh, Ph.:0571-2972424</b>", heading_style)
  elements.append(heading)

  # Add line separator 
  elements.append(Spacer(1, 12))  # Add some space after heading
  #---> error in next line?
  #elements.append(Line(0, 0, 530, 0))  # Adjust the length as needed

  heading_style = ParagraphStyle(name='Heading3', parent=styles['Heading3'], alignment=0)  # 0 = Left alignment
  name=billGeneration[0].patientID.patientName
  name2Use=f"<b>Patient name:  {name}</b>"
  heading = Paragraph(name2Use, heading_style)
  elements.append(heading)
  bill= billGeneration[0].billNo
  bill2Use=f"<b>Bill No: {bill}</b>"
  heading = Paragraph(bill2Use, heading_style)
  billD= billGeneration[0].billDate
  billD2Use=f"<b>Bill Date: {billD}</b>"
  heading = Paragraph(billD2Use, heading_style)
  PNo= billGeneration[0].patientID.patientPhoneNo
  Phone2Use=f"<b>Bill Date: {PNo}</b>"
  heading = Paragraph(Phone2Use, heading_style)
  
  elements.append(heading)


  # Add data table
  table = Table(data)

  # Style the table
  style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                      ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                      ('GRID', (0, 0), (-1, -1), 1, colors.black)])

  table.setStyle(style)
  elements.append(table)


  # Build PDF
  doc.build(elements)
  output.close()

  temp_pdf_path = "temp.pdf"
  merge_to_bil_path = "bills.pdf"
  merge_pdf(temp_pdf_path, merge_to_bil_path)