#!/usr/bin/env python3
# © 2015 James R. Barlow: github.com/jbarlow83

from subprocess import Popen, PIPE
from decimal import Decimal
from math import hypot
import re
import sys
import PyPDF2 as pypdf
from collections import namedtuple

try:
    from math import isclose
except ImportError:
    def isclose(a, b, rel_tol=1e-9):
        "Python 3.4 does not have math.isclose()"
        diff = abs(b - a)
        return diff <= abs(rel_tol * b) or diff <= abs(rel_tol * a)

matrix_mult = pypdf.pdf.utils.matrixMultiply

FRIENDLY_COLORSPACE = {
    '/DeviceGray': 'gray',
    '/CalGray': 'gray',
    '/DeviceRGB': 'rgb',
    '/CalRGB': 'rgb',
    '/DeviceCMYK': 'cmyk',
    '/Lab': 'lab',
    '/ICCBased': 'icc',
    '/Indexed': 'index',
    '/Separation': 'sep',
    '/DeviceN': 'devn',
    '/Pattern': '-',
    '/G': 'gray',  # Abbreviations permitted in inline images
    '/RGB': 'rgb',
    '/CMYK': 'cmyk',
    '/I': 'index',
}

FRIENDLY_ENCODING = {
    '/CCITTFaxDecode': 'ccitt',
    '/DCTDecode': 'jpeg',
    '/JPXDecode': 'jpx',
    '/JBIG2Decode': 'jbig2',
    '/CCF': 'ccitt',  # Abbreviations permitted in inline images
    '/DCT': 'jpeg',
    '/AHx': 'asciihex',
    '/A85': 'ascii85',
    '/LZW': 'lzw',
    '/Fl': 'flate',
    '/RL': 'runlength'
}

FRIENDLY_COMP = {
    'gray': 1,
    'rgb': 3,
    'cmyk': 4,
    'lab': 3,
    'index': 1
}


UNIT_SQUARE = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _matrix_from_shorthand(shorthand):
    """Convert from PDF matrix shorthand to full matrix

    PDF 1.7 spec defines a shorthand for describing the entries of a matrix
    since the last column is always (0, 0, 1).
    """

    a, b, c, d, e, f = map(float, shorthand)
    return ((a, b, 0),
            (c, d, 0),
            (e, f, 1))


def _shorthand_from_matrix(matrix):
    """Convert from transformation matrix to PDF shorthand."""
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    e, f = matrix[2][0], matrix[2][1]
    return tuple(map(float, (a, b, c, d, e, f)))


def _is_unit_square(shorthand):
    values = map(float, shorthand)
    pairwise = zip(values, UNIT_SQUARE)
    return all([isclose(a, b, rel_tol=1e-3) for a, b in pairwise])

XobjectSettings = namedtuple('XobjectSettings',
    ['name', 'shorthand', 'stack_depth'])

InlineSettings = namedtuple('InlineSettings',
    ['settings', 'shorthand', 'stack_depth'])

ContentsInfo = namedtuple('ContentsInfo', ['xobject_settings', 'inline_images'])


def _normalize_stack(operations):
    """Fix runs of qQ's in the stack

    For some reason PyPDF2 converts runs of qqq, QQ, QQQq, etc. into single
    operations.  Break this silliness up and issue each stack operation
    individually so we don't lose count.

    """
    for operands, command in operations:
        if re.match(br'Q*q+$', command):   # Zero or more Q, one or more q
            for char in command:           # Split into individual bytes
                yield ([], bytes([char]))  # Yield individual bytes
        else:
            yield (operands, command)


