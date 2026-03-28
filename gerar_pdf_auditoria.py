# -*- coding: utf-8 -*-
"""
Gerador de PDF - Auditoria SEO Lbor Borrachas
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.lib import colors

OUTPUT = "c:/Users/L\u00e9o/Agent_SEO/AUDITORIA-SEO-LBORBORRACHAS.pdf"

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

W, H = A4

# ── Estilos ────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def estilo(nome, **kw):
    s = ParagraphStyle(nome, **kw)
    return s

TITULO_CAPA = estilo("TituloCapa",
    fontName="Helvetica-Bold", fontSize=26, textColor=white,
    alignment=TA_CENTER, leading=32)

SUBTITULO_CAPA = estilo("SubtituloCapa",
    fontName="Helvetica", fontSize=13, textColor=HexColor("#bfdbfe"),
    alignment=TA_CENTER, leading=18)

INFO_CAPA = estilo("InfoCapa",
    fontName="Helvetica", fontSize=10, textColor=HexColor("#93c5fd"),
    alignment=TA_CENTER, leading=14)

H1 = estilo("H1",
    fontName="Helvetica-Bold", fontSize=16, textColor=AZUL_ESCURO,
    spaceBefore=18, spaceAfter=6, leading=20,
    borderPad=4)

H2 = estilo("H2",
    fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_MEDIO,
    spaceBefore=12, spaceAfter=4, leading=15)

H3 = estilo("H3",
    fontName="Helvetica-Bold", fontSize=10, textColor=CINZA_ESCURO,
    spaceBefore=8, spaceAfter=3, leading=13)

BODY = estilo("Body",
    fontName="Helvetica", fontSize=9, textColor=CINZA_ESCURO,
    leading=13, spaceAfter=4)

BODY_BOLD = estilo("BodyBold",
    fontName="Helvetica-Bold", fontSize=9, textColor=CINZA_ESCURO,
    leading=13, spaceAfter=4)

LABEL = estilo("Label",
    fontName="Helvetica-Bold", fontSize=8, textColor=CINZA_MEDIO,
    leading=11)

CODE = estilo("Code",
    fontName="Courier", fontSize=8, textColor=HexColor("#1e293b"),
    backColor=CINZA_CLARO, leading=11, leftIndent=8, rightIndent=8,
    spaceBefore=4, spaceAfter=4)

NOTA = estilo("Nota",
    fontName="Helvetica-Oblique", fontSize=8, textColor=CINZA_MEDIO,
    leading=11, spaceAfter=4)

TBL_HDR = estilo("TblHdr",
    fontName="Helvetica-Bold", fontSize=8, textColor=white,
    alignment=TA_LEFT, leading=11)

TBL_BODY = estilo("TblBody",
    fontName="Helvetica", fontSize=8, textColor=CINZA_ESCURO,
    leading=11)

TBL_BODY_BOLD = estilo("TblBodyBold",
    fontName="Helvetica-Bold", fontSize=8, textColor=CINZA_ESCURO,
    leading=11)

# ── Helpers ─────────────────────────────────────────────────────────────────
def hr(color=CINZA_BORDA, thickness=0.5, spaceB=4, spaceA=4):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=spaceA, spaceBefore=spaceB)

def sp(h=6):
    return Spacer(1, h)

def p(txt, style=BODY):
    return Paragraph(txt, style)

def tbl_style(header_color=AZUL_ESCURO, stripe=True, borda=True):
    cmds = [
        ("BACKGROUND", (0,0), (-1,0), header_color),
        ("TEXTCOLOR",  (0,0), (-1,0), white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 5),
        ("TOPPADDING",    (0,0), (-1,0), 5),
        ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",   (0,1), (-1,-1), 8),
        ("TOPPADDING",    (0,1), (-1,-1), 4),
        ("BOTTOMPADDING", (0,1), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ]
    if stripe:
        cmds += [("ROWBACKGROUNDS", (0,1), (-1,-1), [white, CINZA_CLARO])]
    if borda:
        cmds += [
            ("GRID",      (0,0), (-1,-1), 0.4, CINZA_BORDA),
            ("BOX",       (0,0), (-1,-1), 0.6, CINZA_BORDA),
        ]
    return TableStyle(cmds)


class ScoreBox(Flowable):
    """Caixa colorida com pontuacao grande."""
    def __init__(self, score, label, color_bg, color_txt=white, w=120, h=60):
        Flowable.__init__(self)
        self.score = score
        self.label = label
        self.color_bg = color_bg
        self.color_txt = color_txt
        self.w = w
        self.h = h
        self.width  = w
        self.height = h

    def draw(self):
        c = self.canv
        c.setFillColor(self.color_bg)
        c.roundRect(0, 0, self.w, self.h, 6, fill=1, stroke=0)
        # Numero grande
        c.setFillColor(self.color_txt)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(self.w/2, self.h/2 + 6, self.score)
        # Label
        c.setFont("Helvetica", 8)
        c.drawCentredString(self.w/2, self.h/2 - 12, self.label)


class ColorBadge(Flowable):
    """Badge colorido pequeno (CRITICO / ALTO / MEDIO / BAIXO)."""
    COLORS = {
        "CRITICO": (VERMELHO, white),
        "ALTO":    (LARANJA, white),
        "MEDIO":   (AMARELO, HexColor("#1c1917")),
        "BAIXO":   (VERDE, white),
        "PASS":    (VERDE, white),
        "FAIL":    (VERMELHO, white),
        "PARCIAL": (AMARELO, HexColor("#1c1917")),
    }
    def __init__(self, label, w=55, h=14):
        Flowable.__init__(self)
        self.label = label.upper()
        self.w = w
        self.h = h
        self.width  = w
        self.height = h

    def draw(self):
        bg, fg = self.COLORS.get(self.label, (CINZA_MEDIO, white))
        c = self.canv
        c.setFillColor(bg)
        c.roundRect(0, 0, self.w, self.h, 4, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(self.w/2, 3, self.label)


def esc(txt):
    """Escapa < e > em texto puro para nao conflitar com o parser do ReportLab."""
    return txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")



def secao(titulo, story):
    story.append(sp(8))
    story.append(hr(AZUL_MEDIO, 1.5, spaceB=0, spaceA=0))
    story.append(sp(4))
    story.append(p(titulo, H1))
    story.append(sp(2))


def subsecao(titulo, story):
    story.append(p(titulo, H2))


def badge_cell(txt):
    """Celula de tabela com cor de status."""
    mapa = {
        "CRITICO": ("<font color='#dc2626'><b>CRITICO</b></font>", VERMELHO_CLARO),
        "ALTO":    ("<font color='#ea580c'><b>ALTO</b></font>",    LARANJA_CLARO),
        "MEDIO":   ("<font color='#d97706'><b>MEDIO</b></font>",   AMARELO_CLARO),
        "BAIXO":   ("<font color='#16a34a'><b>BAIXO</b></font>",   VERDE_CLARO),
        "PASS":    ("<font color='#16a34a'><b>OK</b></font>",      VERDE_CLARO),
        "FAIL":    ("<font color='#dc2626'><b>FALHA</b></font>",   VERMELHO_CLARO),
        "PARCIAL": ("<font color='#d97706'><b>PARCIAL</b></font>", AMARELO_CLARO),
        "WARNING": ("<font color='#d97706'><b>AVISO</b></font>",   AMARELO_CLARO),
        "ERRO":    ("<font color='#dc2626'><b>ERRO</b></font>",    VERMELHO_CLARO),
    }
    key = txt.strip().upper()
    if key in mapa:
        html, bg = mapa[key]
        return Paragraph(html, TBL_BODY), bg
    return Paragraph(txt, TBL_BODY), None


# ── Construtor principal ────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Auditoria SEO - Lbor Borrachas",
        author="Claude SEO Audit System",
    )

    story = []

    # ═══════════════════════════════════════════════════════════════════════
    # CAPA
    # ═══════════════════════════════════════════════════════════════════════

    # Bloco azul de capa (simulado com tabela)
    capa_data = [[
        Paragraph("<br/><br/><br/>", TITULO_CAPA),
    ]]
    # Usamos uma tabela com fundo azul como "capa"
    capa_tbl = Table([[
        Paragraph(
            "<font size=28><b>Auditoria SEO Completa</b></font><br/><br/>"
            "<font size=14 color='#bfdbfe'>lborborrachas.com.br</font><br/><br/>"
            "<font size=11 color='#93c5fd'>Lbor Borrachas — Distribuidora e Fabricante de Artefatos de Borracha Industrial</font>",
            estilo("CapaTxt", fontName="Helvetica-Bold", fontSize=28,
                   textColor=white, alignment=TA_CENTER, leading=34)
        )
    ]], colWidths=[17*cm])
    capa_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL_ESCURO),
        ("TOPPADDING",    (0,0), (-1,-1), 60),
        ("BOTTOMPADDING", (0,0), (-1,-1), 60),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS",(0,0), (-1,-1), [8,8,8,8]),
    ]))
    story.append(capa_tbl)
    story.append(sp(20))

    # Metadados
    meta = [
        ["Data da Auditoria",  "24 de marco de 2026"],
        ["URL Auditada",       "https://www.lborborrachas.com.br/"],
        ["Segmento",           "Borrachas Industriais — Distribuidor e Fabricante B2B/B2C"],
        ["Mercado",            "Brasil (Sao Paulo, SP)"],
        ["Plataforma",         "PHP 7.4 + AngularJS 1.6.9 (CMS MGMasters)"],
        ["Auditor",            "Claude SEO Audit System (claude-sonnet-4-6)"],
    ]
    meta_tbl = Table(
        [[Paragraph(r, TBL_BODY_BOLD), Paragraph(v, TBL_BODY)] for r,v in meta],
        colWidths=[5*cm, 12*cm]
    )
    meta_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [CINZA_CLARO, white]),
        ("BOX",  (0,0), (-1,-1), 0.6, CINZA_BORDA),
        ("GRID", (0,0), (-1,-1), 0.4, CINZA_BORDA),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(meta_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # PONTUACAO GERAL
    # ═══════════════════════════════════════════════════════════════════════
    secao("Pontuacao Geral de Saude SEO", story)

    # Placar principal
    placar_tbl = Table([[
        Paragraph(
            "<font size=48 color='#dc2626'><b>39</b></font><br/>"
            "<font size=12 color='#6b7280'>de 100</font><br/><br/>"
            "<font size=10 color='#374151'><b>Necessita Melhorias Significativas</b></font>",
            estilo("Placar", fontName="Helvetica-Bold", fontSize=48,
                   textColor=VERMELHO, alignment=TA_CENTER, leading=56)
        )
    ]], colWidths=[17*cm])
    placar_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CINZA_CLARO),
        ("TOPPADDING",    (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("BOX",           (0,0), (-1,-1), 1, CINZA_BORDA),
    ]))
    story.append(placar_tbl)
    story.append(sp(12))

    # Tabela de categorias
    story.append(p("Detalhamento por Categoria", H2))
    cats = [
        ["Categoria", "Peso", "Pontuacao", "Ponderado"],
        ["SEO Tecnico",              "22%", "54/100", "11,9"],
        ["Qualidade de Conteudo / E-E-A-T", "23%", "38/100", "8,7"],
        ["SEO On-Page",              "20%", "30/100", "6,0"],
        ["Schema / Dados Estruturados", "10%", "31/100", "3,1"],
        ["Performance (Core Web Vitals)", "10%", "44/100", "4,4"],
        ["Prontidao para IA (GEO)",  "10%", "31/100", "3,1"],
        ["Imagens",                  "5%",  "35/100", "1,75"],
        ["TOTAL",                    "100%","—",       "39 / 100"],
    ]
    cat_tbl = Table(
        [[Paragraph(c, TBL_HDR if i==0 else (TBL_BODY_BOLD if i==len(cats)-1 else TBL_BODY))
          for c in row]
         for i, row in enumerate(cats)],
        colWidths=[7*cm, 2.5*cm, 3.5*cm, 4*cm]
    )
    cat_tbl.setStyle(tbl_style())
    cat_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL_ESCURO),
        ("BACKGROUND", (0,-1),(-1,-1), AZUL_ESCURO),
        ("TEXTCOLOR",  (0,-1),(-1,-1), white),
        ("FONTNAME",   (0,-1),(-1,-1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-2), [white, CINZA_CLARO]),
        ("GRID",   (0,0), (-1,-1), 0.4, CINZA_BORDA),
        ("BOX",    (0,0), (-1,-1), 0.6, CINZA_BORDA),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 8),
        ("FONTNAME",   (0,1), (-1,-2), "Helvetica"),
        ("FONTSIZE",   (0,1), (-1,-2), 8),
    ]))
    story.append(cat_tbl)
    story.append(sp(8))

    # Scores suplementares
    sup = [
        ["Area (Suplementar)", "Pontuacao"],
        ["SEO Local",          "23/100"],
        ["Sitemap",            "54/100"],
        ["Visual / Mobile",    "64/100"],
    ]
    sup_tbl = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(sup)],
        colWidths=[9*cm, 8*cm]
    )
    sup_tbl.setStyle(tbl_style(CINZA_MEDIO))
    story.append(p("Pontuacoes Suplementares (informativo)", H3))
    story.append(sup_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # RESUMO EXECUTIVO
    # ═══════════════════════════════════════════════════════════════════════
    secao("Resumo Executivo", story)

    # Top 5 problemas criticos
    subsecao("Top 5 Problemas Criticos", story)
    criticos = [
        ("Endereco fisico completamente ausente",
         "O negocio esta invisivel para os sistemas locais do Google. O local pack "
         "e inacessivel sem o endereco no rodape e na pagina de contato."),
        ("AngularJS 1.6.9 (EOL dez/2021) + PHP 7.4.33 (EOL nov/2022)",
         "Ambos os runtimes estao sem suporte de seguranca. O framework JS "
         "representa risco de renderizacao e o PHP exposto no header anuncia a superficie de ataque."),
        ("Zero cabecalhos de seguranca (HSTS, CSP, X-Frame-Options)",
         "Ausencia de HSTS deixa usuarios expostos a SSL stripping antes dos "
         "redirecionamentos. Corrigivel em 30 minutos via Cloudflare Transform Rules."),
        ("Sem pagina 'Quem Somos', sem CNPJ publico, sem credenciais da equipe",
         "Falha critica de E-E-A-T (Confiabilidade) para um fornecedor B2B que "
         "solicita o CNPJ do comprador no proprio formulario de contato."),
        ("Homepage com ~80 palavras de conteudo editorial",
         "A pagina inteira e uma grade de produtos sem proposta de valor, sem "
         "narrativa da empresa e sem diferenciais. E o principal motivo da nota 39/100."),
    ]
    for i, (titulo, desc) in enumerate(criticos, 1):
        bloco = Table([[
            Paragraph(f"<b>{i}.</b>", estilo("Num", fontName="Helvetica-Bold",
                      fontSize=14, textColor=VERMELHO, alignment=TA_CENTER)),
            [Paragraph(f"<b>{titulo}</b>", BODY_BOLD), Paragraph(desc, BODY)]
        ]], colWidths=[1*cm, 16*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), VERMELHO_CLARO),
            ("BOX",           (0,0), (-1,-1), 0.6, VERMELHO),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(bloco)
        story.append(sp(4))

    story.append(sp(8))
    subsecao("Top 5 Ganhos Rapidos (Quick Wins)", story)
    wins = [
        ("Adicionar endereco fisico ao rodape",
         "1 hora de esforco. Habilita vinculacao com o GBP, elegibilidade ao local pack e consistencia NAP."),
        ("Adicionar cabecalhos de seguranca via Cloudflare",
         "30 minutos. Transform Rules -> HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy."),
        ("Corrigir 3 bugs criticos de schema",
         "2 horas. WebSite name:\"\" -> \"Lbor Borrachas\"; SearchAction &s= -> ?s=; remover TollFree incorreto."),
        ("Adicionar meta description + tags Open Graph",
         "30 minutos. Uma atualizacao de campo no CMS que tambem alimenta resumos gerados por IA."),
        ("Criar /llms.txt",
         "1 hora. Arquivo de texto puro, sem codigo, sinaliza prontidao para IA para GPTBot, ClaudeBot e PerplexityBot."),
    ]
    for i, (titulo, desc) in enumerate(wins, 1):
        bloco = Table([[
            Paragraph(f"<b>{i}.</b>", estilo("Num2", fontName="Helvetica-Bold",
                      fontSize=14, textColor=VERDE, alignment=TA_CENTER)),
            [Paragraph(f"<b>{titulo}</b>", BODY_BOLD), Paragraph(desc, BODY)]
        ]], colWidths=[1*cm, 16*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), VERDE_CLARO),
            ("BOX",           (0,0), (-1,-1), 0.6, VERDE),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(bloco)
        story.append(sp(4))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 1. SEO TECNICO
    # ═══════════════════════════════════════════════════════════════════════
    secao("1. SEO Tecnico — 54/100", story)

    subsecao("Infraestrutura", story)
    infra = [
        ["Componente",  "Status",  "Detalhe"],
        ["CDN",         "OK",      "Cloudflare com edge GRU (Sao Paulo)"],
        ["HTTPS",       "OK",      "Forcado via 301 em todo o site"],
        ["Compressao",  "OK",      "Brotli (Content-Encoding: br)"],
        ["HTTP/3",      "OK",      "Anunciado via alt-svc para clientes modernos"],
        ["Cache HTML",  "FALHA",   "Cache-Control: no-store - todas as paginas passam pela origem"],
    ]
    it = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(infra)],
        colWidths=[4*cm, 2.5*cm, 10.5*cm]
    )
    it.setStyle(tbl_style())
    story.append(it)
    story.append(sp(10))

    subsecao("Problemas Encontrados", story)

    # Tabela de problemas tecnicos
    tec_issues = [
        ["ID",   "Severidade", "Problema",                           "Detalhe"],
        ["T1",   "CRITICO",    "Cadeia de 3 redirecionamentos",
         "http://lborborrachas.com.br/ faz 3 saltos ate o destino. Deve ser 1 redirect 301."],
        ["T2",   "CRITICO",    "AngularJS 1.6.9 (EOL dez/2021)",
         "Framework SPA sem suporte. Dependencia de renderizacao JS cria risco para rotas dinamicas."],
        ["T3",   "CRITICO",    "Zero cabecalhos de seguranca",
         "Sem HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy."],
        ["T4",   "CRITICO",    "PHP 7.4.33 EOL exposto no X-Powered-By",
         "PHP 7.4 sem suporte desde nov/2022. Versao visivel nos headers HTTP."],
        ["T5",   "ALTO",       "Title tag: 'Lbor Borrachas' (14 chars)",
         "Nenhuma palavra-chave de produto, localizacao ou proposta de valor."],
        ["T6",   "ALTO",       "Canonical vs og:url: barra final inconsistente",
         "Canonical sem barra; og:url com barra; sitemap sem barra. Deve ser uniforme."],
        ["T7",   "ALTO",       "Schema WebSite: name vazio + SearchAction quebrado",
         "name:\"\" e target com & em vez de ?. Desqualifica o Sitelinks Searchbox."],
        ["T8",   "ALTO",       "Schema Organization: TollFree incorreto",
         "(11) 2167-5600 e um numero local de SP, nao um 0800."],
        ["T9",   "ALTO",       "Sem preload da imagem LCP",
         "Primeiro card de produto sem <link rel=preload> nem fetchpriority=high."],
        ["T10",  "MEDIO",      "Meta description como lista de palavras-chave",
         "Termos separados por pipe, capitalizacao mista, sem CTA."],
        ["T11",  "MEDIO",      "Sitemap: lastmod dinamico + changefreq=always",
         "Todos os 303 URLs mostram a data de hoje. Google ignora esses valores."],
        ["T12",  "MEDIO",      "Cache TTL de assets estaticos: 4 horas",
         "CSS/JS ja usam nomes versionados — deveriam ser max-age=31536000, immutable."],
        ["T13",  "BAIXO",      "IDs numericos nos slugs de categoria",
         "/c/11-lencol-de-borracha — prefixo numerico cria risco de link rot."],
        ["T14",  "BAIXO",      "meta revisit-after (obsoleto)",
         "Ignorado por todos os crawlers desde o inicio dos anos 2000."],
        ["T15",  "BAIXO",      "Sem IndexNow",
         "Nao implementado. Baixo esforco, acelera re-indexacao no Bing/Yandex."],
        ["T16",  "BAIXO",      "Blog em subdominio externo",
         "blog.lborborrachas.com.br (HTTP 500). Autoridade de blog nao flui para o dominio principal."],
    ]

    def build_tec_tbl(rows):
        col_w = [1.2*cm, 2.2*cm, 4.5*cm, 9.1*cm]
        sev_hex = {
            "CRITICO": "#dc2626", "ALTO": "#ea580c",
            "MEDIO": "#d97706",   "BAIXO": "#16a34a"
        }
        data = []
        for i, row in enumerate(rows):
            if i == 0:
                data.append([Paragraph(c, TBL_HDR) for c in row])
            else:
                sev = row[1]
                cor = sev_hex.get(sev, "#6b7280")
                data.append([
                    Paragraph(row[0], TBL_BODY_BOLD),
                    Paragraph(f"<font color='{cor}'><b>{sev}</b></font>", TBL_BODY),
                    Paragraph(esc(row[2]), TBL_BODY_BOLD),
                    Paragraph(esc(row[3]), TBL_BODY),
                ])
        t = Table(data, colWidths=col_w)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [white, CINZA_CLARO]),
            ("GRID",          (0,0),(-1,-1), 0.4, CINZA_BORDA),
            ("BOX",           (0,0),(-1,-1), 0.6, CINZA_BORDA),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 5),
            ("RIGHTPADDING",  (0,0),(-1,-1), 5),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,0), 8),
        ]))
        return t

    story.append(build_tec_tbl(tec_issues))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 2. CONTEUDO E E-E-A-T
    # ═══════════════════════════════════════════════════════════════════════
    secao("2. Qualidade de Conteudo e E-E-A-T — 38/100", story)

    subsecao("Avaliacao E-E-A-T", story)
    eeat = [
        ["Fator",          "Pontuacao", "Observacoes"],
        ["Experiencia",    "18/40",
         "Sem estudos de caso, sem depoimentos de clientes, sem referencias de projetos. "
         "Nomes de vendedores visiveis no WhatsApp mas sem bios ou credenciais."],
        ["Especialidade",  "22/40",
         "Descricoes de produtos mencionam dureza Shore A, faixas de temperatura, "
         "tipos de polimero (EPDM, SBR, Neoprene). Porem sem autoria nem certificacoes citadas."],
        ["Autoridade",     "12/40",
         "Sem citacoes externas, sem associacoes comerciais (ABAM, ABNT), sem avaliacoes, "
         "sem redes sociais vinculadas. Blog retorna HTTP 500."],
        ["Confiabilidade", "28/40",
         "HTTPS ativo. Telefone visivel. WhatsApp por departamento. MAS: sem endereco, "
         "sem pagina Quem Somos (404), sem CNPJ publico, sem politica de privacidade."],
    ]
    et = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(eeat)],
        colWidths=[3*cm, 2.5*cm, 11.5*cm]
    )
    et.setStyle(tbl_style())
    story.append(et)
    story.append(sp(6))
    story.append(p("<b>Total E-E-A-T: 20,5/40 (51%)</b>", BODY_BOLD))
    story.append(sp(10))

    subsecao("Problemas de Conteudo", story)
    cont_issues = [
        ["Sev.",     "Problema",                   "Detalhe"],
        ["CRITICO",  "Sem pagina 'Quem Somos'",
         "/sobre, /sobre-nos, /empresa, /quem-somos retornam 404. "
         "Zero historico da empresa, credenciais da equipe ou CNPJ visiveis."],
        ["CRITICO",  "Blog completamente inoperante",
         "blog.lborborrachas.com.br retorna HTTP 500. Link de blog no rodape aponta para URL quebrada."],
        ["CRITICO",  "Homepage com ~80 palavras editoriais",
         "Pagina e apenas uma grade de produtos. Sem H1 substantivo, sem proposta de valor, "
         "sem areas de atuacao, sem diferenciais."],
        ["ALTO",     "Title tag apenas com a marca",
         "Sem palavras-chave de produto ou localizacao."],
        ["ALTO",     "OG tags incompletas; Twitter Cards ausentes",
         "og:type e og:locale faltando. Zero Twitter Card tags em qualquer pagina."],
        ["ALTO",     "Schema sameAs vazio",
         "Google nao consegue corroborar a identidade da entidade."],
        ["MEDIO",    "Descricoes de categoria ~90-120 palavras",
         "Abaixo do minimo de 600-800 palavras para paginas B2B competitivas."],
        ["MEDIO",    "Sem preco, prazo ou MOQ",
         "Obriga compradores a enviarem cotacoes cegas. Falha na satisfacao de intencao do usuario."],
        ["MEDIO",    "Sem politica de privacidade LGPD",
         "Formularios coletam CNPJ, e-mail, telefone sem politica vinculada. "
         "Risco legal sob Lei 13.709/2018."],
    ]
    ct = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(cont_issues)],
        colWidths=[2.2*cm, 4.5*cm, 10.3*cm]
    )
    ct.setStyle(tbl_style())
    story.append(ct)
    story.append(sp(8))
    story.append(p(
        "<b>Prontidao para Citacao por IA: 18/100</b> — O site tem efetivamente zero trechos "
        "citaveis. Sem paragrafos definicionais (134-167 palavras), sem blocos de FAQ, sem tabelas "
        "de especificacoes, sem autores nomeados, sem datas de publicacao.",
        BODY))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 3. SEO ON-PAGE
    # ═══════════════════════════════════════════════════════════════════════
    secao("3. SEO On-Page — 30/100", story)

    onpage = [
        ["Elemento",         "Constatacao",                        "Status"],
        ["Title tag",        "\"Lbor Borrachas\" (14 chars, so marca)", "FALHA"],
        ["Meta description", "Presente mas lista de keywords, cap. mista", "PARCIAL"],
        ["H1",               "\"Todos os produtos\" - zero valor de keyword", "FALHA"],
        ["H2",               "Nenhum na homepage",                  "FALHA"],
        ["H3",               "24 nomes de categorias - profundidade correta", "PASS"],
        ["Hierarquia",       "Plana (H1->H3, sem H2)",              "FALHA"],
        ["Links internos",   "Categoria->produto presentes",        "PASS"],
        ["Breadcrumbs",      "Ausentes em todas as paginas",        "FALHA"],
        ["Keywords locais",  "Nenhuma em headings",                 "FALHA"],
        ["Open Graph",       "Parcial (og:title, og:description)",  "PARCIAL"],
        ["Twitter Cards",    "Completamente ausentes",              "FALHA"],
        ["lang attribute",   "pt-br — correto",                     "PASS"],
        ["Viewport meta",    "Presente",                            "PASS"],
    ]
    op_tbl = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(onpage)],
        colWidths=[4*cm, 8*cm, 5*cm]
    )
    op_tbl.setStyle(tbl_style())
    story.append(op_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 4. SCHEMA
    # ═══════════════════════════════════════════════════════════════════════
    secao("4. Schema / Dados Estruturados — 31/100", story)

    story.append(p(
        "Dois blocos JSON-LD estao presentes na homepage (WebSite e Organization), "
        "mas ambos contem erros criticos que os tornam nao funcionais para rich results.",
        BODY))
    story.append(sp(6))

    schema_erros = [
        ["Erro",                                        "Severidade"],
        ["@context usa http:// em vez de https://",     "CRITICO"],
        ["WebSite name: string vazia \"\"",              "CRITICO"],
        ["SearchAction target: & em vez de ?",           "CRITICO"],
        ["Organization: propriedade name ausente",       "CRITICO"],
        ["Microdata: 55 ListItems com URLs relativas",   "CRITICO"],
        ["Sem schema LocalBusiness",                     "CRITICO"],
        ["Sem schema Product nas paginas /p/ (230 pag)", "CRITICO"],
        ["Organization contactOption:TollFree incorreto","WARNING"],
        ["Organization sameAs: array vazio",             "WARNING"],
        ["Container ItemList vazio nas pag. de categoria","ERRO"],
        ["Sem BreadcrumbList em nenhuma pagina",         "ALTO"],
    ]
    se_tbl = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(schema_erros)],
        colWidths=[13*cm, 4*cm]
    )
    se_tbl.setStyle(tbl_style())
    story.append(se_tbl)
    story.append(sp(10))

    subsecao("Oportunidades de Schema Ausentes", story)
    schema_opp = [
        ["Tipo de Schema",      "Prioridade", "Impacto"],
        ["LocalBusiness",       "CRITICO",    "Painel de empresa, local pack, exibicao de endereco"],
        ["Product + Offer",     "CRITICO",    "Rich results de produto, elegibilidade ao Shopping"],
        ["BreadcrumbList",      "ALTO",       "Trilha de breadcrumb nos SERPs"],
        ["ItemList (JSON-LD)",  "ALTO",       "Rich results de paginas de categoria"],
        ["Article/BlogPosting", "MEDIO",      "Rich results de artigos no blog"],
        ["FAQPage",             "MEDIO",      "Beneficio para citacao por IA (GEO)"],
    ]
    so_tbl = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(schema_opp)],
        colWidths=[5.5*cm, 3*cm, 8.5*cm]
    )
    so_tbl.setStyle(tbl_style())
    story.append(so_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 5. PERFORMANCE
    # ═══════════════════════════════════════════════════════════════════════
    secao("5. Performance (Core Web Vitals) — 44/100", story)

    subsecao("Estimativa de Core Web Vitals (75 percentil, mobile Brasil)", story)
    cwv = [
        ["Metrica", "Estimativa",     "Limite Bom", "Status"],
        ["LCP",     "3,5s - 5,5s",    "< 2,5s",     "FALHA (Ruim)"],
        ["INP",     "250ms - 400ms",  "< 200ms",    "FALHA (Precisa Melhorar)"],
        ["CLS",     "0,05 - 0,12",    "< 0,10",     "MARGINAL"],
    ]
    cwv_tbl = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(cwv)],
        colWidths=[3.5*cm, 4*cm, 3.5*cm, 6*cm]
    )
    cwv_tbl.setStyle(tbl_style())
    story.append(cwv_tbl)
    story.append(sp(6))
    story.append(p(
        "Verificar dados reais no CrUX em cruxvis.withgoogle.com para valores "
        "do 75 percentil com usuarios reais brasileiros.", NOTA))
    story.append(sp(10))

    subsecao("Causas Raiz dos Problemas de Performance", story)
    perf = [
        ["Problema",                          "Impacto",    "Detalhe"],
        ["HTML sem cache (Cache-Control: no-store)", "TTFB ~450ms",
         "Todas as requisicoes anonimas passam pela origem. Cloudflare bypassa o CDN."],
        ["Google Fonts @import dentro do CSS", "+300-600ms",
         "Cascata serial: HTML > CSS > Fontes. Mover para <link> no <head> com preconnect."],
        ["Sem preload da imagem LCP",          "FCP/LCP atrasados",
         "Primeiro card de produto sem <link rel=preload> nem fetchpriority=high."],
        ["51 imagens, zero lazy loading",      "Carga total na abertura",
         "Todas as imagens carregam no inicio. Adicionar loading=lazy nas abaixo do fold."],
        ["Bundle JS de 442KB sem defer",       "INP 250-400ms",
         "AngularJS 1.6.9 + jQuery 1.9.1 em bundle sincrono unico."],
        ["Sem entrega WebP/AVIF",              "~30% de imagem extra",
         "Todas as imagens em PNG/JPG. Sem negociacao de conteudo para formatos modernos."],
        ["TTL de assets estaticos: 4 horas",   "Performance em retorno",
         "CSS/JS ja usam nomes versionados - deveriam ser max-age=31536000, immutable."],
        ["Imagens sem width/height",           "Risco de CLS",
         "Browser nao pode reservar espaco antes das imagens carregarem."],
    ]
    pt = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(perf)],
        colWidths=[5.5*cm, 3*cm, 8.5*cm]
    )
    pt.setStyle(tbl_style())
    story.append(pt)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 6. SEO LOCAL
    # ═══════════════════════════════════════════════════════════════════════
    secao("6. SEO Local — 23/100", story)

    story.append(p(
        "<b>PROBLEMA CRITICO:</b> O endereco fisico completo (Rua, numero, bairro, CEP) "
        "esta ausente em TODAS as paginas do site. O negocio e completamente invisivel "
        "para os sistemas locais do Google.", BODY_BOLD))
    story.append(sp(8))

    subsecao("Consistencia NAP", story)
    nap = [
        ["Elemento",     "Homepage",           "Pag. Contato",       "Rodape",    "Schema"],
        ["Nome",         "Lbor Borrachas OK",  "Lbor Borrachas OK",  "LborBorrachas.com.br", "String vazia FALHA"],
        ["Endereco",     "AUSENTE",            "AUSENTE",            "AUSENTE",   "AUSENTE"],
        ["Telefone",     "(11) 2167-5600 OK",  "(11) 2167-5600 OK",  "AUSENTE",   "+55-11-2167-5600 OK"],
        ["E-mail",       "vendas@lbor.com.br", "vendas@lbor.com.br", "AUSENTE",   "AUSENTE"],
    ]
    nt = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(nap)],
        colWidths=[3*cm, 3.5*cm, 3.5*cm, 3*cm, 4*cm]
    )
    nt.setStyle(tbl_style())
    story.append(nt)
    story.append(sp(10))

    subsecao("Sinais do Google Business Profile", story)
    story.append(p(
        "Pontuacao: 0/7 sinais detectados. Nenhum embed do Maps, nenhuma referencia ao GBP "
        "no schema, nenhum widget de avaliacoes.", BODY))
    story.append(sp(6))

    subsecao("Palavras-chave Locais Ausentes", story)
    story.append(p(
        "Nenhum modificador geografico foi encontrado em qualquer heading (H1/H2/H3), "
        "no title tag, nos nomes de categoria ou nas meta descriptions:",
        BODY))

    kw_miss = [
        "borrachas industriais Sao Paulo",
        "lencol de borracha SP",
        "distribuidora de borracha Sao Paulo",
        "fornecedor de borrachas SP",
        "borracha EPDM Sao Paulo",
        "piso de borracha Sao Paulo",
    ]
    for kw in kw_miss:
        story.append(p(f"  • {kw} — <b>NAO ENCONTRADO</b>", BODY))

    story.append(sp(8))
    story.append(p(
        "<b>Paginas de Localizacao: 0.</b> Nenhuma pagina especifica de localizacao existe. "
        "Uma pagina como /borrachas-industriais-sao-paulo e alta prioridade para rankeamento "
        "local organico.", BODY_BOLD))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 7. GEO / IA
    # ═══════════════════════════════════════════════════════════════════════
    secao("7. Prontidao para Busca por IA (GEO) — 31/100", story)

    subsecao("Acesso de Crawlers de IA (robots.txt)", story)
    crawlers = [
        ["Crawler",      "Propósito",                 "Status"],
        ["GPTBot",       "ChatGPT — citacoes e treino","PERMITIDO (sem regra explicita)"],
        ["OAI-SearchBot","ChatGPT busca ao vivo",      "PERMITIDO"],
        ["ClaudeBot",    "Anthropic — indexacao",      "PERMITIDO"],
        ["PerplexityBot","Perplexity AI",              "PERMITIDO"],
        ["Google-Extended","Gemini / AI Overviews",    "PERMITIDO"],
    ]
    crt = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(crawlers)],
        colWidths=[4*cm, 6*cm, 7*cm]
    )
    crt.setStyle(tbl_style())
    story.append(crt)
    story.append(sp(8))

    story.append(p(
        "<b>llms.txt: AUSENTE (404)</b> — Arquivo nao existe. "
        "Alto impacto, baixo esforco: um llms.txt bem formado sinaliza prontidao para IA "
        "e guia crawlers para paginas de alto valor.", BODY_BOLD))
    story.append(sp(8))

    subsecao("Prontidao por Plataforma de IA", story)
    plat = [
        ["Plataforma",          "Pontuacao", "Principal Gap"],
        ["Google AI Overviews", "28/100",    "Sem schema FAQ, sem headings em formato de resposta, sem meta desc."],
        ["ChatGPT / SearchGPT", "25/100",    "Zero trechos citaveis, entidade nao corroborada externamente."],
        ["Perplexity AI",       "30/100",    "SSR ajuda; zero conteudo em nivel de passagem para extrair."],
        ["Bing Copilot",        "35/100",    "SSR + schema existente dao leve vantagem; mesma falta de conteudo."],
    ]
    pt2 = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(plat)],
        colWidths=[4.5*cm, 2.5*cm, 10*cm]
    )
    pt2.setStyle(tbl_style())
    story.append(pt2)
    story.append(sp(8))
    story.append(p(
        "<b>Contexto Competitivo GEO:</b> A maturidade GEO entre fornecedores B2B "
        "industriais brasileiros e extremamente baixa em 2026. Um site que implementar "
        "llms.txt, schema FAQ e conteudo orientado a respostas nos proximos 60 dias provavelmente "
        "se tornara a fonte padrao citada por IA para consultas de borracha industrial em pt-BR — "
        "a janela competitiva esta aberta agora.", BODY))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 8. SITEMAP & IMAGENS
    # ═══════════════════════════════════════════════════════════════════════
    secao("8. Sitemap e Imagens", story)

    subsecao("Sitemap — 54/100", story)
    smap = [
        ["Verificacao",                    "Status", "Detalhe"],
        ["Descoberta (robots.txt)",         "PASS",   "Declarado no robots.txt, acessivel em /sitemap.xml"],
        ["Validade XML",                    "PASS",   "Bem formado, namespace correto"],
        ["Total de URLs",                   "303",    "230 produtos, 42 categorias, 30 artigos, 1 homepage"],
        ["Precisao do lastmod",             "FALHA",  "Todos os 303 URLs mostram a data de hoje — gerado dinamicamente"],
        ["Uso de changefreq",               "FALHA",  "'always' em todos os URLs — Google ignora"],
        ["Uso de priority",                 "FALHA",  "1.00 em todos — valores uniformes ignorados"],
        ["/cotacao no sitemap",             "FALHA",  "Pagina de conversao primaria ausente do sitemap"],
        ["Slugs malformados",               "5 erros","Hifens finais, palavras fundidas (borrachapara), slug truncado"],
    ]
    sm_tbl = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(smap)],
        colWidths=[5.5*cm, 2.5*cm, 9*cm]
    )
    sm_tbl.setStyle(tbl_style())
    story.append(sm_tbl)
    story.append(sp(10))

    subsecao("Imagens — 35/100", story)
    imgs = [
        ["Verificacao",              "Status",   "Detalhe"],
        ["Alt text presente",        "PASS",     "Todas as imagens de categoria com alt text"],
        ["Qualidade do alt text",    "PARCIAL",  "1 imagem errada: Mangueira de Silicone usada para Perfil de Silicone"],
        ["Lazy loading",             "FALHA",    "Zero atributos loading=lazy em qualquer imagem"],
        ["Entrega WebP / AVIF",      "FALHA",    "Todas em PNG/JPG sem negociacao de formato"],
        ["Width/height explicitos",  "FALHA",    "Nenhum <img width height> em nenhuma imagem"],
        ["Preload da imagem LCP",    "FALHA",    "Sem <link rel=preload> para a primeira imagem visivel"],
        ["fetchpriority",            "FALHA",    "Sem fetchpriority=high em nenhuma imagem"],
        ["srcset responsivo",        "FALHA",    "Mesma imagem servida independente do viewport"],
        ["Compressao",               "PARCIAL",  "Thumbs 240px, tamanho moderado (~15-40 KB cada)"],
    ]
    img_tbl = Table(
        [[Paragraph(esc(c) if i>0 else c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(imgs)],
        colWidths=[5*cm, 2.5*cm, 9.5*cm]
    )
    img_tbl.setStyle(tbl_style())
    story.append(img_tbl)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 9. PLANO DE ACAO
    # ═══════════════════════════════════════════════════════════════════════
    secao("9. Plano de Acao Priorizado", story)

    story.append(p(
        "Pontuacao atual: <b>39/100</b> | Meta em 3 meses: <b>72-79/100</b> | "
        "Ganho estimado: <b>+33-40 pontos</b>", BODY_BOLD))
    story.append(sp(8))

    # Tabela de impacto por fase
    fases = [
        ["Fase",     "Prazo",    "Ganho Est.", "Acoes Prioritarias"],
        ["Fase 1",   "Semana 1", "+8-10 pts",
         "Cabecalhos de seguranca, endereco, correncoes de schema, title tag, llms.txt"],
        ["Fase 2",   "Semana 2", "+10-12 pts",
         "GBP, schema LocalBusiness, pagina Quem Somos, schema Product"],
        ["Fase 3",   "Mes 1",    "+8-10 pts",
         "Blog, cache edge, correcoes LCP, conteudo de categorias"],
        ["Fase 4",   "Trimestre 1","5-8 pts",
         "Conteudo da homepage, schema FAQ, YouTube, atualizacao PHP"],
        ["TOTAL",    "3 meses",  "~71-79/100","—"],
    ]
    ft = Table(
        [[Paragraph(c, TBL_HDR if i==0 else TBL_BODY) for c in row]
         for i, row in enumerate(fases)],
        colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 9.5*cm]
    )
    ft.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
        ("BACKGROUND",    (0,-1),(-1,-1),AZUL_ESCURO),
        ("TEXTCOLOR",     (0,-1),(-1,-1),white),
        ("FONTNAME",      (0,-1),(-1,-1),"Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1), (-1,-2),[white, CINZA_CLARO]),
        ("GRID",          (0,0), (-1,-1),0.4, CINZA_BORDA),
        ("BOX",           (0,0), (-1,-1),0.6, CINZA_BORDA),
        ("TOPPADDING",    (0,0), (-1,-1),5),
        ("BOTTOMPADDING", (0,0), (-1,-1),5),
        ("LEFTPADDING",   (0,0), (-1,-1),6),
        ("RIGHTPADDING",  (0,0), (-1,-1),6),
        ("VALIGN",        (0,0), (-1,-1),"TOP"),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1),8),
    ]))
    story.append(ft)
    story.append(sp(12))

    # Acoes detalhadas - Fase 1
    sev_hex2 = {
        "CRITICO": "#dc2626", "ALTO": "#ea580c",
        "MEDIO": "#d97706",   "BAIXO": "#16a34a"
    }

    def action_block(cod, sev, titulo, esforco, impacto, acao_txt, color_bg, color_borda):
        cor = sev_hex2.get(sev, "#6b7280")
        bloco = Table([[
            [
                Paragraph(f"<b>{cod}</b> — <font color='{cor}'><b>{sev}</b></font>",
                          BODY_BOLD),
                Paragraph(f"<b>{esc(titulo)}</b>", H3),
                Paragraph(f"<b>Esforco:</b> {esc(esforco)} | <b>Impacto:</b> {esc(impacto)}", NOTA),
                Paragraph(esc(acao_txt), BODY),
            ]
        ]], colWidths=[17*cm])
        bloco.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), color_bg),
            ("BOX",           (0,0),(-1,-1), 0.8, color_borda),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ]))
        return bloco

    story.append(p("FASE 1 — Esta Semana (Sem deploy de codigo)", H2))
    story.append(sp(4))

    acoes_f1 = [
        ("C1", "CRITICO", "Adicionar Endereco Fisico ao Rodape e Pagina de Contato",
         "1 hora", "Visibilidade no local pack, associacao com GBP, consistencia NAP",
         "Adicionar o endereco completo (Rua, numero, bairro, cidade, estado, CEP) "
         "como texto visivel no rodape e em /contato. Incluir CNPJ publicamente.",
         VERMELHO_CLARO, VERMELHO),
        ("C2", "CRITICO", "Adicionar Cabecalhos de Seguranca via Cloudflare",
         "30 minutos", "Seguranca, sinais de confianca do usuario",
         "Cloudflare > Transform Rules > Modify Response Header: Strict-Transport-Security, "
         "X-Content-Type-Options, X-Frame-Options, Referrer-Policy.",
         VERMELHO_CLARO, VERMELHO),
        ("C3", "CRITICO", "Corrigir Cadeia de Redirecionamento",
         "30 minutos", "Crawl budget, link equity, TTFB",
         "Cloudflare Page Rules: http://lborborrachas.com.br/* -> 301 -> "
         "https://www.lborborrachas.com.br/$1 (1 unico salto).",
         VERMELHO_CLARO, VERMELHO),
        ("C4", "CRITICO", "Suprimir Versao PHP no Header",
         "5 minutos", "Seguranca",
         "Adicionar expose_php = Off no php.ini. "
         "Planejar atualizacao para PHP 8.2+ no roadmap tecnico.",
         VERMELHO_CLARO, VERMELHO),
        ("C5", "CRITICO", "Corrigir Erros Criticos de Schema",
         "2 horas", "Sitelinks Searchbox, rich results, confianca da entidade",
         "1) name:\"\" -> \"Lbor Borrachas\" no JSON-LD WebSite. "
         "2) search&s= -> search?s= no target da SearchAction. "
         "3) Remover contactOption:TollFree incorreto. "
         "4) Mudar todos @context http:// para https://.",
         VERMELHO_CLARO, VERMELHO),
        ("H1", "ALTO", "Expandir Title Tag da Homepage",
         "15 minutos", "CTR, sinal de ranking por palavra-chave",
         "Atualizar para 50-60 caracteres: "
         "\"Lbor Borrachas | Manta, Lencol e Perfis de Borracha Industrial\"",
         LARANJA_CLARO, LARANJA),
        ("H2", "ALTO", "Reescrever Meta Description da Homepage",
         "15 minutos", "CTR, qualidade de resumo por IA",
         "Substituir por (ate 155 chars): \"Distribuidora e fabricante de manta, "
         "lencol e perfis de borracha industrial. Neoprene, EPDM, Silicone e mais. "
         "Solicite orcamento online.\"",
         LARANJA_CLARO, LARANJA),
        ("H3", "ALTO", "Adicionar Tags Open Graph + Twitter Card",
         "1 hora", "Compartilhamento social, extracao de metadata por IA",
         "Adicionar ao template <head>: og:type=website, og:locale=pt_BR, "
         "twitter:card, twitter:title, twitter:description, twitter:image.",
         LARANJA_CLARO, LARANJA),
        ("H4", "ALTO", "Criar /llms.txt",
         "1 hora", "Prontidao para busca por IA (GEO)",
         "Criar em https://www.lborborrachas.com.br/llms.txt com nome, URL, "
         "descricao, paginas-chave e permissoes explitas para GPTBot, ClaudeBot, "
         "PerplexityBot e Google-Extended.",
         LARANJA_CLARO, LARANJA),
    ]

    for cod, sev, titulo, esf, imp, acao, bg, borda in acoes_f1:
        story.append(KeepTogether([
            action_block(cod, sev, titulo, esf, imp, acao, bg, borda),
            sp(5)
        ]))

    story.append(PageBreak())

    story.append(p("FASE 2 — Semana 2 (Mudancas de template CMS)", H2))
    story.append(sp(4))

    acoes_f2 = [
        ("C6", "CRITICO", "Revindicar e Otimizar Google Business Profile",
         "2-4 horas", "Ranking no local pack (fator #1 Whitespark 2026)",
         "Acessar google.com/business, reivindicar o perfil para o endereco de SP, "
         "definir categoria primaria, subir 10+ fotos, adicionar horario, descricao e URL.",
         VERMELHO_CLARO, VERMELHO),
        ("C7", "CRITICO", "Atualizar Schema Organization para LocalBusiness",
         "3 horas", "Painel de empresa, local pack, rich results",
         "Substituir o JSON-LD Organization por LocalBusiness com: name, address "
         "(PostalAddress completo), geo (GeoCoordinates), telephone, openingHoursSpecification, "
         "sameAs com URL do GBP e LinkedIn.",
         VERMELHO_CLARO, VERMELHO),
        ("C8", "CRITICO", "Criar Pagina 'Quem Somos'",
         "4 horas", "E-E-A-T Confiabilidade, sinais de entidade do Google",
         "Criar /quem-somos com: historico e ano de fundacao (400+ palavras), "
         "endereco completo + mapa, CNPJ publico, membros nomeados da equipe, "
         "associacoes industriais, certificacoes, link para politica de privacidade LGPD.",
         VERMELHO_CLARO, VERMELHO),
        ("H5", "ALTO", "Adicionar Schema BreadcrumbList a Categorias e Produtos",
         "4 horas", "Breadcrumb nos SERPs, CTR",
         "Adicionar JSON-LD BreadcrumbList no <head> de cada template de categoria "
         "e produto com items absolutos (Inicio > Categoria > Produto).",
         LARANJA_CLARO, LARANJA),
        ("H6", "ALTO", "Corrigir Microdata: Converter para JSON-LD com URLs Absolutas",
         "3 horas", "Rich results de ItemList",
         "Remover container ItemList vazio. Converter todos os 55 itemprop=url e "
         "itemprop=image de URLs relativas para absolutas, ou migrar para JSON-LD.",
         LARANJA_CLARO, LARANJA),
        ("H7", "ALTO", "Corrigir H1 da Homepage e Adicionar Tags H2",
         "2 horas", "Relevancia de keyword, hierarquia de conteudo",
         "H1: \"Borrachas Industriais: Lencol, Manta, Perfis e Silicone em Sao Paulo\". "
         "H2s: grupos de familias de produtos com modificadores locais.",
         LARANJA_CLARO, LARANJA),
        ("H10", "ALTO", "Adicionar Schema Product a Todas as Paginas /p/",
         "1-2 dias", "Rich results de produto, elegibilidade ao Shopping",
         "Gerar dinamicamente JSON-LD Product+Offer em cada pagina de produto "
         "com name, description, image (URL absoluta), sku, brand e offers.",
         LARANJA_CLARO, LARANJA),
    ]

    for cod, sev, titulo, esf, imp, acao, bg, borda in acoes_f2:
        story.append(KeepTogether([
            action_block(cod, sev, titulo, esf, imp, acao, bg, borda),
            sp(5)
        ]))

    story.append(PageBreak())

    story.append(p("FASE 3 — Mes 1 (Conteudo e Performance)", H2))
    story.append(sp(4))

    acoes_f3 = [
        ("C9", "CRITICO", "Restaurar ou Migrar Blog",
         "4-8 horas", "Autoridade topica, E-E-A-T, alvo de backlinks",
         "Corrigir HTTP 500 no blog.lborborrachas.com.br ou migrar os 30 artigos "
         "para www.lborborrachas.com.br/blog/ com redirects 301.",
         VERMELHO_CLARO, VERMELHO),
        ("H11", "ALTO", "Ativar Cache Edge no Cloudflare para Paginas HTML",
         "2 horas", "Reducao de TTFB de ~450ms para ~20-50ms em hits de cache",
         "Cache Rule: excluir /admin, /cotacao, /contato, /carrinho. "
         "Action: Cache Everything, Edge TTL: 5 minutos. "
         "Remover/ignorar cookie de sessao para requisicoes GET anonimas.",
         LARANJA_CLARO, LARANJA),
        ("H12", "ALTO", "Adicionar Preload da Imagem LCP + Lazy Loading",
         "2 horas", "LCP de 4-5s para 2-3s",
         "Adicionar <link rel=preload as=image> no <head> para a primeira imagem de produto. "
         "Adicionar loading=lazy em todas as imagens abaixo da 4a posicao.",
         LARANJA_CLARO, LARANJA),
        ("H13", "ALTO", "Corrigir Google Fonts @import para <link> com Preconnect",
         "1 hora", "Remove 300-600ms do caminho critico de renderizacao",
         "Remover @import do CSS. Adicionar ao <head>: "
         "<link rel=preconnect href=https://fonts.googleapis.com> e "
         "<link rel=preconnect href=https://fonts.gstatic.com crossorigin>.",
         LARANJA_CLARO, LARANJA),
        ("H14", "ALTO", "Adicionar defer ao Bundle JS Principal",
         "30 minutos", "Remove 442KB JS do caminho critico de renderizacao",
         "Mudar <script src=/script_6978.min.js> para "
         "<script src=/script_6978.min.js defer>.",
         LARANJA_CLARO, LARANJA),
        ("M1", "MEDIO", "Publicar Politica de Privacidade LGPD",
         "2 horas", "Conformidade legal, sinais de confianca",
         "Criar /politica-de-privacidade atendendo a Lei 13.709/2018. "
         "Vincular no rodape, em /contato e em /cotacao.",
         AMARELO_CLARO, AMARELO),
        ("M2", "MEDIO", "Expandir Descricoes de Categorias para 600-800 Palavras",
         "3-5h por categoria", "Autoridade topica, remediacao de conteudo ralo",
         "Priorizar: /c/11-lencol-de-borracha, /c/26-pisos-de-borracha, "
         "/c/365-manta-de-silicone, /c/63-neoprene-fretado. "
         "Incluir tabelas de especificacoes, aplicacoes industriais, FAQ.",
         AMARELO_CLARO, AMARELO),
        ("M3", "MEDIO", "Corrigir Sitemap: Datas lastmod Reais + Remover Tags Obsoletas",
         "4 horas", "Eficiencia de crawl budget",
         "Armazenar timestamp updated_at real por produto/categoria/artigo no banco. "
         "Emitir timestamps reais no lastmod. Remover todos changefreq e priority.",
         AMARELO_CLARO, AMARELO),
        ("M5", "MEDIO", "Criar Pagina de Localizacao Sao Paulo",
         "3 horas", "Ranking organico local para queries geomodificadas",
         "Criar /borrachas-industriais-sao-paulo com H1 local, "
         "endereco + embed do Maps, area de atuacao (SP + ABCD + Grande SP), "
         "horario, CTA para /cotacao e schema LocalBusiness.",
         AMARELO_CLARO, AMARELO),
    ]

    for cod, sev, titulo, esf, imp, acao, bg, borda in acoes_f3:
        story.append(KeepTogether([
            action_block(cod, sev, titulo, esf, imp, acao, bg, borda),
            sp(5)
        ]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # 10. CHECKLIST DE MONITORAMENTO
    # ═══════════════════════════════════════════════════════════════════════
    secao("10. Checklist de Monitoramento", story)

    story.append(p(
        "Apos implementar as Fases 1 e 2, verificar os seguintes pontos:", BODY))
    story.append(sp(6))

    checks = [
        ("Google Search Console",
         "Enviar sitemap apos correcao do lastmod; verificar erros de schema no relatorio de Resultados Avancados."),
        ("Google Rich Results Test",
         "Validar schemas LocalBusiness, WebSite e Product em search.google.com/test/rich-results."),
        ("CrUX / PageSpeed Insights",
         "Monitorar LCP, INP, CLS antes e apos as mudancas de performance em pagespeed.web.dev."),
        ("Cloudflare Analytics",
         "Verificar aumento na taxa de cache hit apos ativar o Cache Rule para HTML."),
        ("GBP Insights",
         "Monitorar impressoes no local pack e solicitacoes de direcao apos reivindicar o GBP."),
        ("Schema Validator",
         "Testar todos os blocos JSON-LD em validator.schema.org apos correcoes."),
        ("Google Search Console — Pagina Quem Somos",
         "Monitorar indexacao da nova pagina em Coverage > Indexed."),
    ]

    for titulo, desc in checks:
        bloco = Table([[
            Paragraph("[ ]", BODY_BOLD),
            [Paragraph(f"<b>{titulo}</b>", BODY_BOLD), Paragraph(desc, BODY)]
        ]], colWidths=[0.8*cm, 16.2*cm])
        bloco.setStyle(TableStyle([
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 4),
            ("RIGHTPADDING",  (0,0),(-1,-1), 4),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
            ("LINEBELOW",     (0,0),(-1,-1), 0.3, CINZA_BORDA),
        ]))
        story.append(bloco)

    story.append(sp(16))
    story.append(hr(AZUL_MEDIO, 1))
    story.append(sp(6))
    story.append(p(
        "Auditoria gerada por Claude SEO Audit System (claude-sonnet-4-6) em 24 de marco de 2026. "
        "Todos os dados foram obtidos por analise direta do site lborborrachas.com.br via crawl ao vivo.",
        NOTA))

    # ─── Build ───────────────────────────────────────────────────────────────
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(CINZA_MEDIO)
        canvas.drawString(2*cm, 1.2*cm,
            "Auditoria SEO — lborborrachas.com.br — Confidencial — 24/03/2026")
        canvas.drawRightString(W - 2*cm, 1.2*cm, f"Pagina {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF gerado com sucesso: {OUTPUT}")


if __name__ == "__main__":
    build()
