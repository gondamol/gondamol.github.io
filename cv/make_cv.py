from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, Table, TableStyle, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
import os

INK   = colors.HexColor('#1A1A18')
TERRA = colors.HexColor('#B84E16')
WARM  = colors.HexColor('#F0EBE1')
MUTED = colors.HexColor('#6B6560')
BORD  = colors.HexColor('#D8D2C8')
WHITE = colors.white

W, H = A4
ML = 18*mm; MR = 18*mm; MT = 14*mm; MB = 14*mm

OUT = '/home/gondamol/portfolio/gondamol.github.io/cv/Nichodemus_Amollo_CV.pdf'

doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)

def s(name, **k): return ParagraphStyle(name, **k)

NAME    = s('N', fontName='Helvetica-Bold', fontSize=24, textColor=INK,
            spaceAfter=2, leading=28)
TITL    = s('T', fontName='Helvetica', fontSize=9.5, textColor=TERRA,
            spaceAfter=1, leading=13)
CONT    = s('C', fontName='Helvetica', fontSize=8.5, textColor=MUTED,
            spaceAfter=0, leading=12)
SHEAD   = s('SH', fontName='Helvetica-Bold', fontSize=7, textColor=TERRA,
            spaceBefore=12, spaceAfter=3, leading=9, letterSpacing=1.8)
ROLE    = s('R', fontName='Helvetica-Bold', fontSize=9.5, textColor=INK,
            spaceBefore=5, spaceAfter=1, leading=12)
ORG     = s('O', fontName='Helvetica-Oblique', fontSize=8.5, textColor=MUTED,
            spaceAfter=1, leading=11)
PER     = s('P', fontName='Helvetica', fontSize=8, textColor=TERRA,
            spaceAfter=3, leading=10)
BODY    = s('B', fontName='Helvetica', fontSize=8.5, textColor=INK,
            spaceAfter=2, leading=12, alignment=TA_JUSTIFY, firstLineIndent=0)
BULL    = s('BU', fontName='Helvetica', fontSize=8.5, textColor=INK,
            spaceAfter=2, leading=12, leftIndent=10)
SCAT    = s('SC', fontName='Helvetica-Bold', fontSize=8.5, textColor=INK,
            spaceAfter=1, leading=11)
SVAL    = s('SV', fontName='Helvetica', fontSize=8.5, textColor=INK,
            spaceAfter=4, leading=12)
PUB     = s('PU', fontName='Helvetica', fontSize=8.5, textColor=INK,
            spaceAfter=4, leading=12, leftIndent=12, firstLineIndent=-12,
            alignment=TA_JUSTIFY)

def rule(c=BORD, t=0.5):
    return HRFlowable(width='100%', thickness=t, color=c,
                      spaceAfter=5, spaceBefore=0)

def sec(title):
    return [Spacer(1,3),
            Paragraph(title, SHEAD),
            rule(TERRA, 1.2)]

def job(role, org, period, bullets):
    rows = [Paragraph(role, ROLE),
            Paragraph(org, ORG),
            Paragraph(period, PER)]
    for b in bullets:
        rows.append(Paragraph(f'\u2022\u2002{b}', BULL))
    return KeepTogether(rows)

CW = W - ML - MR

story = []

# Header
story.append(Paragraph('NICHODEMUS WERRE AMOLLO', NAME))
story.append(Paragraph(
    'Research Data Manager\u2002\u00b7\u2002Biostatistician\u2002\u00b7\u2002MEL Specialist',
    TITL))
story.append(Spacer(1, 3))
story.append(Paragraph(
    'Nairobi, Kenya\u2002\u00b7\u2002+254 725 737 867\u2002\u00b7\u2002'
    'nichodemuswerre@gmail.com\u2002\u00b7\u2002gondamol.github.io\u2002\u00b7\u2002'
    'linkedin.com/in/nichodemusamollo',
    CONT))
story.append(rule(TERRA, 1.5))

# Profile
story += sec('PROFESSIONAL PROFILE')
story.append(Paragraph(
    'Research data and analytics professional with 8+ years of experience delivering '
    'end to end data systems for public health and development programmes across East Africa. '
    'I lead multi country workflows spanning instrument design, field quality assurance, '
    'statistical modelling, dashboard delivery, and evidence synthesis for funders, '
    'ministries, and research teams. Expert in biostatistical methods, impact evaluation, '
    'and translating complex findings into decisions that reach communities.',
    BODY))

# Experience
story += sec('PROFESSIONAL EXPERIENCE')