def _interpret_contents(contentstream, initial_shorthand=UNIT_SQUARE):
    """Interpret the PDF content stream

    The stack represents the state of the PDF graphics stack.  We are only
    interested in the current transformation matrix (CTM) so we only track
    this object; a full implementation would need to track many other items.

    The CTM is initialized to the mapping from user space to device space.
    PDF units are 1/72".  In a PDF viewer or printer this matrix is initialized
    to the transformation to device space.  For example if set to
    (1/72, 0, 0, 1/72, 0, 0) then all units would be calculated in inches.

    Images are always considered to be (0, 0) -> (1, 1).  Before drawing an
    image there should be a 'cm' that sets up an image coordinate system
    where drawing from (0, 0) -> (1, 1) will draw on the desired area of the
    page.

    PDF units suit our needs so we initialize ctm to the identity matrix.

    PyPDF2 replaces inline images with a fake "INLINE IMAGE" operator.

    """

    operations = contentstream.operations
    stack = []
    ctm = _matrix_from_shorthand(initial_shorthand)
    xobject_settings = []
    inline_images = []

    for n, op in enumerate(_normalize_stack(operations)):
        operands, command = op
        if command == b'q':
            stack.append(ctm)
            if len(stack) > 32:
                raise RuntimeError(
                    "PDF graphics stack overflow, command %i" % n)
        elif command == b'Q':
            try:
                ctm = stack.pop()
            except IndexError:
                raise RuntimeError(
                    "PDF graphics stack underflow, command %i" % n)
        elif command == b'cm':
            ctm = matrix_mult(
                _matrix_from_shorthand(operands), ctm)
        elif command == b'Do':
            image_name = operands[0]
            settings = XobjectSettings(
                name=image_name, shorthand=_shorthand_from_matrix(ctm),
                stack_depth=len(stack))
            xobject_settings.append(settings)
        elif command == b'INLINE IMAGE':
            settings = operands['settings']
            inline = InlineSettings(
                settings=settings, shorthand=_shorthand_from_matrix(ctm),
                stack_depth=len(stack))
            inline_images.append(inline)

    return ContentsInfo(
        xobject_settings=xobject_settings,
        inline_images=inline_images)


def _get_dpi(ctm_shorthand, image_size):
    """Given the transformation matrix and image size, find the image DPI.

    PDFs do not include image resolution information within image data.
    Instead, the PDF page content stream describes the location where the
    image will be rasterized, and the effective resolution is the ratio of the
    pixel size to raster target size.

    Normally a scanned PDF has the paper size set appropriately but this is
    not guaranteed. The most common case is a cropped image will change the
    page size (/CropBox) without altering the page content stream. That means
    it is not sufficient to assume that the image fills the page, even though
    that is the most common case.

    A PDF image may be scaled (always), cropped, translated, rotated in place
    to an arbitrary angle (rarely) and skewed. Only equal area mappings can
    be expressed, that is, it is not necessary to consider distortions where
    the effective DPI varies with position.

    To determine the image scale, transform an offset axis vector v0 (0, 0),
    width-axis vector v0 (1, 0), height-axis vector vh (0, 1) with the matrix,
    which gives the dimensions of the image in PDF units. From there we can
    compare to actual image dimensions. PDF uses
    row vector * matrix_tranposed unlike the traditional
    matrix * column vector.

    The offset, width and height vectors can be combined in a matrix and
    multiplied by the transform matrix. Then we want to calculated
        magnitude(width_vector - offset_vector)
    and
        magnitude(height_vector - offset_vector)

    When the above is worked out algebraically, the effect of translation
    cancels out, and the vector magnitudes become functions of the nonzero
    transformation matrix indices. The results of the derivation are used
    in this code.

    pdfimages -list does calculate the DPI in some way that is not completely
    naive, but it does not get the DPI of rotated images right, so cannot be
    used anymore to validate this. Photoshop works, or using Acrobat to
    rotate the image back to normal.

    It does not matter if the image is partially cropped, or even out of the
    /MediaBox.

    """

    a, b, c, d, _, _ = ctm_shorthand

    # Calculate the width and height of the image in PDF units
    image_drawn_width = hypot(a, b)
    image_drawn_height = hypot(c, d)

    # The scale of the image is pixels per PDF unit (1/72")
    scale_w = image_size[0] / image_drawn_width
    scale_h = image_size[1] / image_drawn_height

    # DPI = scale * 72
    dpi_w = scale_w * 72.0
    dpi_h = scale_h * 72.0

    return (dpi_w, dpi_h)


def _find_inline_images(contentsinfo):
    "Find inline images in the contentstream"

    for n, inline in enumerate(contentsinfo.inline_images):
        image = {}
        image['name'] = str('inline-%02d' % n)
        image['width'] = inline.settings['/W']
        image['height'] = inline.settings['/H']
        if '/BPC' in inline.settings:
            image['bpc'] = inline.settings['/BPC']
        else:
            image['bpc'] = 8
        if '/CS' in inline.settings:
            image['color'] = FRIENDLY_COLORSPACE.get(inline.settings['/CS'], '-')
        else:
            image['color'] = '-'
        image['comp'] = FRIENDLY_COMP.get(image['color'], '?')
        if '/F' in inline.settings:
            filter_ = inline.settings['/F']
            if isinstance(filter_, pypdf.generic.ArrayObject):
                filter_ = filter_[0]
            image['enc'] = FRIENDLY_ENCODING.get(filter_, 'image')
        else:
            image['enc'] = 'image'

        dpi_w, dpi_h = _get_dpi(
            inline.shorthand, (image['width'], image['height']))
        image['dpi_w'], image['dpi_h'] = Decimal(dpi_w), Decimal(dpi_h)
        yield image


