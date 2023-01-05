# YINL Specification

This document specifies the YINL format. YINL files are UTF-8 encoded plain text files with a `.yi` or `.yinl` extension. It is intended that the YINL format be human-readable and writable, but also be compilable into a document. 

Throughout this document content encapsulated in angle brackets (`<` and `>`) should be treated as a place-holder value.

YINL files are broken into three major parts, the `header`, body, and `footer`. 

## Header

In the `header` the following information may be specified

- `title` The title of the document
- `author` The author(s) of the document
- `date` The date of the document
- `institute` The institute(s) of the author(s)
- `citations` The citation style to be used in the document

Each of these fields may be specified with the following syntax:

```
header:
    ...
    <field>:
        <content>
    ...
```

## Body

The body is divided into sections using the section keyword. A section has the following syntax, with `<content>` potentially beginning on the same line:

```
section <title>:
    <content>
```

It is permitted that the `<content>` of a `section` may contain further `section`s, encapsulated `section`s will be treated as a subsection of the original `section` and styled accordingly.

### Macros

The body can also contain macros with the following syntax

```
<macro-name>: (<arg1>, <arg2>, ...)
```

The common YINL macros are listed below, further macros can be defined in the document `footer` with Python

- `anchor: (<identifier>)` Defines a point to which a link can point
- `link: (<identifier>, <text>)` Defines a link to an anchor with the given `<text>`
- `figure: (<path>, <caption>)` Produces a figure with the given `<path>` and `<caption>`

### Short-hands

Short-hands are also available, and are defined in the document footer. A shorthand follows the syntax and will be replaced by the content specified in the `footer`

```
\short-hand-name
```

## Footer

The `footer` may contain three further sections describing `citations`, custom `macros`, and `shorthands`. 

### Citations

Citations are produced in the footer with the following syntax

```
footer:
    ...
    citations:
        <identifier>: <author>, <title>, <year>
        ...
    ...
```

### Macros

Custom macros can be defined using Python, the following syntax is used in the footer of the document

```
footer:
    ...
    macros:
        <macro-name>: (<arg1>, <arg2>, ...)
            <python>
        ...
    ...
```

The return value from the python code will be used as the output of the macro upon compilation.

### Short-hands

Short-hands are defined in the footer as follows

```
footer:
    ...
    shorthands:
        <short-hand>: <content>
        ...
    ...
```

## Example

An example of a simple YINL file is given below to demonstrate the syntax

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
        y: YINL
```