"""Builds the CV and slide-deck PDFs into ../assets. Run: python tools/build_pdfs.py
Optional: drop Roboto-Regular.ttf, Roboto-Medium.ttf and Roboto-Bold.ttf into ../fonts to embed Roboto."""
import os
from reportlab.lib.colors import HexColor as H
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, KeepTogether

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets")

# ---- fonts: Roboto if available, else Helvetica
F, FM, FB = "Helvetica", "Helvetica", "Helvetica-Bold"
fd = os.path.join(ROOT, "fonts")
try:
    pdfmetrics.registerFont(TTFont("Roboto", os.path.join(fd, "Roboto-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Roboto-Medium", os.path.join(fd, "Roboto-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", os.path.join(fd, "Roboto-Bold.ttf")))
    F, FM, FB = "Roboto", "Roboto-Medium", "Roboto-Bold"
except Exception:
    pass

# ---- palette
INK, SLATE = H("#27364f"), H("#5d6b82")
BLUE, BLUE_D, LAV, MINT, PEACH, GREY, LINE = (H(x) for x in
    ("#cfe0f7", "#6f9bd9", "#e4defa", "#d6f1e6", "#fde3d6", "#f3f5f9", "#dde2ea"))

# ---- content
NAME, ROLE = "Aris Mansor Sofiyan", "Financial Analyst"
EMAIL, CITY = "hello@example.com", "Kuala Lumpur, Malaysia"
LI_URL, LI_TXT = "https://www.linkedin.com/in/lee-sai-hin", "linkedin.com/in/lee-sai-hin"
SUMMARY = ("Financial analyst with six years' experience in audit and corporate finance. I build valuation, "
           "forecasting and risk models that leadership teams use to make decisions, and I document every assumption "
           "so the logic is easy to follow and challenge.")
JOBS = [
    ("Senior Analyst", "Northbridge Capital", "2024 – Present", [
        "Lead valuation work for growth-stage investments across the portfolio.",
        "Cut model turnaround from two weeks to four days with a standard template.",
        "Present findings to the investment committee each month."]),
    ("Financial Analyst", "Meridian Group", "2021 – 2024", [
        "Built the annual budget model used by 12 business units.",
        "Flagged a $1.2M cost overrun early, saving the project from a loss.",
        "Automated month-end reporting with Excel VBA and SQL."]),
    ("Audit Associate", "Hartley & Co.", "2019 – 2021", [
        "Audited 15 mid-sized clients across retail and logistics.",
        "Trained four new joiners on audit tooling and documentation."]),
]
PROJECTS = [
    ("Retail chain valuation", "DCF and comparables model for a 40-store retailer ahead of an acquisition.", "Offer set 8% below the seller's ask."),
    ("Rolling cash forecast", "13-week cash model that pulls from the ledger and refreshes every Monday.", "No surprise shortfalls in 18 months."),
    ("Portfolio risk dashboard", "Power BI view of exposure, drawdown and stress tests by holding.", "Used in every monthly investment review."),
]
SKILLS = ["DCF and comparables", "Three-statement modelling", "Budgeting and forecasting", "Risk and sensitivity analysis",
          "Excel and VBA", "SQL and Python", "Power BI"]
EDU = ("B.Acc. (Hons) Accounting", "University of Malaya, 2015 – 2019")
CERTS = ["CFA Level 3 candidate (2026)", "ACCA affiliate"]
LANGS = ["English (fluent)", "Bahasa Malaysia (native)"]

# =================== CV (A4, one page) ===================
def cv():
    W, Hh = A4
    side_w = 190
    def bg(c, d):
        c.setFillColor(BLUE); c.rect(0, 0, side_w, Hh, stroke=0, fill=1)
        c.setFillColor(LAV); c.rect(0, Hh - 14, W, 14, stroke=0, fill=1)
        c.setFillColor(BLUE_D); c.rect(side_w, Hh - 14, W - side_w, 14, stroke=0, fill=1)
    doc = BaseDocTemplate(os.path.join(OUT, "Aris-Mansor-Sofiyan-CV.pdf"), pagesize=A4,
                          title=f"{NAME} – CV", author=NAME, leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0)
    side = Frame(0, 0, side_w, Hh, leftPadding=20, rightPadding=18, topPadding=36, bottomPadding=24, id="s")
    main = Frame(side_w, 0, W - side_w, Hh, leftPadding=26, rightPadding=30, topPadding=36, bottomPadding=24, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[side, main], onPage=bg)])

    P = lambda n, **k: ParagraphStyle(n, fontName=k.pop("fn", F), **k)
    name = P("n", fn=FB, fontSize=25, leading=29, textColor=INK)
    role = P("r", fn=FM, fontSize=12.5, leading=16, textColor=SLATE, spaceAfter=10)
    h = P("h", fn=FB, fontSize=10.5, leading=13, textColor=INK, spaceBefore=12, spaceAfter=5)
    body = P("b", fontSize=9.2, leading=13.2, textColor=INK)
    bul = P("bl", fontSize=9, leading=12.6, textColor=INK, leftIndent=10, bulletIndent=0)
    jt = P("jt", fn=FB, fontSize=10, leading=13, textColor=INK)
    jm = P("jm", fontSize=8.8, leading=12, textColor=SLATE, spaceAfter=3)
    sh = P("sh", fn=FB, fontSize=9.5, leading=12, textColor=INK, spaceBefore=14, spaceAfter=5)
    sb = P("sb", fontSize=8.8, leading=12.4, textColor=INK, spaceAfter=3)
    sl = P("sl", fontSize=8.8, leading=12.4, textColor=INK)

    s = [Paragraph("Contact", ParagraphStyle("c0", parent=sh, spaceBefore=96)),
         Paragraph(EMAIL, sb), Paragraph(CITY, sb),
         Paragraph(f'<link href="{LI_URL}" color="#27364f"><u>{LI_TXT}</u></link>', sb),
         Paragraph("Skills", sh)] + [Paragraph(x, sb) for x in SKILLS] + \
        [Paragraph("Education", sh), Paragraph(f"<b>{EDU[0]}</b>", sl), Paragraph(EDU[1], sb),
         Paragraph("Certifications", sh)] + [Paragraph(x, sb) for x in CERTS] + \
        [Paragraph("Languages", sh)] + [Paragraph(x, sb) for x in LANGS]
    from reportlab.platypus import FrameBreak
    s.append(FrameBreak())
    m = [Paragraph(NAME, name), Paragraph(ROLE, role), Paragraph("Profile", h), Paragraph(SUMMARY, body),
         Paragraph("Experience", h)]
    for t, co, yrs, bl in JOBS:
        m.append(KeepTogether([Paragraph(f"{t}, {co}", jt), Paragraph(yrs, jm)] +
                              [Paragraph(b, bul, bulletText="•") for b in bl] + [Spacer(1, 7)]))
    m.append(Paragraph("Selected projects", h))
    for t, d, r in PROJECTS:
        m.append(Paragraph(f"<b>{t}.</b> {d} <font color='#5d6b82'>{r}</font>", bul, bulletText="•"))
    doc.build(s + m)

