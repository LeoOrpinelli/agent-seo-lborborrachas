# -*- coding: utf-8 -*-
"""
Gerador de PDF - Analise Comparativa de Concorrentes SEO
Lbor Borrachas vs Elastim, Cambuci, Roma Borracha, UNITEC
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

OUTPUT = "c:/Users/L\u00e9o/Agent_SEO/COMPARATIVO-CONCORRENTES-LBOR.pdf"

# ── Cores ──────────────────────────────────────────────────────────────────
AZUL_ESCURO   = HexColor("#1a2744")
AZUL_MEDIO    = HexColor("#2563eb")
AZUL_CLARO    = HexColor("#dbeafe")
VERDE         = HexColor("#16a34a")
VERDE_CLARO   = HexColor("#dcfce7")
AMARELO       = HexColor("#d97706")
AMARELO_CLARO = HexColor("#fef9c3")
VERMELHO      = HexColor("#dc2626")
VERMELHO_CLARO= HexColor("#fee2e2")
LARANJA       = HexColor("#ea580c")
LARANJA_CLARO = HexColor("#ffedd5")
CINZA_ESCURO  = HexColor("#374151")
CINZA_MEDIO   = HexColor("#6b7280")
CINZA_CLARO   = HexColor("#f3f4f6")
CINZA_BORDA   = HexColor("#d1d5db")
ROXO          = HexColor("#7c3aed")
ROXO_CLARO    = HexColor("#ede9fe")

# Cor de destaque por empresa
COR_LBOR    = HexColor("#2563eb")
COR_ELASTIM = HexColor("#0891b2")
COR_CAMBUCI = HexColor("#7c3aed")
COR_ROMA    = HexColor("#16a34a")
COR_UNITEC  = HexColor("#d97706")

W, H = A4

# ── Estilos ────────────────────────────────────────────────────────────────
def estilo(nome, **kw):
    return ParagraphStyle(nome, **kw)

H1 = estilo("H1", fontName="Helvetica-Bold", fontSize=16, textColor=AZUL_ESCURO,
            spaceBefore=18, spaceAfter=6, leading=20)
H2 = estilo("H2", fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_MEDIO,
            spaceBefore=12, spaceAfter=4, leading=15)
H3 = estilo("H3", fontName="Helvetica-Bold", fontSize=10, textColor=CINZA_ESCURO,
            spaceBefore=8, spaceAfter=3, leading=13)
BODY = estilo("Body", fontName="Helvetica", fontSize=9, textColor=CINZA_ESCURO,
              leading=13, spaceAfter=4)
BODY_BOLD = estilo("BodyBold", fontName="Helvetica-Bold", fontSize=9,
                   textColor=CINZA_ESCURO, leading=13, spaceAfter=4)
NOTA = estilo("Nota", fontName="Helvetica-Oblique", fontSize=8,
              textColor=CINZA_MEDIO, leading=11, spaceAfter=4)
TBL_HDR = estilo("TblHdr", fontName="Helvetica-Bold", fontSize=8,
                 textColor=white, alignment=TA_LEFT, leading=11)
TBL_HDR_C = estilo("TblHdrC", fontName="Helvetica-Bold", fontSize=8,
                   textColor=white, alignment=TA_CENTER, leading=11)
TBL_BODY = estilo("TblBody", fontName="Helvetica", fontSize=8,
                  textColor=CINZA_ESCURO, leading=11)
TBL_BODY_C = estilo("TblBodyC", fontName="Helvetica", fontSize=8,
                    textColor=CINZA_ESCURO, alignment=TA_CENTER, leading=11)
TBL_BODY_BOLD = estilo("TblBodyBold", fontName="Helvetica-Bold", fontSize=8,
                       textColor=CINZA_ESCURO, leading=11)
TBL_LBOR = estilo("TblLbor", fontName="Helvetica-Bold", fontSize=8,
                  textColor=COR_LBOR, leading=11)

def esc(txt):
    return str(txt).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def hr(color=CINZA_BORDA, thickness=0.5, spaceB=4, spaceA=4):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=spaceA, spaceBefore=spaceB)

def sp(h=6):
    return Spacer(1, h)

def p(txt, style=BODY):
    return Paragraph(txt, style)

def tbl_base_style(hdr_color=AZUL_ESCURO):
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), hdr_color),
        ("TEXTCOLOR",     (0,0), (-1,0), white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 5),
        ("TOPPADDING",    (0,0), (-1,0), 5),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 8),
        ("TOPPADDING",    (0,1), (-1,-1), 4),
        ("BOTTOMPADDING", (0,1), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [white, CINZA_CLARO]),
        ("GRID",          (0,0), (-1,-1), 0.4, CINZA_BORDA),
        ("BOX",           (0,0), (-1,-1), 0.6, CINZA_BORDA),
    ])

def secao(titulo, story):
    story.append(sp(8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_MEDIO,
                            spaceAfter=0, spaceBefore=0))
    story.append(sp(4))
    story.append(p(titulo, H1))
    story.append(sp(2))


# ── Score bar (visual) ──────────────────────────────────────────────────────
def score_row(empresa, score, cor, max_w=11*cm):
    """Retorna uma mini-tabela com barra de progresso para o score."""
    pct = score / 100.0
    bar_filled = max_w * pct
    bar_empty  = max_w * (1 - pct)

    cor_score = VERDE if score >= 60 else (AMARELO if score >= 45 else VERMELHO)

    filled_tbl = Table([[""]], colWidths=[bar_filled], rowHeights=[14])
    filled_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),cor),
                                    ("BOX",(0,0),(-1,-1),0,white)]))
    empty_tbl = Table([[""]], colWidths=[bar_empty], rowHeights=[14])
    empty_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CINZA_CLARO),
                                   ("BOX",(0,0),(-1,-1),0,white)]))

    return Table([[
        Paragraph(f"<b>{esc(empresa)}</b>",
                  estilo(f"emp_{empresa}", fontName="Helvetica-Bold", fontSize=9,
                         textColor=cor, leading=12)),
        Table([[filled_tbl, empty_tbl]], colWidths=[bar_filled, bar_empty]),
        Paragraph(f"<font color='#{cor_score.hexval()[2:]}'><b>{score}/100</b></font>",
                  estilo(f"sc_{empresa}", fontName="Helvetica-Bold", fontSize=11,
                         textColor=cor_score, alignment=TA_CENTER, leading=14)),
    ]], colWidths=[3.5*cm, max_w + 0.2*cm, 2.3*cm])


def sim_nao(val, positivo=True):
    """Celula colorida Sim/Nao."""
    if val is True or val == "SIM":
        return Paragraph("<font color='#16a34a'><b>SIM</b></font>", TBL_BODY_C)
    if val is False or val == "NAO":
        return Paragraph("<font color='#dc2626'><b>NAO</b></font>", TBL_BODY_C)
    if val == "PARCIAL":
        return Paragraph("<font color='#d97706'><b>PARCIAL</b></font>", TBL_BODY_C)
    return Paragraph(esc(str(val)), TBL_BODY_C)


# ─── DADOS DOS CONCORRENTES ──────────────────────────────────────────────────
EMPRESAS = {
    "lbor":    {"nome": "Lbor Borrachas",    "url": "lborborrachas.com.br",    "cor": COR_LBOR},
    "elastim": {"nome": "Elastim",           "url": "elastim.com.br",          "cor": COR_ELASTIM},
    "cambuci": {"nome": "Borrachas Cambuci", "url": "borrachascambuci.com.br", "cor": COR_CAMBUCI},
    "roma":    {"nome": "Roma Borracha",     "url": "romaborracha.com.br",      "cor": COR_ROMA},
    "unitec":  {"nome": "UNITEC Borrachas",  "url": "unitecborrachas.com.br",   "cor": COR_UNITEC},
}

SCORES = {
    "lbor":    {"total": 39, "tecnico": 54, "conteudo": 38, "onpage": 30,
                "schema": 31, "cwv": 44, "geo": 31, "imagens": 35},
    "elastim": {"total": 48, "tecnico": 52, "conteudo": 55, "onpage": 52,
                "schema": 30, "cwv": 50, "geo": 28, "imagens": 60},
    "cambuci": {"total": 36, "tecnico": 38, "conteudo": 42, "onpage": 28,
                "schema": 45, "cwv": 35, "geo": 30, "imagens": 30},
    "roma":    {"total": 67, "tecnico": 72, "conteudo": 75, "onpage": 68,
                "schema": 70, "cwv": 60, "geo": 45, "imagens": 50},
    "unitec":  {"total": 45, "tecnico": 55, "conteudo": 40, "onpage": 45,
                "schema": 42, "cwv": 55, "geo": 32, "imagens": 45},
}


def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Comparativo SEO - Lbor Borrachas vs Concorrentes",
        author="Claude SEO Audit System",
    )
    story = []

    # ═══════════════════════════════════════════════════════════════════════
    # CAPA
    # ═══════════════════════════════════════════════════════════════════════
    capa = Table([[
        Paragraph(
            "<font size=24><b>Analise Comparativa de Concorrentes</b></font><br/><br/>"
            "<font size=12 color='#bfdbfe'>Borracha Industrial — SEO Benchmarking</font><br/><br/>"
            "<font size=10 color='#93c5fd'>Lbor Borrachas vs Elastim, Cambuci, Roma Borracha e UNITEC</font>",
            estilo("Capa", fontName="Helvetica-Bold", fontSize=24, textColor=white,
                   alignment=TA_CENTER, leading=30)
        )
    ]], colWidths=[17*cm])
    capa.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), AZUL_ESCURO),
        ("TOPPADDING",    (0,0),(-1,-1), 50),
        ("BOTTOMPADDING", (0,0),(-1,-1), 50),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
        ("RIGHTPADDING",  (0,0),(-1,-1), 20),
    ]))
    story.append(capa)
    story.append(sp(20))

    meta = [
        ["Data",          "24 de marco de 2026"],
        ["Mercado",       "Borrachas Industriais — Brasil (São Paulo, SP)"],
        ["Sites analisados", "5 (Lbor + 4 concorrentes)"],
        ["Metodologia",   "Crawl ao vivo + analise de SEO on-page, tecnico, schema, conteudo e E-E-A-T"],
        ["Auditor",       "Claude SEO Audit System (claude-sonnet-4-6)"],
    ]
    mt = Table([[Paragraph(r, TBL_BODY_BOLD), Paragraph(v, TBL_BODY)] for r,v in meta],
               colWidths=[4*cm, 13*cm])
    mt.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[CINZA_CLARO, white]),
        ("BOX",(0,0),(-1,-1),0.6,CINZA_BORDA),
        ("GRID",(0,0),(-1,-1),0.4,CINZA_BORDA),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    story.append(mt)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 1. RANKING GERAL
    # ═══════════════════════════════════════════════════════════════════════
    secao("1. Ranking Geral de Saude SEO", story)
    story.append(p(
        "Pontuacao calculada com os mesmos pesos utilizados na auditoria original da Lbor: "
        "SEO Tecnico 22% | Conteudo/E-E-A-T 23% | On-Page 20% | Schema 10% | "
        "Performance 10% | GEO/IA 10% | Imagens 5%.", NOTA))
    story.append(sp(8))

    ranking = sorted(SCORES.items(), key=lambda x: x[1]["total"], reverse=True)
    posicao = {k: i+1 for i,(k,_) in enumerate(ranking)}

    for k, sc in ranking:
        e = EMPRESAS[k]
        pos = posicao[k]
        destaque = k == "lbor"
        row = score_row(
            f"{pos}. {e['nome']} ({e['url']})",
            sc["total"], e["cor"]
        )
        row.setStyle(TableStyle([
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 4),
            ("BOX",           (0,0),(-1,-1), 1.5 if destaque else 0.4,
             COR_LBOR if destaque else CINZA_BORDA),
            ("BACKGROUND",    (0,0),(-1,-1),
             AZUL_CLARO if destaque else white),
        ]))
        story.append(row)
        story.append(sp(4))

    story.append(sp(8))
    story.append(p(
        "<b>Posicao da Lbor: 4a de 5</b> — A Lbor esta acima apenas da Borrachas Cambuci, "
        "que possui as mesmas limitacoes de plataforma (AngularJS) e ausencia de endereco fisico. "
        "O maior diferencial competitivo da Lbor e o tamanho do catalogo (230+ produtos vs "
        "4-16 categorias dos concorrentes). O maior gap e de conteudo, endereco e E-E-A-T.",
        BODY))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 2. COMPARATIVO POR CATEGORIA
    # ═══════════════════════════════════════════════════════════════════════
    secao("2. Comparativo por Categoria SEO", story)

    cats = ["SEO Tecnico", "Conteudo/E-E-A-T", "On-Page SEO", "Schema",
            "Performance", "GEO/IA", "Imagens"]
    keys = ["tecnico", "conteudo", "onpage", "schema", "cwv", "geo", "imagens"]
    pesos = [22, 23, 20, 10, 10, 10, 5]

    ordem = ["lbor", "elastim", "cambuci", "roma", "unitec"]
    nomes_curtos = {"lbor":"Lbor","elastim":"Elastim","cambuci":"Cambuci",
                    "roma":"Roma","unitec":"UNITEC"}

    def cor_score(s):
        if s >= 65: return "#16a34a"
        if s >= 50: return "#d97706"
        return "#dc2626"

    hdr = [Paragraph("Categoria", TBL_HDR), Paragraph("Peso", TBL_HDR_C)]
    for k in ordem:
        cor = "#2563eb" if k=="lbor" else "#ffffff"
        hdr.append(Paragraph(
            f"<font color='#{EMPRESAS[k]['cor'].hexval()[2:]}'><b>{nomes_curtos[k]}</b></font>",
            TBL_HDR_C))

    cat_rows = [hdr]
    for cat, key, peso in zip(cats, keys, pesos):
        row = [Paragraph(cat, TBL_BODY_BOLD), Paragraph(f"{peso}%", TBL_BODY_C)]
        for k in ordem:
            s = SCORES[k][key]
            row.append(Paragraph(
                f"<font color='{cor_score(s)}'><b>{s}</b></font>", TBL_BODY_C))
        cat_rows.append(row)

    # Total
    tot_row = [Paragraph("<b>TOTAL PONDERADO</b>", TBL_BODY_BOLD),
               Paragraph("<b>100%</b>", TBL_BODY_C)]
    for k in ordem:
        s = SCORES[k]["total"]
        tot_row.append(Paragraph(
            f"<font color='{cor_score(s)}'><b>{s}</b></font>", TBL_BODY_C))
    cat_rows.append(tot_row)

    cat_tbl = Table(cat_rows, colWidths=[4.5*cm, 1.5*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm])
    cat_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
        ("BACKGROUND",    (0,-1),(-1,-1),AZUL_ESCURO),
        ("TEXTCOLOR",     (0,-1),(-1,-1), white),
        ("FONTNAME",      (0,-1),(-1,-1),"Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1), (-1,-2),[white, CINZA_CLARO]),
        ("GRID",          (0,0), (-1,-1), 0.4, CINZA_BORDA),
        ("BOX",           (0,0), (-1,-1), 0.6, CINZA_BORDA),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (1,0), (-1,-1), "CENTER"),
        # Destaque coluna Lbor (index 2)
        ("BACKGROUND",    (2,1), (2,-2), AZUL_CLARO),
        ("FONTNAME",      (2,0), (2,-1), "Helvetica-Bold"),
    ]))
    story.append(cat_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 3. COMPARATIVO DETALHADO — SINAIS ON-PAGE
    # ═══════════════════════════════════════════════════════════════════════
    secao("3. Comparativo Detalhado — Sinais On-Page e Tecnico", story)

    def cmp_tbl(titulo, rows, col_w=None):
        if col_w is None:
            col_w = [5*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.4*cm]
        hdr_row = [Paragraph(titulo, TBL_HDR)]
        for k in ordem:
            hdr_row.append(Paragraph(nomes_curtos[k], TBL_HDR_C))
        data = [hdr_row]
        for row in rows:
            data.append([Paragraph(esc(row[0]), TBL_BODY_BOLD)] +
                        [sim_nao(v) for v in row[1:]])
        t = Table(data, colWidths=col_w)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), AZUL_ESCURO),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[white, CINZA_CLARO]),
            ("GRID",          (0,0),(-1,-1), 0.4, CINZA_BORDA),
            ("BOX",           (0,0),(-1,-1), 0.6, CINZA_BORDA),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            ("BACKGROUND",    (1,1),(1,-1), AZUL_CLARO),  # col Lbor
        ]))
        return t

    # Tabela tecnica
    rows_tec = [
        # sinal           lbor   elastim  cambuci  roma   unitec
        ["HTTPS ativo",    True,  True,    True,    True,  True],
        ["CDN confirmado", True,  "NAO",   "NAO",   "NAO", "NAO"],
        ["Cabecalhos de seguranca (HSTS etc)", "NAO","PARCIAL","NAO","PARCIAL","PARCIAL"],
        ["robots.txt correto",  True,  True,    "NAO",   True,  True],
        ["Sitemap.xml",         True,  True,    "NAO",   True,  True],
        ["Sem cadeia de redirects", "NAO", True, True,  True,  True],
        ["Cache de HTML (CDN edge)", "NAO","NAO","NAO","NAO","NAO"],
        ["Cache assets estaticos 1 ano", "NAO","NAO","NAO","NAO","PARCIAL"],
        ["Platform atualizada (nao EOL)", "NAO","PARCIAL","NAO",True,True],
    ]
    story.append(p("Infraestrutura e Rastreabilidade", H2))
    story.append(cmp_tbl("Sinal", rows_tec))
    story.append(sp(10))

    # Tabela on-page
    rows_op = [
        # sinal           lbor   elastim  cambuci  roma   unitec
        ["Title tag com keyword", "NAO", "NAO", "NAO",  True, True],
        ["Meta description presente", True, True, "NAO", True, "NAO"],
        ["H1 com keyword de produto", "NAO", True, "NAO", True, "NAO"],
        ["H2 headings na homepage",   "NAO", True, "NAO", True, "NAO"],
        ["Breadcrumbs (schema)",      "NAO", "NAO","NAO", True, "NAO"],
        ["Open Graph completo",       "PARCIAL","NAO","NAO",True,"NAO"],
        ["Twitter Cards",             "NAO", "NAO","NAO","PARCIAL","NAO"],
        ["lang=pt-br correto",        True,  True,  True, True,  True],
        ["Viewport meta correto",     True,  True,  True, True,  True],
    ]
    story.append(p("SEO On-Page", H2))
    story.append(cmp_tbl("Sinal", rows_op))
    story.append(sp(10))

    # Tabela schema
    rows_sch = [
        # sinal           lbor   elastim  cambuci  roma   unitec
        ["Organization / LocalBusiness schema", "PARCIAL","PARCIAL",True,True,True],
        ["LocalBusiness (nao apenas Organization)", "NAO","NAO","NAO",True,"NAO"],
        ["WebSite + SearchAction funcional", "NAO","NAO",True,True,True],
        ["BreadcrumbList schema", "NAO","NAO","NAO",True,"NAO"],
        ["Product schema em produtos", "NAO","NAO","NAO","NAO","PARCIAL"],
        ["URLs absolutas no schema/microdata", "NAO","NAO","NAO",True,"PARCIAL"],
        ["@context com https:// (nao http://)", "NAO","NAO","NAO",True,"PARCIAL"],
    ]
    story.append(p("Schema e Dados Estruturados", H2))
    story.append(cmp_tbl("Sinal", rows_sch))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 4. COMPARATIVO E-E-A-T E CONTEUDO
    # ═══════════════════════════════════════════════════════════════════════
    secao("4. Comparativo E-E-A-T e Conteudo", story)

    rows_eeat = [
        # sinal           lbor   elastim  cambuci  roma   unitec
        ["Endereco fisico completo visivel", "NAO", True,  "NAO", True,  "NAO"],
        ["CNPJ publico no site",             "NAO", "NAO", "NAO", True,  "NAO"],
        ["Pagina Quem Somos / Empresa",      "NAO", "PARCIAL","NAO",True, "NAO"],
        ["Anos de experiencia declarados",   "NAO", "NAO", True,  True,  "NAO"],
        ["Certificacoes industriais (ISO etc)","NAO","NAO","NAO", True,  "NAO"],
        ["Equipe nomeada com funcoes",        "NAO", "NAO","NAO", True,  "NAO"],
        ["Mission / Visao / Qualidade",       "NAO", "NAO","NAO", True,  "NAO"],
        ["Blog ativo com artigos",            "NAO", "NAO","NAO","NAO",  "PARCIAL"],
        ["Politica de privacidade (LGPD)",    "NAO", True, "NAO","NAO",  "NAO"],
        ["Redes sociais vinculadas",          "NAO", True, "NAO", True,  "NAO"],
        ["Avaliacoes / reviews visiveis",     "NAO", "NAO","NAO","NAO",  "NAO"],
        ["Capacidade de producao publicada",  "NAO", "NAO","NAO", True,  "NAO"],
        ["Mais de 50 anos de experiencia",    "NAO", "NAO", True, "NAO", "NAO"],
        ["Marketplace (Mercado Livre/Shopee)","NAO", "NAO", True, "NAO", "NAO"],
    ]
    story.append(cmp_tbl("Sinal E-E-A-T", rows_eeat))
    story.append(sp(8))

    # Tabela de conteudo
    rows_cont = [
        # sinal           lbor   elastim  cambuci  roma   unitec
        ["Maior catalogo de produtos (230+)", True, "NAO","NAO","NAO","NAO"],
        ["Descricoes de categoria 600+ palavras","NAO","NAO","NAO","PARCIAL","NAO"],
        ["FAQ em paginas de produto",         "NAO", "NAO","NAO","NAO",  "NAO"],
        ["Tabelas de especificacoes tecnicas","NAO", "NAO","NAO","NAO",  "NAO"],
        ["Conteudo com palavras-chave locais SP","NAO","PARCIAL","NAO","NAO","NAO"],
        ["llms.txt presente",                 "NAO", "NAO","NAO","NAO",  "NAO"],
        ["WhatsApp multi-departamento",        True,  "NAO","PARCIAL","PARCIAL","NAO"],
        ["Formulario de cotacao dedicado",     True,  True, True, True,  "PARCIAL"],
    ]
    story.append(p("Conteudo e Conversao", H2))
    story.append(cmp_tbl("Sinal", rows_cont))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 5. LBOR vs CONCORRENTES — ONDE GANHA E ONDE PERDE
    # ═══════════════════════════════════════════════════════════════════════
    secao("5. Lbor Borrachas — Onde Ganha e Onde Perde", story)

    # VANTAGENS DA LBOR
    story.append(p("Vantagens Competitivas da Lbor", H2))
    story.append(sp(4))

    vantagens = [
        ("Catalogo: 230+ produtos, 42 categorias",
         "Nenhum concorrente chega perto. Elastim tem 14 categorias, Roma tem 4, "
         "Cambuci 16+, UNITEC indeterminado. A amplitude de catalogo da Lbor e seu maior "
         "ativo de SEO — cada produto e uma pagina indexavel com potencial de ranking."),
        ("Infraestrutura CDN: Cloudflare com Brotli + HTTP/3",
         "E o unico dos 5 com CDN confirmado (Cloudflare GRU). Brotli e HTTP/3 disponivel. "
         "Elastim usa PHP custom sem CDN confirmado. Roma e UNITEC usam WordPress sem CDN claro. "
         "Vantagem real de velocidade de entrega para usuarios brasileiros."),
        ("WhatsApp multi-departamento (Vendas, Cobranca, Compras, Faturamento)",
         "O canal de conversao e mais completo que todos os concorrentes. Cambuci e Roma "
         "tem WhatsApp de 2 contatos. Elastim e UNITEC nao tem multi-canal confirmado. "
         "Para B2B, reduzir atrito na comunicacao e um diferencial de conversao real."),
        ("GTM com consent-default-denied (padrao LGPD)",
         "O tracking esta configurado de forma LGPD-compliant, o que e tecnicamente superior "
         "ao que foi observado nos concorrentes. Reduz risco de multa ANPD."),
        ("Alt text em todas as imagens de produto",
         "Acessibilidade e SEO de imagem corretos. Cambuci e UNITEC nao confirmaram. "
         "Diferencial para indexacao de imagens no Google Imagens."),
        ("Sitemap.xml com 303 URLs (maior cobertura)",
         "O sitemap tem mais URLs indexadas que qualquer concorrente identificado, "
         "o que reflete a amplitude do catalogo. Maior superficie de indexacao disponivel."),
    ]

    for titulo, desc in vantagens:
        bloco = Table([[
            Paragraph("&#9650;", estilo("seta", fontName="Helvetica-Bold", fontSize=14,
                      textColor=VERDE, alignment=TA_CENTER)),
            [Paragraph(f"<b>{esc(titulo)}</b>", BODY_BOLD), Paragraph(esc(desc), BODY)]
        ]], colWidths=[0.8*cm, 16.2*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), VERDE_CLARO),
            ("BOX",           (0,0),(-1,-1), 0.6, VERDE),
            ("TOPPADDING",    (0,0),(-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        story.append(bloco)
        story.append(sp(4))

    story.append(sp(8))

    # DESVANTAGENS DA LBOR
    story.append(p("Lacunas Competitivas da Lbor (vs Concorrentes)", H2))
    story.append(sp(4))

    lacunas = [
        ("CRITICO", "Endereco fisico ausente — Lbor e unica sem endereço junto com UNITEC",
         "Elastim publica: Rua Erasmo Braga, 446, Presidente Altino - Osasco/SP. "
         "Roma publica: Rua Paulo Candido da Silva, 53, Laranjeiras, Caieiras/SP. "
         "Sem endereco, a Lbor nao pode rankar no Local Pack do Google Maps, "
         "que e onde a maioria dos compradores B2B industriais busca fornecedores locais."),
        ("CRITICO", "Sem certificacao ISO — Roma tem ISO 9001:2015 desde 2003",
         "Para B2B industrial, ISO 9001 e um criterio de qualificacao de fornecedores "
         "em setores como automotive (FIAT, GM, VW), construcao e alimentos. "
         "Roma usa o badge ISO como diferencial central na homepage. "
         "Lbor nao menciona nenhuma certificacao — isso e uma barreira de conversao em contratos corporativos."),
        ("ALTO", "Sem anos de experiencia declarados — Cambuci: 50 anos, Roma: 33 anos",
         "Cambuci usa 'Mais de 50 anos de experiencia' como headline de confianca. "
         "Roma publica fundacao em 1988 e historico completo. "
         "Lbor nao declara em nenhum lugar ha quantos anos opera — "
         "compradores B2B valorizam longevidade como proxy de confiabilidade."),
        ("ALTO", "Pior title tag do grupo (14 chars, apenas marca)",
         "Ranking dos title tags: UNITEC ('Produtos e Artefatos de Borracha - UNITEC BORRACHAS') "
         "e Roma tem melhores titulos. Elastim tem 'Home - Elastim' (fraco, mas contem a proposicao). "
         "Cambuci e Lbor tem apenas a marca. O title tag e o fator on-page #1 para CTR organico."),
        ("ALTO", "Sem redes sociais — Elastim tem Instagram, Facebook e LinkedIn",
         "Elastim mantém presenca ativa em 3 plataformas sociais, que sao fontes de "
         "brand mention para GEO (citacao por IA) e sinal de autoridade de entidade para Google. "
         "Lbor nao tem nenhum link de rede social visivel no site."),
        ("ALTO", "Schema com 3 bugs criticos — Roma e UNITEC tem schema funcional",
         "Roma tem WebPage + Organization + BreadcrumbList + SearchAction funcionais, "
         "com OG tags configuradas. UNITEC tem Organization + WebSite + WebPage. "
         "O schema da Lbor tem name vazio, SearchAction quebrada e URLs relativas — "
         "desqualificando o site de Sitelinks Searchbox e BreadcrumbList nos SERPs."),
        ("ALTO", "Blog quebrado (HTTP 500) — UNITEC tem estrutura de blog WordPress",
         "UNITEC usa WordPress com estrutura de blog (mesmo sem conteudo confirmado). "
         "Roma tem pagina /empresa com historico extenso. Elastim tem CTAs de consultoria. "
         "O blog da Lbor devolve HTTP 500 — perdendo toda autoridade topica que 30 artigos "
         "poderiam gerar."),
        ("MEDIO", "Sem pagina Quem Somos — Roma tem historia, missao, visao e politica de qualidade",
         "A pagina /empresa da Roma publica: historia desde 1988, relocalizacao em 1997, "
         "certificacoes ISO progressivas, capacidade de 30 tons/mes, area de 1.480m2, "
         "missao, visao e politica de qualidade. Isso e E-E-A-T de nivel enterprise. "
         "A Lbor nao tem nem uma pagina basica sobre a empresa."),
        ("MEDIO", "PHP 7.4.33 EOL — maior risco de seguranca do grupo",
         "Elastim usa PHP custom mas sem versao exposta. Roma e UNITEC estao em WordPress "
         "com updates regulares. A Lbor expoe PHP/7.4.33 (EOL nov/2022) no header X-Powered-By, "
         "anunciando uma vulnerabilidade sem patch. Nenhum outro concorrente faz isso."),
    ]

    sev_bg = {"CRITICO": (VERMELHO_CLARO, VERMELHO),
              "ALTO":    (LARANJA_CLARO,  LARANJA),
              "MEDIO":   (AMARELO_CLARO,  AMARELO)}

    for sev, titulo, desc in lacunas:
        bg, borda = sev_bg.get(sev, (CINZA_CLARO, CINZA_BORDA))
        sev_hex = {"CRITICO":"#dc2626","ALTO":"#ea580c","MEDIO":"#d97706"}
        bloco = Table([[
            [Paragraph(f"<font color='{sev_hex[sev]}'><b>{sev}</b></font>", BODY_BOLD),
             Paragraph(f"<b>{esc(titulo)}</b>", BODY_BOLD),
             Paragraph(esc(desc), BODY)]
        ]], colWidths=[17*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("BOX",           (0,0),(-1,-1), 0.6, borda),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ]))
        story.append(bloco)
        story.append(sp(4))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 6. PERFIL DE CADA CONCORRENTE
    # ═══════════════════════════════════════════════════════════════════════
    secao("6. Perfil Detalhado de Cada Concorrente", story)

    perfis = [
        {
            "nome": "Roma Borracha", "url": "romaborracha.com.br",
            "score": 67, "cor": COR_ROMA, "posicao": "1 lugar",
            "resumo": (
                "O concorrente mais forte do grupo. Fundada em 1988, ISO 9001:2015, "
                "1.480m2 de producao, 30 tons/mes de capacidade, equipe nomeada, "
                "missao/visao publicada e schema completo com BreadcrumbList. "
                "E um fornecedor especializado (4 categorias vs 42 da Lbor) mas "
                "posicionado como referencia tecnica premium."
            ),
            "pontos_fortes": [
                "ISO 9001:2015 — criterio de qualificacao corporativa",
                "33 anos de mercado declarados + historico detalhado",
                "Schema completo: Organization + BreadcrumbList + SearchAction",
                "OG tags e meta description configurados",
                "Equipe nomeada (Flavia e Mayara) — E-E-A-T de experiencia",
                "Missao, Visao e Politica de Qualidade publicados",
                "Endereco completo: Caieiras, SP (CEP 07745-045)",
                "WordPress — plataforma moderna e indexavel",
            ],
            "pontos_fracos": [
                "Catalogo limitado a 4 categorias (vs 230+ produtos da Lbor)",
                "Sem blog ativo identificado",
                "Sem redes sociais confirmadas",
                "Sem politica de privacidade LGPD identificada",
                "llms.txt ausente",
                "Foco muito especializado — menos superficie de indexacao",
            ],
            "ameaca": "ALTA — Compradores B2B que exigem ISO ou buscam 'lencol de borracha "
                      "certificado SP' encontrarao Roma primeiro.",
            "oportunidade": "Lbor supera amplamente em variedade. Uma certificacao ISO e "
                            "uma pagina Quem Somos robusta poderiam eliminar o gap de E-E-A-T.",
        },
        {
            "nome": "Elastim", "url": "elastim.com.br",
            "score": 48, "cor": COR_ELASTIM, "posicao": "2 lugar",
            "resumo": (
                "Segundo colocado. Ponto forte e o H1 com keyword clara, endereco completo "
                "em Osasco/SP, presenca em 3 redes sociais, politica de privacidade e "
                "integracao com Waze/Google Maps. Catalogo de 14 categorias."
            ),
            "pontos_fortes": [
                "H1 excelente: 'Somos Especialistas em Produtos de Borracha'",
                "Endereco completo: Rua Erasmo Braga, 446, Osasco/SP",
                "Horario de atendimento publicado (Seg-Sex 08:00-17:30)",
                "Redes sociais: Instagram, Facebook e LinkedIn",
                "Integracao com Waze e Google Maps",
                "Politica de privacidade presente",
                "WebP para imagens (performance)",
                "W3C validation badges e Google Safe Browsing cert",
            ],
            "pontos_fracos": [
                "Title tag: 'Home - Elastim' (sem keyword de produto)",
                "Schema limitado a WebPage (sem LocalBusiness, BreadcrumbList)",
                "Sem certificacao industrial (ISO, ABNT)",
                "Sem anos de experiencia declarados",
                "Sem blog",
                "OG tags nao confirmados",
                "Sem CDN confirmado",
                "14 categorias vs 42 da Lbor",
            ],
            "ameaca": "MEDIA — Endereco completo e redes sociais dao vantagem local. "
                      "H1 com keyword pode rankear melhor em queries genericas.",
            "oportunidade": "Lbor supera em catalogo e CDN. Adicionar endereco e redes "
                            "sociais colocaria Lbor a frente em SEO local.",
        },
        {
            "nome": "UNITEC Borrachas", "url": "unitecborrachas.com.br",
            "score": 45, "cor": COR_UNITEC, "posicao": "3 lugar",
            "resumo": (
                "Terceiro colocado. Maior vantagem e o title tag com keywords "
                "('Produtos e Artefatos de Borracha - UNITEC BORRACHAS') e a plataforma "
                "WordPress + WooCommerce, moderna e SEO-friendly. Porem muitos sinais "
                "fundamentais estao ausentes ou nao confirmados."
            ),
            "pontos_fortes": [
                "Melhor title tag do grupo: inclui keywords de produto",
                "WordPress + WooCommerce — plataforma moderna e indexavel",
                "Schema: Organization + WebSite + WebPage",
                "Ativo desde 2013 — dominio com 12+ anos de idade",
                "Ultima modificacao: nov/2025 — site ativo",
                "OG image configurada (1536x1024px)",
                "Estrutura de blog WordPress presente",
            ],
            "pontos_fracos": [
                "Sem H1 detectado",
                "Sem meta description",
                "Sem endereco visivel",
                "Sem telefone visivel",
                "Sem Open Graph completo",
                "Sem certificacoes ou anos de experiencia",
                "Sem LGPD / politica de privacidade confirmada",
                "Catalogo nao confirmado em profundidade",
            ],
            "ameaca": "MEDIA — Title tag com keyword pode dar vantagem em rankings gerais. "
                      "WooCommerce permite Product schema escalavel.",
            "oportunidade": "Lbor supera em catalogo confirmado, CDN e WhatsApp. "
                            "Adicionando title tag com keyword, UNITEC ficaria para tras.",
        },
        {
            "nome": "Borrachas Cambuci", "url": "borrachascambuci.com.br",
            "score": 36, "cor": COR_CAMBUCI, "posicao": "5 lugar",
            "resumo": (
                "O concorrente mais proximo da Lbor em termos de problemas — "
                "mesma plataforma (AngularJS), sem endereco fisico, sem CNPJ publico. "
                "Diferencial unico: '50+ anos de experiencia' e presenca no Mercado Livre "
                "e Shopee. Isso cria sinais de confianca e vendas offline que a Lbor nao tem."
            ),
            "pontos_fortes": [
                "'Mais de 50 anos de experiencia' — maior sinal de longevidade do grupo",
                "Presenca no Mercado Livre e Shopee — canal de vendas diversificado",
                "Schema Organization + WebSite + SearchAction presente",
                "Contato por WhatsApp disponivel",
                "16+ categorias de produto",
            ],
            "pontos_fracos": [
                "Mesmo AngularJS + mesmos problemas de EOL que a Lbor",
                "Endereco: variaveis de template nao preenchidas (pior que a Lbor)",
                "CNPJ: nao preenchido no template",
                "H1 nao detectado",
                "Sem meta description",
                "Sem redes sociais confirmadas",
                "Sem blog",
                "WhatsApp apenas (sem telefone fixo)",
            ],
            "ameaca": "BAIXA — Os problemas tecnicos sao iguais ou piores que os da Lbor. "
                      "O '50 anos' e presenca em marketplaces sao os unicos diferenciais reais.",
            "oportunidade": "A Lbor pode superar Cambuci em SEO rapidamente com as correcoes "
                            "da Fase 1. O catalogo da Lbor ja e maior. A Cambuci e o unico "
                            "concorrente que a Lbor pode ultrapassar em 30 dias.",
        },
    ]

    for perfil in perfis:
        cor = perfil["cor"]
        # Header do perfil
        hdr_perfil = Table([[
            Paragraph(
                f"<font color='#ffffff' size=12><b>{esc(perfil['posicao'])} — "
                f"{esc(perfil['nome'])}</b></font><br/>"
                f"<font color='#e0e7ff' size=9>{esc(perfil['url'])} | "
                f"Score: {perfil['score']}/100</font>",
                estilo(f"hp_{perfil['nome']}", fontName="Helvetica-Bold", fontSize=12,
                       textColor=white, leading=16)
            )
        ]], colWidths=[17*cm])
        hdr_perfil.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), cor),
            ("TOPPADDING",    (0,0),(-1,-1), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 10),
            ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ]))
        story.append(hdr_perfil)

        # Resumo
        story.append(Table([[
            Paragraph(esc(perfil["resumo"]), BODY)
        ]], colWidths=[17*cm]))

        # Pontos fortes e fracos lado a lado
        pf_txt = "\n".join([f"+ {esc(x)}" for x in perfil["pontos_fortes"]])
        pp_txt = "\n".join([f"- {esc(x)}" for x in perfil["pontos_fracos"]])

        pf_items = [Paragraph(f"<font color='#16a34a'>+</font> {esc(x)}", BODY)
                    for x in perfil["pontos_fortes"]]
        pp_items = [Paragraph(f"<font color='#dc2626'>-</font> {esc(x)}", BODY)
                    for x in perfil["pontos_fracos"]]

        lado = Table([[
            [Paragraph("<b>Pontos Fortes</b>", H3)] + pf_items,
            [Paragraph("<b>Pontos Fracos</b>", H3)] + pp_items,
        ]], colWidths=[8.5*cm, 8.5*cm])
        lado.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(0,-1), VERDE_CLARO),
            ("BACKGROUND",   (1,0),(1,-1), VERMELHO_CLARO),
            ("BOX",          (0,0),(0,-1), 0.5, VERDE),
            ("BOX",          (1,0),(1,-1), 0.5, VERMELHO),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
            ("RIGHTPADDING", (0,0),(-1,-1), 8),
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ]))
        story.append(lado)

        # Ameaca e oportunidade
        am_op = Table([[
            [Paragraph("<b>Ameaca para Lbor</b>", H3),
             Paragraph(esc(perfil["ameaca"]), BODY)],
            [Paragraph("<b>Oportunidade para Lbor</b>", H3),
             Paragraph(esc(perfil["oportunidade"]), BODY)],
        ]], colWidths=[8.5*cm, 8.5*cm])
        am_op.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(0,-1), LARANJA_CLARO),
            ("BACKGROUND",   (1,0),(1,-1), AZUL_CLARO),
            ("BOX",          (0,0),(0,-1), 0.5, LARANJA),
            ("BOX",          (1,0),(1,-1), 0.5, AZUL_MEDIO),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
            ("RIGHTPADDING", (0,0),(-1,-1), 8),
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ]))
        story.append(am_op)
        story.append(sp(12))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 7. PLANO DE ACAO COMPARATIVO
    # ═══════════════════════════════════════════════════════════════════════
    secao("7. Plano de Acao para Superar os Concorrentes", story)

    story.append(p(
        "Acoes priorizadas especificamente para fechar as lacunas identificadas "
        "vs os concorrentes, em adicao ao Plano de Acao da auditoria original.",
        BODY))
    story.append(sp(8))

    acoes_comp = [
        ("SEMANA 1", "Adicionar endereco fisico (bate Cambuci + emparelha com Elastim e Roma)",
         "Cambuci nao tem endereco (template vazio). Elastim e Roma tem. "
         "Adicionar o endereco completo no rodape da Lbor em 1 hora coloca a Lbor "
         "a frente de Cambuci em SEO local e abre a elegibilidade ao Local Pack, "
         "que nenhum dos concorrentes esta explorando plenamente."),
        ("SEMANA 1", "Reescrever title tag (supera Elastim e Cambuci)",
         "Title sugerido: 'Lbor Borrachas | Manta, Lencol e Perfis de Borracha Industrial'. "
         "Isso supera Elastim ('Home - Elastim') e Cambuci ('Borrachas Cambuci | Vale Amazonico'). "
         "So Roma e UNITEC teriam titles melhores apos a mudanca."),
        ("SEMANA 1", "Corrigir schema (supera Elastim e Cambuci, aproxima de Roma)",
         "Apos as correcoes (https://, name nao vazio, SearchAction funcional, LocalBusiness), "
         "a Lbor teria schema melhor que Elastim e Cambuci, e comparavel ao UNITEC. "
         "So Roma permanece a frente com BreadcrumbList."),
        ("SEMANA 2", "Criar pagina Quem Somos com CNPJ + anos de experiencia (supera Elastim e UNITEC)",
         "Publicar fundacao, CNPJ, historico e capacidade operacional elimina o gap "
         "de E-E-A-T vs Roma e coloca a Lbor a frente de Elastim e UNITEC, que nao tem "
         "essas informacoes detalhadas."),
        ("SEMANA 2", "Adicionar redes sociais (emparelha com Elastim)",
         "Instagram e LinkedIn com perfis ativos coloca a Lbor no mesmo nivel que Elastim "
         "em sinais de autoridade de entidade — que sao usados por Google e IA "
         "para corroborar legitimidade da empresa."),
        ("MES 1", "Buscar certificacao ISO 9001 (supera todos os concorrentes)",
         "Roma e o unico com ISO 9001. Uma certificacao coloca a Lbor em categoria "
         "propria para contratos corporativos no setor automotivo, construcao e industria alimenticia. "
         "Esse e o gap mais dificil de fechar, mas de maior retorno em conversao B2B."),
        ("MES 1", "Restaurar blog e publicar 4 artigos comparativos de materiais (supera todos)",
         "Nenhum concorrente tem blog ativo confirmado. A Lbor tem 30 artigos no subdominio "
         "quebrado. Migrar para /blog/ e publicar guias como 'EPDM vs Neoprene: qual escolher?' "
         "cria um ativo de conteudo que nenhum concorrente tem — vantagem de autoridade topica."),
        ("MES 1", "Ativar page Sao Paulo + Google Business Profile (supera Elastim em local)",
         "Elastim esta em Osasco/SP. Roma em Caieiras/SP. Se a Lbor esta em Sao Paulo, "
         "uma pagina /borrachas-industriais-sao-paulo e um GBP otimizado posicionam a Lbor "
         "como referencia para o mercado principal, superando concorrentes em cidades menores."),
    ]

    for prazo, titulo, desc in acoes_comp:
        cor_prazo = {"SEMANA 1": VERDE, "SEMANA 2": AZUL_MEDIO, "MES 1": AMARELO}.get(prazo, CINZA_MEDIO)
        cor_bg    = {"SEMANA 1": VERDE_CLARO, "SEMANA 2": AZUL_CLARO, "MES 1": AMARELO_CLARO}.get(prazo, CINZA_CLARO)

        bloco = Table([[
            Paragraph(f"<font color='#{cor_prazo.hexval()[2:]}'><b>{prazo}</b></font>",
                      estilo(f"prazo_{prazo}", fontName="Helvetica-Bold", fontSize=9,
                             textColor=cor_prazo, alignment=TA_CENTER, leading=12)),
            [Paragraph(f"<b>{esc(titulo)}</b>", BODY_BOLD),
             Paragraph(esc(desc), BODY)]
        ]], colWidths=[2.2*cm, 14.8*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), cor_bg),
            ("BOX",           (0,0),(-1,-1), 0.6, cor_prazo),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        story.append(bloco)
        story.append(sp(4))

    story.append(sp(12))

    # Projecao de ranking
    story.append(p("Projecao de Ranking Apos Implementacao (3 meses)", H2))
    story.append(sp(4))

    proj = [
        ["Pos.", "Empresa",          "Score Atual", "Score Projetado (3m)", "Principal Fator"],
        ["1",    "Roma Borracha",    "67/100",       "70/100",              "ISO + E-E-A-T forte — dificil de superar"],
        ["2",    "Lbor Borrachas",   "39/100",       "72-79/100",           "+Endereco+Schema+Blog+GBP+Conteudo"],
        ["3",    "UNITEC Borrachas", "45/100",       "52/100",              "WordPress ajuda mas sem conteudo profundo"],
        ["4",    "Elastim",          "48/100",       "50/100",              "Sem investimento SEO novo identificado"],
        ["5",    "Borrachas Cambuci","36/100",        "38/100",              "Mesmos problemas de plataforma, sem acao"],
    ]
    proj_tbl = Table(
        [[Paragraph(c, TBL_HDR_C if i==0 else TBL_BODY_C) for c in row]
         for i, row in enumerate(proj)],
        colWidths=[1*cm, 4*cm, 2.5*cm, 3.5*cm, 6*cm]
    )
    proj_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), AZUL_ESCURO),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[white, CINZA_CLARO]),
        # Destacar linha Lbor (index 2)
        ("BACKGROUND",    (0,2),(-1,2), AZUL_CLARO),
        ("FONTNAME",      (0,2),(-1,2), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,2),(-1,2), COR_LBOR),
        ("GRID",          (0,0),(-1,-1), 0.4, CINZA_BORDA),
        ("BOX",           (0,0),(-1,-1), 0.6, CINZA_BORDA),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,0), 8),
        ("FONTSIZE",      (0,1),(-1,-1),8),
    ]))
    story.append(proj_tbl)
    story.append(sp(8))
    story.append(p(
        "A Lbor tem o maior potencial de crescimento do grupo — pode passar de 4 para 2 lugar "
        "em 3 meses com implementacoes que nao requerem mudanca de plataforma. "
        "O catalogo de 230+ produtos e um ativo de SEO que nenhum concorrente possui; "
        "o que falta e conteudo, endereco e schema para ativa-lo plenamente.",
        BODY))

    # Footer
    story.append(sp(20))
    story.append(HRFlowable(width="100%", thickness=1, color=AZUL_MEDIO,
                            spaceAfter=6, spaceBefore=6))
    story.append(p(
        "Analise Comparativa gerada por Claude SEO Audit System (claude-sonnet-4-6) "
        "em 24 de marco de 2026. Dados coletados por crawl ao vivo de todos os 5 sites "
        "na mesma data. Scores sao estimativas baseadas em analise on-page e nao "
        "incluem dados de backlinks ou posicoes reais de SERP.",
        NOTA))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(CINZA_MEDIO)
        canvas.drawString(2*cm, 1.2*cm,
            "Comparativo SEO — Lbor vs Concorrentes — 24/03/2026")
        canvas.drawRightString(W - 2*cm, 1.2*cm, f"Pagina {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF comparativo gerado: {OUTPUT}")


if __name__ == "__main__":
    build()
