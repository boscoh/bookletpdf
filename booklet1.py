import os
import random

from bookletpdf import Booklet, title_style, resize_image, colors


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

lines = []
color_by_label = {
	'red': colors.Color(1.0, 0, 0),
	'blue': colors.Color(0, 0, 1.0),
	'': colors.Color(0.8, 0.8, 0.8)
}
for i in range(100):
	x = random.randint(0, 100)
	y = random.randint(0, 100)
	label = random.choice(['', 'red', 'blue'])
	lines.append([x, y, label, color_by_label[label]])
doc.add_spectra_graph(lines)

doc.build()

os.system('open booklet1.pdf')
