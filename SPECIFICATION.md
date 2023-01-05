# YINL Specification

This document specifies the YINL format. YINL files are UTF-8 encoded plain text files with a `.yi` or `.yinl` extension. It is intended that the YINL format be human-readable and writable, but also be compilable into a document. 

Please note that throughout this document, content appearing in `<` and `>` is acting as a place-holder for user-generated content and when used should be replaced in full.

YINL files are broken into sections with the `section` keyword. A section has the following syntax, `<content>` may begin on the same line

```
section <title>:
    <content>
```

Furthermore, a number of special types of section can be defined with following alternative keywords

- `title` The title of the document
- `author` The author(s) of the document
- `date` The date of the document

In addition to `section` and special types of `section`, YINL files can also contain macros with the following syntax:

```
<macro-name>: (<arg1>, <arg2>, ...)
```

The common YINL macros are listed below

- `anchor: (<identifier>)` Defines a point to which a link can point
- `link: (<identifier>, <text>)` Defines a link to an anchor
- `cite: (<author>, <year>, <title>, <link>)` Defines a citation to be used in the `citations` section
- `citations: (<style>)` Produces a section containing citations, `<style>` is the style of the citations, e.g. `ieee`
- `figure: (<path>, <caption>)` Produces a figure with the given `<path>` and `<caption>`

An example of a simple YINL file is given below for clarity

```
title:
    YINL Specification
author:
    J. L. Hay
date:
    2023-04-01

section Introduction:

    This document introduces the specification for the YINL format.

    section Why YINL?: anchor: (why-yinl)
        This is a subsection describing why YINL was created. It is also has an anchor so it can b

    figure: (/path/to/img.png, Figure 1 - An example figure) anchor: (fig1)

    How about a citation now? cite: (J. L. Hay, 2023, YINL Specification), and a link to the why YINL section link: (why-yinl, link text)

citations: (ieee)
```