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
- `subtitle` The subtitle of the document
- `author` The author(s) of the document
- `date` The date of the document
- `image` An image to be included in the document, `<content>` should be a path to the image and `<title>` may be an optional caption
- `citations` An automatically generated list of citations, `<content>` should be a citation style, see below for a list of supported citation styles

In addition to `section` and special types of `section`, YINL files can also contain macros with the following syntax:

```
<macro-name>: (<arg1>, <arg2>, ...)
```

There are three main macros used in YINL

- `anchor: (<identifier>)` Defines a point to which a link can point
- `link: (<identifier>)` Defines a link to an anchor
- `cite: (author, year, title, link)` Defines a citation to be used in the `citations` section