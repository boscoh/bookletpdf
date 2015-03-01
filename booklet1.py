import os
import random

from bookletpdf import Booklet, title_style, resize_image


doc = Booklet('booklet1.pdf')

doc.add_spacer(2.5)
doc.add_paragraph('Example PDF Title', style=title_style)
doc.add_paragraph('Oh Yeah', style=title_style)

doc.switch_page_template('numbered_page')
doc.add_page_break()

doc.add_toc_header('Table of Contents')
doc.add_toc()

doc.add_page_break()
doc.add_toc_header('Chapter 1')
doc.add_paragraph('Lorum Ipsum et cetera.')
doc.add_bullet('point one')
doc.add_bullet('point two')

resize_image('seal.jpg', 'seal-300.jpg', width=100)
doc.add_figure('seal-300.jpg', 'This is a seal.')

doc.add_page_break()
doc.add_toc_header('Next Chapter')
doc.add_paragraph('More spicey.')

x_vals = [random.randint(0, 100) for i in range(100)]
y_vals = [random.randint(0, 100) for i in range(100)]
doc.add_spectra_graph(x_vals, y_vals)

doc.build()

os.system('open booklet1.pdf')
