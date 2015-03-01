# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import OrderedDict
import re

try:
    from reportlab import rl_config
    from reportlab.pdfgen.canvas import Canvas

    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Spacer, Paragraph, NextPageTemplate, PageBreak, Table, TableStyle
    from reportlab.platypus.figures import ImageFigure
    from reportlab.platypus.tableofcontents import TableOfContents

    from reportlab.graphics.shapes import colors, Drawing, Rect, Line, Group, String

    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
except:
    raise ImportError("Couldn't import reportlab")


# suppress creation timestamp and randomized document ID
rl_config.invariant = 1


# define styles

title_style = ParagraphStyle(
    name='Title',
    fontSize=30,
    leading=30,
    spaceAfter=12,
    textColor=colors.Color(0.4, 0., 0.),
    alignment=TA_LEFT,
    fontName='Helvetica-Bold')

heading1_style = ParagraphStyle(
    name='toc-entry-1',
    fontSize=20,
    leading=20,
    spaceAfter=20,
    alignment=TA_LEFT,
    leftIndent=0,
    fontName='Helvetica-Bold')

heading2_style = ParagraphStyle(
    name='toc-entry-2',
    fontSize=16,
    leading=16,
    spaceAfter=16,
    alignment=TA_LEFT,
    leftIndent=0,
    fontName='Helvetica-Bold')

bullet_style = ParagraphStyle(
    name='Bullet',
    fontSize=12,
    leading=12,
    spaceAfter=6,
    textColor='black',
    alignment=TA_LEFT,
    bulletIndent=0,
    leftIndent=10)

paragraph_style = ParagraphStyle(
    name='Paragraph',
    leftIndent=0,
    spaceBefore=0,
    spaceAfter=12,
    alignment=TA_JUSTIFY,
    fontSize=12,
    leading=12)

footer_style = ParagraphStyle(
    name='footer',
    leftIndent=0,
    spaceBefore=0,
    spaceAfter=0,
    fontSize=12,
    leading=12)


class SpectraGraph():

    def __init__(
            self, full_width, full_height,
            x_lims, y_lims, box_offset):
        self.drawing = Drawing(full_width, full_height)
        self.x_lims = x_lims
        self.y_lims = y_lims
        self.x_delta = x_lims[1] - x_lims[0]
        self.y_delta = y_lims[1] - y_lims[0]
        self.i_plot_offset = box_offset
        self.j_plot_offset = box_offset
        self.width_plot = full_width - box_offset
        self.height_plot = full_height - box_offset
        self.font_size = 6
        background_color = colors.Color(0.98, 0.98, 0.98)
        self.drawing.add(
            Rect(
                self.i_plot_offset, self.j_plot_offset,
                self.width_plot, self.height_plot,
                fillColor=background_color,
                strokeColor=None))
        self.add_labels()

    def add_labels(self):
        unmatched_color = colors.Color(0.8, 0.8, 0.8)
        self.drawing.add(
            String(
                self.i_plot_offset + 0.5 * self.width_plot,
                self.j_plot_offset - 10,
                'M/Z',
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='middle',
                fillColor=unmatched_color))

        self.drawing.add(
            String(
                self.i_plot_offset,
                self.j_plot_offset - 10,
                str(self.x_lims[0]),
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='middle',
                fillColor=unmatched_color))

        self.drawing.add(
            String(
                self.i_plot_offset + self.width_plot,
                self.j_plot_offset - 10,
                str(int(self.x_lims[1])),
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='middle',
                fillColor=unmatched_color))

        self.drawing.add(
            String(
                self.i_plot_offset - 5,
                self.j_plot_offset - 2,
                str(self.y_lims[0]),
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='end',
                fillColor=unmatched_color))

        self.drawing.add(
            String(
                self.i_plot_offset - 5,
                self.j_plot_offset + self.height_plot - 2,
                str(int(self.y_lims[1])),
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='end',
                fillColor=unmatched_color))

    def x_to_i(self, x):
        fraction = (x - self.x_lims[0]) / float(self.x_delta)
        return fraction * self.width_plot + self.i_plot_offset

    def y_to_j(self, y):
        fraction = (y - self.y_lims[0]) / float(self.y_delta)
        return fraction * self.height_plot + self.j_plot_offset

    def add_vert_line(self, x, y, label, color):
        i = self.x_to_i(x)
        j = self.y_to_j(y)
        self.drawing.add(
            Line(
                i, self.j_plot_offset,
                i, j,
                strokeColor=color,
                strokeWidth=0.75))
        if not label:
            return
        group = Group(
            String(
                0, 0,
                label,
                fontSize=self.font_size,
                fontName='Helvetica',
                textAnchor='start',
                fillColor=color))
        group.translate(i + 1, j + 2)
        group.rotate(90)
        self.drawing.add(group)