def _image_xobjects(container):
    """Search for all XObject-based images in the container

    Usually the container is a page, but it could also be a Form XObject
    that contains images. Filter out the Form XObjects which are dealt with
    elsewhere.

    Generate a sequence of tuples (image, xobj container), where container,
    where xobj is the name of the object and image is the object itself,
    since the object does not know its own name.

    """

    if '/Resources' not in container:
        return
    resources = container['/Resources']
    if '/XObject' not in resources:
        return
    for xobj in resources['/XObject']:
        candidate = resources['/XObject'][xobj]
        if candidate['/Subtype'] == '/Image':
            image = candidate
            yield (image, xobj)


def _find_regular_images(container, contentsinfo):
    """Find images stored in the container's /Resources /XObject

    Usually the container is a page, but it could also be a Form XObject
    that contains images.

    Generates images with their DPI at time of drawing.

    """

    for pdfimage, xobj in _image_xobjects(container):
        image = {}
        image['name'] = xobj
        image['width'] = pdfimage['/Width']
        image['height'] = pdfimage['/Height']
        if '/BitsPerComponent' in pdfimage:
            image['bpc'] = pdfimage['/BitsPerComponent']
        else:
            image['bpc'] = 8

        # Fixme: this is incorrectly treats explicit masks as stencil masks,
        # but good enough for now. Explicit masks have /ImageMask true but are
        # never called for in content stream, instead are drawn as a /Mask on
        # other images. For our purposes finding out the details of /Mask
        # will seldom matter.
        if '/ImageMask' in pdfimage:
            image['type'] = 'stencil' if pdfimage['/ImageMask'].value \
                            else 'image'
        else:
            image['type'] = 'image'
        if '/Filter' in pdfimage:
            filter_ = pdfimage['/Filter']
            if isinstance(filter_, pypdf.generic.ArrayObject):
                filter_ = filter_[0]
            image['enc'] = FRIENDLY_ENCODING.get(filter_, 'image')
        else:
            image['enc'] = 'image'
        if '/ColorSpace' in pdfimage:
            cs = pdfimage['/ColorSpace']
            if isinstance(cs, pypdf.generic.ArrayObject):
                cs = cs[0]
            image['color'] = FRIENDLY_COLORSPACE.get(cs, '-')
        else:
            image['color'] = 'jpx' if image['enc'] == 'jpx' else '?'

        image['comp'] = FRIENDLY_COMP.get(image['color'], '?')

        # Bit of a hack... infer grayscale if component count is uncertain
        # but encoding must be monochrome. This happens if a monochrome image
        # has an ICC profile attached. Better solution would be to examine
        # the ICC profile.
        if image['comp'] == '?' and image['enc'] in ('ccitt', 'jbig2'):
            image['comp'] = FRIENDLY_COMP['gray']

        image['dpi_w'] = image['dpi_h'] = 0

        for xobj in contentsinfo.xobject_settings:
            # Loop in case the same image is display multiple times on a page
            if xobj.name != image['name']:
                continue

            if xobj.stack_depth == 0 and _is_unit_square(xobj.shorthand):
                # At least one PDF in the wild (and test suite) draws an image
                # when the graphics stack depth is 0, meaning that the image
                # gets drawn into a square of 1x1 PDF units (or 1/72",
                # or 0.35 mm).  The equivalent DPI will be >100,000.  Exclude
                # these from our DPI calculation for the page.
                continue

            dpi_w, dpi_h = _get_dpi(
                xobj.shorthand, (image['width'], image['height']))

            # When image is used multiple times take the highest DPI it is
            # rendered at
            image['dpi_w'] = max(dpi_w, image.get('dpi_w', 0))
            image['dpi_h'] = max(dpi_h, image.get('dpi_h', 0))

        DPI_PREC = Decimal('1.000')
        dpi = Decimal(image['dpi_w'] * image['dpi_h']).sqrt()
        image['dpi_w'] = Decimal(image['dpi_w']).quantize(DPI_PREC)
        image['dpi_h'] = Decimal(image['dpi_h']).quantize(DPI_PREC)
        image['dpi'] = dpi.quantize(DPI_PREC)
        yield image


