import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import docx
from docx.shared import Pt
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

OUTPUT_DIR = Path("./sample_test_docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def wrap_text(text: str, max_chars: int):
    words = text.split(" ")
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 <= max_chars:
            curr.append(w)
            curr_len += len(w) + 1
        else:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
    if curr:
        lines.append(" ".join(curr))
    return lines


def generate_legal_contract_pdf(filepath: Path):
    c = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(54, height - 54, "MASTER SERVICES AND IP LICENSING AGREEMENT")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(54, height - 72, "Between: Apex Global Software Inc. and Target Technologies LLC")
    c.drawString(54, height - 86, "Effective Date: January 15, 2024 | Document ID: MSA-2024-8849")
    c.line(54, height - 94, width - 54, height - 94)

    y = height - 120
    sections_p1 = [
        ("1. RECITALS & SCOPE OF ENGAGEMENT", 
         "Target Technologies LLC ('Provider') agrees to deliver continuous proprietary infrastructure algorithms "
         "to Apex Global Software Inc. ('Client') pursuant to the performance milestones set forth herein."),
        ("2. INTELLECTUAL PROPERTY & ASSIGNMENT RISKS", 
         "Section 2.3: Provider explicitly retains all title, copyright, and patent ownership to foundational codebases. "
         "CRITICAL RESTRICTION: No intellectual property rights created under Statement of Work #4 shall transfer to Client "
         "until full payment of trailing discretionary bonus tranches ($2.4M). Prior assignments contain reversion clauses."),
        ("3. INDEMNITY & UNLIMITED LIABILITY EXPOSURE", 
         "Section 3.1: Provider's indemnification obligations for third-party intellectual property infringement claims "
         "and data breach casualties ARE ENTIRELY UNCAPPED and expressly excluded from any limitation of liability provisions. "
         "Section 3.4: Target Technologies LLC shall defend, indemnify, and hold harmless Client from any consequential losses.")
    ]

    for title, body in sections_p1:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(54, y, title)
        y -= 16
        c.setFont("Helvetica", 9)
        text_obj = c.beginText(54, y)
        text_obj.setFont("Helvetica", 9)
        text_obj.setLeading(13)
        for line in wrap_text(body, 90):
            text_obj.textLine(line)
        c.drawText(text_obj)
        y -= (len(wrap_text(body, 90)) * 13 + 18)

    c.setFont("Helvetica", 8)
    c.drawString(width / 2 - 20, 36, "Page 1 of 2")
    c.showPage()

    c.setFont("Helvetica-Bold", 12)
    c.drawString(54, height - 54, "MASTER SERVICES AGREEMENT (CONTINUED)")
    c.line(54, height - 62, width - 54, height - 62)
    y = height - 90

    sections_p2 = [
        ("4. CHANGE OF CONTROL & ASSIGNABILITY", 
         "Section 4.2: Client possesses immediate unilateral termination rights in the event Target Technologies LLC "
         "enters into any merger, acquisition, restructuring, or majority equity acquisition exceeding 35% without prior "
         "written unanimous consent delivered 60 business days in advance. Failure to obtain consent triggers an automatic $5M penalty."),
        ("5. RESTRICTIVE COVENANTS & NON-COMPETE ENFORCEABILITY", 
         "Section 5.1: Target Technologies LLC and its designated key founders are prohibited from developing, marketing, or "
         "consulting on algorithmic logistics solutions across North America and Western Europe for a duration of 36 months post-termination."),
        ("6. GOVERNING LAW & MANDATORY ARBITRATION", 
         "This agreement shall be governed by Delaware law. Any unresolved dispute exceeding $250,000 shall be submitted to binding JAMS arbitration.")
    ]

    for title, body in sections_p2:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(54, y, title)
        y -= 16
        c.setFont("Helvetica", 9)
        text_obj = c.beginText(54, y)
        text_obj.setFont("Helvetica", 9)
        text_obj.setLeading(13)
        for line in wrap_text(body, 90):
            text_obj.textLine(line)
        c.drawText(text_obj)
        y -= (len(wrap_text(body, 90)) * 13 + 18)

    c.setFont("Helvetica", 8)
    c.drawString(width / 2 - 20, 36, "Page 2 of 2")
    c.save()


def generate_financial_model_xlsx(filepath: Path):
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Consolidated Financials"

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True)
    regular_font = Font(name="Calibri", size=10)
    navy_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    warn_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

    headers1 = ["Financial Metric (USD in Thousands)", "FY2022", "FY2023", "FY2024 (LTM)", "Variance (%)", "Forensic Audit Notes"]
    ws1.append(headers1)
    for col_idx in range(1, len(headers1) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    rows1 = [
        ("Gross Revenue", "$14,500", "$21,200", "$28,400", "+34.0%", "Aggressive milestone-based revenue recognition applied"),
        ("Cost of Goods Sold (COGS)", "$5,200", "$7,800", "$11,900", "+52.5%", "Hosting and cloud compute margin compression"),
        ("Gross Profit", "$9,300", "$13,400", "$16,500", "+23.1%", "Gross margin declined from 64.1% to 58.1%"),
        ("Operating Expenses (OPEX)", "$8,900", "$14,100", "$19,800", "+40.4%", "Rapid head-count expansion and G&A overhead"),
        ("EBITDA (Adjusted)", "$1,800", "$1,100", "($1,200)", "-209.1%", "Reported as positive using non-standard capitalization of R&D"),
        ("Senior Secured Debt (Term Loan B)", "$2,000", "$6,500", "$14,800", "+127.7%", "FLAG: Maturity due in Q3 2025; debt covenant threshold breached"),
        ("Subordinated Convertible Notes", "$0", "$3,000", "$5,000", "+66.7%", "8% PIK interest compounding; converts at 20% discount"),
        ("Total Cash & Cash Equivalents", "$5,100", "$3,400", "$1,450", "-57.4%", "HIGH RISK: Estimated runway is approximately 3.8 months"),
        ("Working Capital Deficit", "$1,200", "($450)", "($2,800)", "-522.2%", "Current liabilities significantly exceed liquid assets")
    ]

    for row_data in rows1:
        ws1.append(row_data)

    for r in range(2, len(rows1) + 2):
        is_warning = "FLAG" in str(ws1.cell(row=r, column=6).value) or "HIGH RISK" in str(ws1.cell(row=r, column=6).value)
        for c in range(1, len(headers1) + 1):
            cell = ws1.cell(row=r, column=c)
            cell.font = bold_font if c in [1, 4] else regular_font
            if is_warning:
                cell.fill = warn_fill

    ws2 = wb.create_sheet(title="Concentration & Liabilities")
    headers2 = ["Customer / Counterparty", "Annual Contract Value", "% of Total ARR", "Contract Expiry", "Audit Risk Note"]
    ws2.append(headers2)
    for col_idx in range(1, len(headers2) + 1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = navy_fill

    rows2 = [
        ("Global Retail Corp (Client A)", "$11,920,000", "42.0%", "Nov 2024", "CRITICAL CONCENTRATION: Up for RFP renewal; price reduction demanded"),
        ("Omni Logistics Holdings (Client B)", "$7,100,000", "25.0%", "Mar 2025", "Notice of dispute delivered over SLA delivery breaches"),
        ("Tier 3 Aggregated Customers", "$9,380,000", "33.0%", "Various", "Long-tail churn rate increased from 11% to 22% in FY24")
    ]

    for row_data in rows2:
        ws2.append(row_data)

    for col in ws1.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws1.column_dimensions[col[0].column_letter].width = max(max_len + 3, 12)

    for col in ws2.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws2.column_dimensions[col[0].column_letter].width = max(max_len + 3, 14)

    wb.save(str(filepath))


def generate_compliance_report_docx(filepath: Path):
    doc = docx.Document()

    p_title = doc.add_paragraph()
    run_title = p_title.add_run("ANNUAL REGULATORY, ESG, AND PRIVACY COMPLIANCE AUDIT")
    run_title.bold = True
    run_title.font.size = Pt(16)

    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Subject Entity: Target Technologies LLC | Jurisdiction: United States & European Union")
    run_sub.font.size = Pt(10)
    run_sub.italic = True
    doc.add_paragraph("─" * 80)

    doc.add_heading("1. Data Privacy and Cybersecurity Integrity (GDPR / CCPA)", level=1)
    doc.add_paragraph(
        "During the Q2 2024 vulnerability assessment, an unencrypted database replica containing approximately "
        "185,000 European Union customer transaction logs was exposed to the public internet for 19 days. "
        "Target Technologies LLC failed to report this incident to the Irish Data Protection Commission (DPC) within "
        "the statutory 72-hour notification window mandated under GDPR Article 33. Outside counsel estimates contingent "
        "administrative fines between €1,800,000 and €4,500,000 depending on final classification."
    )

    doc.add_heading("2. Export Control and International Sanctions Screenings", level=1)
    doc.add_paragraph(
        "A compliance screen of downstream software distributorship agreements revealed that Target Technologies LLC "
        "indirectly licensed proprietary encryption libraries to two sub-contracting logistics firms located in prohibited "
        "jurisdictions without obtaining prerequisite BIS (Bureau of Industry and Security) export licenses. "
        "A formal Voluntary Self-Disclosure (VSD) has not yet been submitted to the Department of Commerce."
    )

    doc.add_heading("3. Pending Material Litigation and Operational Licensing", level=1)
    doc.add_paragraph(
        "Case 24-CV-9821 (S.D.N.Y.): Ex-Chief Technology Officer v. Target Technologies LLC. Plaintiff alleges wrongful "
        "termination and trade secret misappropriation regarding core optimization patents, asserting ownership claims over "
        "the company's primary patent application #US-2023-01992. No litigation reserve has been established on the balance sheet."
    )

    doc.add_paragraph(
        "Operating Permits: The corporate entity has failed to renew its California Specialized Telecommunications "
        "Data License, currently operating under a 90-day grace period that expires on November 30, 2024."
    )

    doc.save(str(filepath))


if __name__ == "__main__":
    print(f"Generating synthetic due diligence documents in: {OUTPUT_DIR.resolve()} ...")

    legal_path = OUTPUT_DIR / "sample_legal_contract.pdf"
    generate_legal_contract_pdf(legal_path)
    print(f" -> Generated: {legal_path.name}")

    financial_path = OUTPUT_DIR / "sample_financial_statements.xlsx"
    generate_financial_model_xlsx(financial_path)
    print(f" -> Generated: {financial_path.name}")

    compliance_path = OUTPUT_DIR / "sample_compliance_audit.docx"
    generate_compliance_report_docx(compliance_path)
    print(f" -> Generated: {compliance_path.name}")

    print("\nAll sample documents generated successfully.")