# =================== Slides (16:9) ===================
SW, SH = 960, 540
def wrap(c, text, x, y, w, font, size, color, lead=None):
    lead = lead or size * 1.4
    c.setFillColor(color); c.setFont(font, size)
    for ln in simpleSplit(text, font, size, w):
        c.drawString(x, y, ln); y -= lead
    return y

def slides():
    c = canvas.Canvas(os.path.join(OUT, "Aris-Mansor-Sofiyan-Slides.pdf"), pagesize=(SW, SH))
    c.setTitle(f"{NAME} – Profile"); c.setAuthor(NAME)
    total = 6
    def base(n, title, fill=H("#ffffff")):
        c.setFillColor(fill); c.rect(0, 0, SW, SH, stroke=0, fill=1)
        c.setFillColor(BLUE); c.rect(0, SH - 10, SW, 10, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont(FB, 30); c.drawString(60, SH - 80, title)
        c.setFillColor(SLATE); c.setFont(F, 11); c.drawString(60, 28, f"{NAME}  |  {ROLE}")
        c.drawRightString(SW - 60, 28, f"{n} / {total}")

    # 1 title
    c.setFillColor(BLUE); c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(LAV); c.circle(SW - 120, SH - 90, 230, stroke=0, fill=1)
    c.setFillColor(MINT); c.circle(SW - 40, 40, 150, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont(FB, 52); c.drawString(60, 300, "Aris Mansor")
    c.drawString(60, 242, "Sofiyan")
    c.setFillColor(SLATE); c.setFont(FM, 22); c.drawString(60, 195, "Financial Analyst")
    c.setFont(F, 14); c.drawString(60, 160, "Valuation, forecasting and risk  |  Kuala Lumpur, Malaysia")
    c.setFillColor(INK); c.setFont(F, 13); c.drawString(60, 70, LI_TXT)
    c.linkURL(LI_URL, (60, 62, 250, 84), relative=0); c.showPage()

    # 2 profile + numbers
    base(2, "Profile")
    wrap(c, SUMMARY, 60, 390, 470, F, 16, INK, 24)
    stats = [("$240M", "Assets covered in models", LAV), ("38", "Valuations delivered", MINT),
             ("6 yrs", "In audit and corporate finance", PEACH), ("CFA L3", "Candidate, 2026", BLUE)]
    for i, (v, l, col) in enumerate(stats):
        x, y = 590 + (i % 2) * 160, 270 - (i // 2) * 150
        c.setFillColor(col); c.roundRect(x, y, 145, 135, 12, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont(FB, 28); c.drawString(x + 14, y + 80, v)
        wrap(c, l, x + 14, y + 55, 120, F, 11.5, INK, 15)
    c.showPage()

    # 3 experience timeline
    base(3, "Experience")
    cols = [BLUE, LAV, MINT]
    for i, (t, co, yrs, bl) in enumerate(JOBS):
        y = 385 - i * 118
        c.setFillColor(cols[i]); c.roundRect(60, y - 78, 150, 96, 10, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont(FB, 14); c.drawString(74, y - 8, yrs)
        c.setFont(F, 12); c.drawString(74, y - 28, co)
        c.setFont(FB, 16); c.drawString(235, y, t)
        yy = y - 22
        for b in bl[:3]:
            yy = wrap(c, "•  " + b, 235, yy, 660, F, 12, INK, 16)
    c.showPage()

    # 4 selected work
    base(4, "Selected work")
    for i, (t, d, r) in enumerate(PROJECTS):
        x = 60 + i * 285
        c.setFillColor(GREY); c.roundRect(x, 170, 265, 240, 12, stroke=0, fill=1)
        c.setFillColor([BLUE, LAV, MINT][i]); c.roundRect(x, 390, 265, 20, 10, stroke=0, fill=1)
        c.rect(x, 390, 265, 10, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont(FB, 18); y = 360
        for ln in simpleSplit(t, FB, 18, 235):
            c.drawString(x + 18, y, ln); y -= 24
        y = wrap(c, d, x + 18, y - 6, 230, F, 12.5, SLATE, 18)
        wrap(c, "Result: " + r, x + 18, y - 14, 230, FM, 13, INK, 18)
    c.showPage()

    # 5 skills + education
    base(5, "Skills and education")
    x, y = 60, 395
    for sk in SKILLS:
        w = pdfmetrics.stringWidth(sk, FM, 13) + 28
        if x + w > 560: x, y = 60, y - 46
        c.setFillColor([BLUE, LAV, MINT, PEACH][SKILLS.index(sk) % 4]); c.roundRect(x, y - 8, w, 32, 16, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont(FM, 13); c.drawString(x + 14, y + 3, sk); x += w + 10
    c.setFillColor(INK); c.setFont(FB, 15); c.drawString(620, 395, "Education")
    c.setFont(FM, 13); c.drawString(620, 370, EDU[0]); c.setFillColor(SLATE); c.setFont(F, 12); c.drawString(620, 352, EDU[1])
    c.setFillColor(INK); c.setFont(FB, 15); c.drawString(620, 300, "Certifications")
    c.setFont(F, 13)
    for i, t in enumerate(CERTS): c.drawString(620, 276 - i * 20, t)
    c.setFont(FB, 15); c.drawString(620, 215, "Languages")
    c.setFont(F, 13)
    for i, t in enumerate(LANGS): c.drawString(620, 191 - i * 20, t)
    c.showPage()

    # 6 contact
    c.setFillColor(LAV); c.rect(0, 0, SW, SH, stroke=0, fill=1)
    c.setFillColor(BLUE); c.circle(120, 40, 200, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont(FB, 40); c.drawString(60, 330, "Let's talk about your numbers")
    c.setFont(F, 16); c.setFillColor(SLATE)
    c.drawString(60, 285, "Open to senior analyst and consulting roles.")
    c.setFillColor(INK); c.setFont(FM, 18)
    c.drawString(60, 220, EMAIL); c.drawString(60, 188, LI_TXT); c.drawString(60, 156, CITY)
    c.linkURL(LI_URL, (60, 180, 300, 206), relative=0)
    c.showPage(); c.save()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); cv(); slides(); print("PDFs written to", OUT, "| font:", F)
