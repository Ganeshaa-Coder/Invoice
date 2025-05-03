"""
Invoice Generator Script

This script allows users to input item details (name, quantity, price)
and generates a text-based invoice displayed in the console.
Optionally, it can also generate a PDF version of the invoice.

Usage:
1. Ensure you have Python installed.
2. Install the required library:
   pip install reportlab
3. Run the script from your terminal:
   python Invoice.py
4. Follow the prompts to enter item details.
5. Choose whether to generate a PDF invoice when prompted.

Dependencies:
- reportlab: Used for generating PDF invoices.
"""
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import sys # Import sys to check for reportlab


def generate_pdf_invoice(filename, items, subtotal, tax, grand_total):
    """
    Generates a PDF invoice with the given details.

    Args:
        filename (str): The name of the PDF file to create.
        items (list): A list of dictionaries, each containing 'name', 'quantity', 'price'.
        subtotal (float): The subtotal amount.
        tax (float): The tax amount.
        grand_total (float): The total amount including tax.
    """
    # Check if reportlab is available (needed for Paragraph and getSampleStyleSheet)
    # Although top-level imports are present, this check ensures clarity if called elsewhere
    # without guaranteeing the context has these specific sub-modules imported.
    # However, the main check is now within generate_invoice before calling this.
    # For robustness, keep the check here too? Or rely on the caller?
    # Let's assume the caller ensures necessary imports like Paragraph are available.

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Invoice Title
    title = "Invoice"
    story.append(Paragraph(title, styles['h1']))
    story.append(Spacer(1, 12)) # 12 points of space

    # Prepare table data
    # Header row
    data = [['Item', 'Quantity', 'Price', 'Total']]
    # Item rows
    for item in items:
        item_total = item["quantity"] * item["price"]
        data.append([
            item['name'],
            str(item['quantity']),
            f"₹{item['price']:.2f}",
            f"₹{item_total:.2f}"
        ])
    # Summary rows
    data.append(['', '', 'Subtotal', f"₹{subtotal:.2f}"])
    data.append(['', '', 'Tax (18%)', f"₹{tax:.2f}"])
    data.append(['', '', 'Grand Total', f"₹{grand_total:.2f}"])

    # Create table
    table = Table(data, colWidths=[200, 80, 100, 100]) # Adjust column widths as needed

    # Add style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),       # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),              # Center align all cells initially
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header font bold
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),             # Header bottom padding
        ('BACKGROUND', (0, 1), (-1, -4), colors.beige),     # Background for item rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),        # Grid lines for all cells
        # Align numeric columns (Price, Total) to the right for items and summary
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        # Make summary rows bold
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),# Background for summary rows
    ])
    table.setStyle(style)

    story.append(table)
    story.append(Spacer(1, 24)) # 24 points of space after table

    # Build the PDF
    try:
        doc.build(story)
        print(f"PDF invoice generated successfully: {filename}")
    except Exception as e:
        # This might be redundant if called from generate_invoice which has its own try-except
        print(f"Error building PDF: {e}")


def generate_invoice():
    """Collects item details from the user and prints a text invoice."""
    print("Invoice Generator\n")
    items = []

    while True:
        name = input("Enter item name (or 'done' to finish): ")
        if name.lower() == "done":
            break
        try:
            quantity = int(input("Quantity: "))
            price = float(input("Price per item: ₹ "))
            if quantity <= 0 or price < 0:
                 print("Quantity must be positive and price cannot be negative. Please enter again.\n")
                 continue
            items.append({"name": name, "quantity": quantity, "price": price})
        except ValueError:
            print("Invalid quantity or price (must be numbers). Please enter again.\n")

    if not items:
        print("No items entered. Exiting.")
        return

    print("\n------ Invoice ------")
    subtotal = 0
    for item in items:
        total = item["quantity"] * item["price"]
        subtotal += total
        print(f"{item['name']} (x{item['quantity']}): ₹{total:.2f}")

    tax = subtotal * 0.18  # 18% tax
    grand_total = subtotal + tax
    print(f"\nSubtotal: ₹{subtotal:.2f}")
    print(f"Tax (18%): ₹{tax:.2f}")
    print(f"Total: ₹{grand_total:.2f}")
    print("---------------------")

    # Ask user if they want a PDF
    generate_pdf = input("Generate PDF invoice? (yes/no): ").lower()
    if generate_pdf == 'yes':
        pdf_filename = input("Enter PDF filename (e.g., invoice.pdf): ")
        if not pdf_filename.lower().endswith('.pdf'):
             pdf_filename += '.pdf' # Ensure .pdf extension

        try:
            # Check if reportlab is installed *before* calling generate_pdf_invoice
            # Although generate_pdf_invoice uses imports defined at top-level,
            # the Paragraph import specifically was moved here for clarity.
            # Let's ensure all necessary imports for reportlab are checked.
            # Note: The top-level imports handle most cases if script is run directly.
            # This try-except primarily catches runtime ImportError if reportlab isn't installed.
            # from reportlab.platypus import Paragraph # Already imported at top
            # from reportlab.lib.styles import getSampleStyleSheet # Already imported at top

            generate_pdf_invoice(pdf_filename, items, subtotal, tax, grand_total)
        except ImportError:
            print("\nError: ReportLab library not found or Paragraph/getSampleStyleSheet not available.")
            print("Please ensure ReportLab is installed: pip install reportlab")
        except Exception as e:
            print(f"\nAn error occurred during PDF generation: {e}")


if __name__ == "__main__":
    generate_invoice()
