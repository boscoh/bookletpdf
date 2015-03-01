

# bookletpdf

Simplifies building a PDF in reportlab with TOC, pages, figures and graphs.

## Installation

From github:

	git clone http://github.com/boscoh/bookletpdf

## Why?

It's based on the mighty [`reportlab`](), which provides a PDF renderer and a complex document manager. You need to understand both to get started. 

For instance, to get a Table of Contents (TOC), you have to subclass the document manager to handle flowables to spy on potential TOC entries. Then you have to ensure the gathering of the correct flowable, before you funnel this through the Doc manager. Like I said, a ton of intricate details.

## The Main Object

Bookletpdf abstracts both the renderer and document manager into a single object.

This really ought to be collected in an object.
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