class TocDocTemplate(BaseDocTemplate):

    """
    A Doc Template that creates a TOC entry for every
    paragraph with style 'Heading1' and 'Heading2'
    """

    def afterFlowable(self, flowable):
        "Registers TOC entries"

        if not flowable.__class__.__name__ == 'Paragraph':
            return

        text = flowable.getPlainText()

        style = flowable.style.name
        p = re.search(r'toc-entry-(\d+)', style)
        if not p:
            return

        level = int(p.group(1))
        toc_entry = [level, text, self.page]
        bookmark_name = getattr(flowable, '_bookmarkName', None)
        if bookmark_name is not None:
            toc_entry.append(bookmark_name)

        self.notify('TOCEntry', tuple(toc_entry))


class Booklet():

    def __init__(self, pdf):
        self.elements = []
        self.chapter_num = 1

        self.doc = TocDocTemplate(pdf)

        self.page_templates = OrderedDict()
        self.build_page_templates()

        self.toc = TableOfContents()

        self.footer_tag = "made with http://boscoh.github.io/peptagram"
        self.footer_tag_link = "http://boscoh.github.io/peptagram"
        self.footer_font_size = 6

    def draw_blank_page(self, canvas, doc):
        canvas.saveState()
        canvas.restoreState()

    def draw_numbered_page(self, canvas, doc):
        footer_bottom = doc.bottomMargin
        top_line = footer_bottom + self.footer_font_size
        line_length = doc.width + doc.leftMargin

        canvas.saveState()
        canvas.setFont('Helvetica', self.footer_font_size)
        text = "Page %d" % doc.page
        canvas.drawString(inch, footer_bottom, text)

        if self.footer_tag:
            canvas.drawRightString(line_length, footer_bottom, self.footer_tag)
            if self.footer_tag_link:
                rect_left = line_length - canvas.stringWidth(text)
                link_rect = (line_length, footer_bottom, rect_left, top_line)
                canvas.linkURL(self.footer_tag_link, link_rect)

        canvas.restoreState()

    def build_page_templates(self):
        # normal frame that as Single Column
        full_width_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            self.doc.height,
            id='normal')

        self.page_templates['blank_page'] = \
            PageTemplate(
                id='blank_page',
                frames=full_width_frame,
                onPage=self.draw_blank_page)

        self.page_templates['numbered_page'] = \
            PageTemplate(
                id='numbered_page',
                frames=full_width_frame,
                onPage=self.draw_numbered_page)

        # A common Two-Column Frame
        left_column_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width / 2 - 6,
            self.doc.height,
            id='left_col')

        right_column_frame = Frame(
            self.doc.leftMargin + self.doc.width / 2 + 6,
            self.doc.bottomMargin,
            self.doc.width / 2 - 6,
            self.doc.height,
            id='right_col')

        self.page_templates['2column_numbered_page'] = \
            PageTemplate(
                id='2column_numbered_page',
                frames=[left_column_frame, right_column_frame],
                onPage=self.draw_numbered_page)

        self.doc.addPageTemplates(self.page_templates.values())

    def switch_page_template(self, template_id):
        self.elements.append(NextPageTemplate(template_id))

    def add_toc(self):
        self.elements.append(self.toc)

    def add_page_break(self):
        self.elements.append(PageBreak())

    def add_paragraph(self, txt, style=paragraph_style):
        self.elements.append(Paragraph(txt, style))

    def add_bullet(self, txt, style=bullet_style):
        self.elements.append(
            Paragraph("<bullet>&bull;</bullet>" + txt, bullet_style))

    def add_spacer(self, height_in_inches):
        self.elements.append(Spacer(0.1 * inch, height_in_inches * inch))

    def add_toc_header(self, text=None):
        if not text:
            text = 'Chapter %d' % self.chapter_num
        self.add_paragraph(text, heading1_style)
        self.add_spacer(0.1)
        self.chapter_num += 1

    def add_figure(self, jpg, caption):
        self.elements.append(
            ImageFigure(jpg, caption))

    def add_spectra_graph(self, x_vals, y_vals):
        x_lims = [0, max(x_vals) * 1.2]
        y_lims = [0, max(y_vals) * 1.2]
        full_width = 450
        full_height = 120
        graph = SpectraGraph(
            full_width, full_height, x_lims, y_lims, 30)
        unmatched_color = colors.Color(0.8, 0.8, 0.8)
        for x, y in zip(x_vals, y_vals):
            graph.add_vert_line(
                x, y, 'haha', unmatched_color)
        self.elements.append(graph.drawing)

    def build(self):
        self.doc.multiBuild(
            self.elements, canvasmaker=Canvas)


def resize_image(in_jpg, out_jpg, width=None, height=None):
    try:
        import PIL
    except:
        raise ImportError("Couldn't import PIL (also known as Pillow)")
    img = PIL.Image.open(in_jpg)
    old_width, old_height = img.size
    width_div_height = old_width / (float(old_height))
    if width and height:
        img.resize((width, height))
    elif width:
        img.resize((width, int(width / width_div_height)))
    elif height:
        img.resize((int(height * width_div_height), height))
    img.save(out_jpg)