story.append(job(
    'Lead Biostatistician and Research Data Manager',
    'Georgetown University gui2de \u00b7 East Africa (Kenya, Uganda, Tanzania, Rwanda) \u00b7 Remote',
    'April 2025 \u2013 Present',
    [
        'Lead statistical and data systems work across 15+ field sites for multi country health '
        'and evaluation programmes including the Health Financial Diaries initiative.',
        'Develop statistical analysis plans and conduct multivariable regression, survival '
        'analysis, and longitudinal data analysis using R and Stata.',
        'Design and maintain automated reporting pipelines, stakeholder dashboards, and '
        'high frequency check systems reducing reporting turnaround from weekly to daily.',
        'Recruit, train, and mentor 20+ research professionals on reproducible workflows '
        'and applied biostatistics.',
        'Coordinate technical workflows for RCT support, high frequency financial diaries, '
        'and policy reporting to USAID and Gates Foundation.',
    ]
))

story.append(job(
    'Senior Statistician and Data Systems Lead',
    'Kenya Medical Research Institute (KEMRI) \u00b7 Nairobi and Kisumu',
    'April 2023 \u2013 March 2025',
    [
        'Provided statistical leadership for infectious disease surveillance, rural health '
        'research, and cancer epidemiology studies.',
        'Designed regression models, survival analyses, and forecasting systems integrating '
        'DHIS2 data with rainfall and market indicators, reducing alert lag from 2 weeks to 3 days.',
        'Built end to end data pipelines integrating health data from 15+ facilities using '
        'SQL and Python ETL processes.',
        'Delivered 8+ interactive Power BI dashboards reducing ad hoc reporting by 60% '
        'and contributed to peer reviewed publications.',
    ]
))

story.append(job(
    'Senior Research Data Manager and Evaluation Lead',
    'JOOUST and VLIR UOS Regional Programme \u00b7 Kenya, Uganda, Rwanda',
    'November 2021 \u2013 April 2023',
    [
        'Managed cross country evaluation datasets for a multi country RCT covering '
        '8,000+ observations across three countries.',
        'Built SQL based infrastructure consolidating 50+ data sources enabling integrated '
        'analysis and predictive reporting.',
        'Supported randomised and quasi experimental analysis including DiD, propensity '
        'score matching, and ANCOVA estimations.',
        'Managed budgets of USD 500,000+ and trained 30+ enumerators achieving error '
        'rates below 2%.',
    ]
))

story.append(job(
    'Data Analyst and MEL Specialist',
    'LERIS Hub \u00b7 Kenya and Uganda',
    'September 2017 \u2013 November 2021',
    [
        'Designed monitoring frameworks, managed field data systems, and produced policy '
        'and donor reporting for health and livelihoods programmes.',
        'Applied causal inference including propensity score matching and regression '
        'discontinuity in non randomised settings.',
        'Supervised data collection teams in two countries using ODK and KoboToolbox '
        'and produced 8+ research briefs adopted by government partners.',
    ]
))

story.append(job(
    'Data Systems Analyst',
    'Lake Region Community Development Initiative \u00b7 Western Kenya',
    'May 2016 \u2013 August 2017',
    [
        'Implemented digital data capture and reporting workflows for community programmes.',
        'Conducted statistical summaries and operational reporting for county stakeholders.',
    ]
))

# Consultancy
story += sec('CONSULTANCY EXPERIENCE')

consults = [
    ('Technical Lead', 'Global Fund PMTCT Effectiveness Study, 2024',
     'Designed study protocol and statistical framework. Led analysis and interpretation. '
     'Supported ethics submission and donor reporting.'),
    ('Lead Consultant', 'RAS Uptake Study, Dalberg and MMV, 2024',
     'Conducted quantitative and qualitative analysis. Delivered final analytical '
     'report used for strategic decision making.'),
    ('MEL Consultant', 'Community Health Dashboards, NEPHAK, 2023',
     'Developed automated analytical dashboards and supported indicator development '
     'and monitoring systems.'),
]
for role, org, desc in consults:
    story.append(Paragraph(f'<b>{role}</b>  \u00b7  {org}', ROLE))
    story.append(Paragraph(desc, BODY))
    story.append(Spacer(1, 3))

# Education
story += sec('EDUCATION')

edu = [
    ('MSc, Epidemiology and Biostatistics (In Progress)',
     'Jaramogi Oginga Odinga University of Science and Technology (JOOUST) \u00b7 Expected 2026',
     'Thesis: Financial Determinants of Effective Hypertension and Diabetes Care in '
     'Rural Primary Health Facilities, Kisumu County. Mixed methods design with '
     '30+ facilities and 500+ participants.'),
    ('BSc, Statistics \u2013 Second Class Upper Division',
     'University of Nairobi \u00b7 2016', ''),
]
for role, org, detail in edu:
    story.append(Paragraph(role, ROLE))
    story.append(Paragraph(org, ORG))
    if detail:
        story.append(Paragraph(detail, BODY))
    story.append(Spacer(1, 4))

