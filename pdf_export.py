
# what it does

# 1. Take the itinerary text as input
# 2. Create a PDF with a title and the itinerary content
# 3. Return the PDF as bytes so Streamlit can offer it as a download

from fpdf import FPDF

def generate_pdf(itinerary_text, destination, num_days):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)   # left, top, right margins — fixes the space error
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, f"{num_days}-Day Trip to {destination}", ln=True, align="C")
    pdf.ln(5)

    # Body
    pdf.set_font("Helvetica", size=10)

    for line in itinerary_text.split("\n"):
        # Clean markdown formatting
        line = line.replace("**", "").replace("##", "").replace("#", "").strip()

        # Skip empty lines but add spacing
        if not line:
            pdf.ln(3)
            continue

        # Encode safely — drop any character FPDF can't handle
        line = line.encode("latin-1", errors="ignore").decode("latin-1")

        # Skip lines that are still empty after encoding
        if not line.strip():
            pdf.ln(3)
            continue

        try:
            pdf.multi_cell(0, 6, txt=line)
        except Exception:
            pass   # silently skip any line that still causes issues

    return bytes(pdf.output())