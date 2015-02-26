

# bookletpdf

Bookletpdf simplifies the building of PDF's with table-of-contents, page numbers, figures and graphs.

## Installation

From github:

	git clone http://github.com/boscoh/bookletpdf

## Why?

It's based on the mighty reportlab, which is powerful but somewhat difficult to get started with. Reportlab provides a PDF renderer and a powerful but complicated document manager. You need to understand both well to get started. 

For instance, to get a Table of Contents (TOC), you have to subclass the document manager to handle flowables that you want to add to the TOC. Then the flowable has to be added to your elements. This you have to feed into your document manager. It's just lots and lots of details.

Bookletpdf abstracts both the renderer and document manager into a single object.

This really ought to be collected in an object.

## The Main Object
- initialize
- build

## Page Templates
- Title page
- Numbered page

## Table of Contents
- Chapters

## Page Breaks, Footers and Pages

## Paragraphs and Styles

## Figures 

## Graphs
- Spectra Graph