def _find_form_xobject_images(pdf, container, contentsinfo):
    """Find any images that are in Form XObjects in the container

    The container may be a page, or a parent Form XObject.

    """
    if '/Resources' not in container:
        return
    resources = container['/Resources']
    if '/XObject' not in resources:
        return
    for xobj in resources['/XObject']:
        candidate = resources['/XObject'][xobj]
        if candidate['/Subtype'] != '/Form':
            continue

        form_xobject = candidate
        for settings in contentsinfo.xobject_settings:
            if settings.name != xobj:
                continue

            # Find images once for each time this Form XObject is drawn.
            # This could be optimized to cache the multiple drawing events
            # but in practice both Form XObjects and multiple drawing of the
            # same object are both very rare.
            ctm_shorthand = settings.shorthand
            yield from _find_images(pdf, form_xobject, ctm_shorthand)


def _find_images(pdf, container, shorthand=None):
    """Find all individual instances of images drawn in the container

    Usually the container is a page, but it may also be a Form XObject.

    On a typical page images are stored inline or as regular images
    in an XObject.

    Form XObjects may include inline images, XObject images,
    and recursively, other Form XObjects; and also vector drawing commands.

    Every instance of an image being drawn somewhere is flattened and
    treated as a unique image, since if the same image is drawn multiple times
    on one page it may be drawn at differing resolutions, and our objective
    is to find the resolution at which the page can be rastered without
    downsampling.

    """

    if container.get('/Type') == '/Page':
        # For a /Page the content stream is attached to the page's /Contents
        page = container
        contentstream = pypdf.pdf.ContentStream(page.getContents(), pdf)
        initial_shorthand = shorthand or UNIT_SQUARE
    elif container.get('/Type') == '/XObject' and \
            container['/Subtype'] == '/Form':
        # For a Form XObject that content stream is attached to the XObject
        contentstream = pypdf.pdf.ContentStream(container, pdf)

        # Set the CTM to the state it was when the "Do" operator was
        # encountered that is drawing this instance of the Form XObject
        ctm = _matrix_from_shorthand(shorthand or UNIT_SQUARE)

        # A Form XObject may provide its own matrix to map form space into
        # user space. Get this if one exists
        form_matrix = _matrix_from_shorthand(
                container.get('/Matrix', UNIT_SQUARE))

        # Concatenate form matrix with CTM to ensure CTM is correct for
        # drawing this instance of the XObject
        ctm = matrix_mult(form_matrix, ctm)
        initial_shorthand = _shorthand_from_matrix(ctm)
    else:
        return

    contentsinfo = _interpret_contents(contentstream, initial_shorthand)

    yield from _find_inline_images(contentsinfo)
    yield from _find_regular_images(container, contentsinfo)
    yield from _find_form_xobject_images(pdf, container, contentsinfo)


def _page_has_text(pdf, page):
    # Simple test
    text = page.extractText()
    if text.strip() != '':
        return True

    # More nuanced test to deal with quirks of Tesseract PDF generation
    # Check if there's a Glyphless font
    try:
        font = page['/Resources']['/Font']
    except KeyError:
        pass
    else:
        font_objects = list(font.keys())
        for font_object in font_objects:
            basefont = font[font_object]['/BaseFont']
            if basefont.endswith('GlyphLessFont'):
                return True

    return False


def _pdf_get_pageinfo(infile, pageno: int):
    pageinfo = {}
    pageinfo['pageno'] = pageno
    pageinfo['images'] = []

    pdf = pypdf.PdfFileReader(infile)
    page = pdf.pages[pageno]

    pageinfo['has_text'] = _page_has_text(pdf, page)

    width_pt = page.mediaBox.getWidth()
    height_pt = page.mediaBox.getHeight()
    pageinfo['width_inches'] = width_pt / Decimal(72.0)
    pageinfo['height_inches'] = height_pt / Decimal(72.0)

    try:
        pageinfo['rotate'] = int(page['/Rotate'])
    except KeyError:
        pageinfo['rotate'] = 0

    pageinfo['images'] = [im for im in
                          _find_images(pdf, page)]
    if pageinfo['images']:
        xres = max(image['dpi_w'] for image in pageinfo['images'])
        yres = max(image['dpi_h'] for image in pageinfo['images'])
        pageinfo['xres'], pageinfo['yres'] = xres, yres
        pageinfo['width_pixels'] = \
            int(round(xres * pageinfo['width_inches']))
        pageinfo['height_pixels'] = \
            int(round(yres * pageinfo['height_inches']))

    return pageinfo


def pdf_get_all_pageinfo(infile):
    pdf = pypdf.PdfFileReader(infile)
    return [_pdf_get_pageinfo(infile, n) for n in range(pdf.numPages)]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()
    info = pdf_get_all_pageinfo(args.infile)
    from pprint import pprint
    pprint(info)


if __name__ == '__main__':
    main()
