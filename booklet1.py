import os
import random

import bookletpdf


def make_random_line():
	color_by_label = {
		'red': bookletpdf.colors.Color(1.0, 0, 0),
		'blue': bookletpdf.colors.Color(0, 0, 1.0),
		'': bookletpdf.colors.Color(0.8, 0.8, 0.8)
	}
	x = random.randint(0, 100)
	y = random.randint(0, 100)
	label = random.choice(color_by_label.keys())
	color = color_by_label[label]
	return (x, y, color, label)


def get_graph_flowable(lines):
	width, height, plot_offset = 450, 120, 30
	x_lims = [0, max([l[0] for l in lines]) * 1.2]
	y_lims = [0, max([l[1] for l in lines]) * 1.2]
	graph = bookletpdf.Graph(width, height, x_lims, y_lims, plot_offset)
	for line in lines:
	  graph.add_vert_line(*line)
	return graph.flowable	


def make_table_data():
	data = []
	n_row = 15
	headings = list("ABCDEFGH")
	n_col = len(headings)
	for j in range(n_row):
		data.append([])
		if j == 0:
			data[0] = headings
			continue
		for i in range(n_col):
			data[j].append(random.randint(0, 100))
	return data


doc = bookletpdf.Booklet('booklet1.pdf')

height_in_inches = 2.5
doc.add_spacer(height_in_inches)
doc.add_paragraph('Example PDF Title', style=bookletpdf.title_style)
doc.add_paragraph('Oh Yeah', style=bookletpdf.title_style)

doc.switch_page_template('numbered_page')
doc.add_page_break()

doc.add_toc_header('Table of Contents')
doc.add_toc()

doc.add_page_break()
doc.add_toc_header('Chapter 1')
doc.add_paragraph('Lorum Ipsum et cetera.')
doc.add_bullet('point one')
doc.add_bullet('point two')

bookletpdf.resize_image('seal.jpg', 'seal-300.jpg', width=100)
doc.add_figure('seal-300.jpg', 'This is a seal.')

doc.add_page_break()
doc.add_toc_header('Next Chapter')
doc.add_paragraph('More spicey.')

lines = [make_random_line() for i in range(100)]
doc.elements.append(get_graph_flowable(lines))

data = make_table_data()
table = bookletpdf.Table(data, hAlign='LEFT')
table.setStyle(bookletpdf.TableStyle(bookletpdf.table_styles))
doc.elements.append(table)

doc.build()

os.system('open booklet1.pdf')
