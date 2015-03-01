
# bookletpdf

Wraps reportlab to create PDF documents filled with graphs, and indexed with a table-of-contents.

## Installation

Download from github:

    git clone http://github.com/boscoh/bookletpdf

Then install with your python install:

    python setup.py install

## Why?
`bookletpdf` helps produce long PDF documents that containly mostly graphs and images, indexed with a table-of-contents. It's based on  [`reportlab`](http://www.reportlab.com/opensource/), which is powerful but complicated. `reportlab` provides a PDF renderer, document manager, frames and drawing primitives. `bookletpdf` wraps all the necessary features to make long documents, and serves as a starting point for your own customized documents.

## The Main Object

`bookletpdf` provides a main object `Booklet` to create documents, as well as a handful of auxillary variables and functions. Create an instance to with your PDF name:

     import bookletpdf
     doc = bookletpdf.Booklet('target.pdf')

Then you add a bunch of `reportlab` stuff and once you've finished, you build the document:

     doc.build()

## Page Templates, Page Breaks & Footers

One of the concepts used in `reportlab` is page templates. A document object receives flowables (paragraphs, tables, images, figures, bullets), and then sends the flowables into a page-template to be drawn into a page of the PDF.

`Booklet` managers page-templates by storing them in the dictionary field `page_templates`. The loaded page templates can be seen by:

    print doc.page_templates.keys()

And these are:

 - `blank_page`
 - `numbered_page`
 - `2column_numbered_page`
 
You can add more page templates directly to this dictonary. During document construction, the first page will be `blank_page` unless you switch. You can switch templates with:

    doc.switch_template('numbered_page')

The `numbered_page` template will put a page number in the bottom-left hand corner. In the bottom-mright hand corner is a name-tag for your document, and this is set to:

    doc.footer_tag = 'whatever'

And this may be set as a link to a URL:

    doc.footer_tag_link = 'http://company.com'

The size of the footer is controlled by:

    doc.footer_font_size = 8

## Paragraph, Bullets and Styles

Text is entered through paragraphs, and they are put into the document in paragraph blocks:

    doc.add_paragraph('A sample paragraph.')
   
Your text can embed all the [various xml](http://www.reportlab.com/software/rml-reference/) tags that `reportlab` recognizes for special characters, bold, superscripts etc.

More importantly, you can add your own `reportlab` style as a second argument, using `Paragraph` which is an alias for the built-in `reportlab` function:

    title_style = ParagraphStyle(
      name='Title',
      fontSize=30,
      leading=30,
      spaceAfter=12,
      textColor=bookletpdf.colors.Color(0.4, 0., 0.),
      alignment=bookletpdf.TA_LEFT,
      fontName='Helvetica-Bold')

    doc.add_paragraph('Some text in different style', new_style)

Another common typographical element is a bullet list:

    doc.add_bullet('a bullet boint')

And bullets can take paragraph styles with optional bullet control:

    my_bullet_style = ParagraphStyle(
        name='Bullet',
        fontSize=12,
        leading=12,
        spaceAfter=6,
        textColor='black',
        alignment=bookletpdf.TA_LEFT,
        bulletIndent=0,
        leftIndent=10)

    doc.add_bullet('next bullet boint', my_bullet_style)

Indeed, `doc` tracks the `reportlab` flowable in the list:

    doc.elements

You can add any `reportlab` flowable `widget` by:

    doc.elements.append(widget)

## Table of Contents

To generate Table of Contents (TOC), you must put a TOC somewhere in the document: 

    doc.add_toc()

How the TOC works is that `doc` will track any paragraph with a name of the form `toc-entry-1`, `toc-entry-2`,... The level in the TOC is indicated by the number at the end:

The such styles have been provided for you, `bookletpdf.heading1` and `bookletpdf.heading2`, but of course you can define your own:

    my_heading_style = ParagraphStyle(
        name='toc-entry-1',
        fontSize=20,
        leading=20,
        spaceAfter=20,
        alignment=bookletpdf.TA_LEFT,
        leftIndent=0,
        fontName='Helvetica-Bold')

This has been wrapped in a method called:

    doc.add_toc_header()

which provides some simple decoration and names the header Chapter X where `doc` keeps count of the number X.

## Figures 

The are quite a few ways to insert figures into your document (use the XML language or construct a new flowable). Here's a convenience function to insert a figure that fills  the width of the page:

    doc.add_figure('image.jpg', 'Optional Caption')

It's also nice to reduce your images before you insert them into your PDF.  Here's a simple resizing function that uses [Pillow](https://python-pillow.github.io/):

    bookletpdf.resize_image(in_jpg, out_jpg, width=None, height=None)

If both width and height are given, it will resize to that, otherwise it will respect the aspect ratio if only one is given.

## Graphs

The original purpose of `bookletpdf` was to draw graphs directly into a PDF document. `reportlab` provides a comprehensive vector-drawing canvas, which has been abstracted into a graphing module through the `Graph` object:

    graph = booklet.Graph()

It provides simple transforms from data to screen coordinates `x_to_i` and `y_toj`, and includes a simple axis with labels. 

The `Graph` provided in `bookletpdf` is simple and is designed to be extended  for your own drawing purposes. To do so, import the [reportlab drawing primitives](http://www.reportlab.com/apis/reportlab/2.4/graphics.html#module-reportlab.graphics.shapes) from `reportlab.graphics.shapes`. These can be added to `Graph` via:

    graph.flowable.add(primitive)

Once the graph has been drawn, you can just add this to the document:

    doc.elements.append(graph.flowable)

As an example, a vertical line drawer is included `add_vert_line`, which is used  in `booklet1.py`.