story.append(Paragraph('Selected Certifications', ROLE))
certs = [
    'Monitoring and Evaluation in Global Health \u2013 University of Washington',
    'Economic Evaluation \u2013 University of Washington',
    'Biomedical Research Ethics \u2013 CITI Programme (2024)',
    'Research Methodology and Quantitative Methods \u2013 Johns Hopkins Bloomberg School of Public Health',
    'AWS Certified Cloud Practitioner (2022)',
    'Google Data Analytics Professional Certificate',
    'Advanced R and Data Science Professional Certificate \u2013 DataCamp',
]
for c in certs:
    story.append(Paragraph(f'\u2022\u2002{c}', BULL))

# Skills table
story += sec('TECHNICAL SKILLS')

skills = [
    ('Statistical and Analytical', 'R (Advanced), Python, Stata, SPSS, SAS, Excel (Advanced)'),
    ('Data Engineering', 'SQL, PostgreSQL, ETL pipelines, BigQuery, GCP, API workflows'),
    ('Data Collection', 'KoboToolbox, ODK, SurveyCTO, REDCap, CommCare, DHIS2/KHIS'),
    ('Visualisation and BI', 'ggplot2, Plotly, Power BI, Tableau, R Shiny, Quarto'),
    ('Evaluation Methods', 'RCT design, DiD, PSM, RDD, longitudinal analysis, survival analysis'),
    ('Field Operations', 'Survey design, HFC, enumerator training, CAPI implementation'),
    ('Other', 'Git, GitHub, LaTeX, Quarto, reproducible research workflows'),
]
tdata = [[Paragraph(f'<b>{k}</b>', SCAT), Paragraph(v, SVAL)] for k, v in skills]
tbl = Table(tdata, colWidths=[CW*0.28, CW*0.72])
tbl.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING',  (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING',   (0,0), (-1,-1), 2),
    ('BOTTOMPADDING',(0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS',(0,0),(-1,-1),[WHITE, WARM]),
]))
story.append(tbl)

# Publications
story += sec('SELECTED PUBLICATIONS')
pubs = [
    'Amollo, N. W., Ogol, J., Museve, E., Owenga, J. A., Aduda, D. O., and Onguru, D. (2025). '
    'Financial Determinants of Effective Hypertension and Diabetes Care in Rural Primary Health '
    'Facilities in Kisumu, Kenya: A Mixed Methods Study.',
    'Mangale, D. I., Adhiambo, H., Adagi, P. A., Nyandieka, E., Amollo, N. W., et al. (2025). '
    'Characteristics and mortality risk among esophageal cancer patients with varied HIV status '
    'seeking care in western Kenya: A 10 year analysis.',
    'Odeny, T. A., Adhiambo, H. F., Mangale, D. I., Were, N. A., Nyandieka, E., Amollo, N. W., '
    'et al. (2025). Survival disparities in cervical cancer patients with and without HIV at JOOTRH.',
    'Ouma, O. J., Omondi, D., Akinyi, I., Amollo, N. W., Ogutu, S., Obinge, E., and van Olmen, J. '
    '(2025). Addressing priority gaps in access and quality of NCD services in primary care '
    'settings in rural Kenya.',
]
for i, p in enumerate(pubs, 1):
    story.append(Paragraph(f'{i}.\u2002{p}', PUB))

# Languages and referees
story += sec('LANGUAGES AND REFEREES')
lr = [[
    Paragraph('<b>Languages</b><br/>English (fluent)\u2002\u00b7\u2002'
              'Kiswahili (fluent)\u2002\u00b7\u2002Dholuo (native)', SVAL),
    Paragraph(
        '<b>Referees</b><br/>'
        'Japheth Ogol \u00b7 JOOUST \u00b7 japheth.ogol@ejooust.ac.ke<br/>'
        'Erick Owino \u00b7 LERIS Hub \u00b7 eowino@lerishub.com<br/>'
        'Catherine Koech \u00b7 Georgetown University \u00b7 ck1256@georgetown.edu',
        SVAL),
]]
lt = Table(lr, colWidths=[CW*0.35, CW*0.65])
lt.setStyle(TableStyle([
    ('VALIGN',       (0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',  (0,0),(-1,-1),0),
    ('RIGHTPADDING', (0,0),(-1,-1),8),
    ('TOPPADDING',   (0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
]))
story.append(lt)

doc.build(story)
import os
print(f'PDF created: {OUT}  ({os.path.getsize(OUT)//1024} KB)')
