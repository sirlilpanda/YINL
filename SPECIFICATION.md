# YINL Specification

This document specifies the YINL format. YINL files are UTF-8 encoded plain text files with a `.yi` or `.yinl` extension. It is intended that the YINL format be human-readable and writable, but also be compilable into a document. 

Please note that throughout this document, content appearing in `<` and `>` is acting as a place-holder for user-generated content and when used should be replaced in full.

YINL files are broken into three major parts, the `header`, body, and `footer`. In the `header` the following information may be specified

- `title` The title of the document
- `author` The author(s) of the document
- `date` The date of the document
- `institute` The insitute(s) of the author(s)
- `citations` The citation style to be used in the document

The body is broken into sections with the `section` keyword. A section has the following syntax, `<content>` may begin on the same line

```
section <title>:
    <content>
```

the body can also contain macros with the following syntax:

```
<macro-name>: (<arg1>, <arg2>, ...)
```

The common YINL macros are listed below, further macros can be defined in the document footer with Python

- `anchor: (<identifier>)` Defines a point to which a link can point
- `link: (<identifier>, <text>)` Defines a link to an anchor with the given `<text>`
- `figure: (<path>, <caption>)` Produces a figure with the given `<path>` and `<caption>`

Shorthands are also available for advanced users, and are defined in the document footer. A shorthand follows the syntax:

```
\short-hand-name
```

The `footer` may contain three further sections describing `citations`, custom `macros`, and `shorthands`.

An example of a simple YINL file is given below for clarity

```
header:
    title:
        YINL Specification
    author:
        J. Doe
    date:
        2023-04-01
    institute:
        University of New Zealand
    citations:
        IEEE

section Introduction:

    This document introduces the specification for the YINL format.

    section Why YINL?: anchor: (why-yinl)
        This is a subsection describing why YINL was created. It is also has an anchor so it can be linked to

    figure: (/path/to/img.png, Figure 1 - An example figure) anchor: (fig1)

    How about a citation now? cite: (dnorman13), and a link to the why \y section link: (why-yinl, link text)

footer:
    citations:
        dnorman13: D. A. Norman, The Design of Everyday Things. (Revis and expand ed.) 2013.
    macros:
        example_macro: (argument)
            <python>
    shorthands:
        \y: YINL
```