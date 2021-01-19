from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from changes.forms import SponsorForm


class TestSponsorForm(TestCase):
    """Test uploading SVG file"""

    def setUp(self):
        svg = ('<?xml version="1.0" standalone="no"?>'
               '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"'
               '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'
               '<svg version="1.0" xmlns="http://www.w3.org/2000/svg"'
               'width="32.000000pt" height="32.000000pt" viewBox="0 0 '
               '32.000000 32.000000"'
               'preserveAspectRatio="xMidYMid meet"' >
               ''
               '<g transform="translate(0.000000,32.000000) '
               'scale(0.100000,-0.100000)"'
               'fill="#000000" stroke="none">'
               '<path d="M95 291 c-41 -18 -77 -68 -82 -113 -10 '
               '-99 84 -178 183 -154 25 7 26'
               '8 9 26 -11 12 -31 20 -50 20 -47 0 -85 41 -85 92 '
               '0 51 43 98 90 98 44 0 90'
               '-47 90 -93 0 -34 33 -78 48 -63 4 4 7 32 7 62 0 49'
               ' -3 57 -37 91 -33 33 -43'
               '37 -95 40 -32 1 -67 -1 -78 -6z"/>'
               '<path d="M140 156 c0 -13 7 -29 15 -36 13 -10 15 -9 '
               '15 9 0 13 6 21 16 21 14'
               '0 14 3 4 15 -20 24 -50 19 -50 -9z"/>'
               '<path d="M190 107 c0 -32 59 -87 93 -87 39 0 35 25 -12 '
               '71 -44 45 -81 52 -81'
               '16z"/>'
               '</g>'
               '</svg>')
        self.logo = SimpleUploadedFile('qgis.svg', svg)

    def test_form_with_svg_file(self):
        form = SponsorForm(data={})
        self.assertFalse(form.is_valid())
        data = {
            'name': u'New Test Sponsor',
        }
        file_data = {
            'logo': self.logo
        }
        form = SponsorForm(data, file_data)
        self.assertTrue(form.is_valid())
