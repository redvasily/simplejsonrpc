# -*- coding: utf8 -*-

import unittest
import datetime
import simplejson

from encoders import SafeEncoder
from decoders import SafeDecoder


class SafeCodecTest(object):
    data = {
        'date': (
            datetime.date(2009, 1, 2),
            '{"__jsonclass__": ["date", 2009, 1, 2]}',
        ),
        'datetime': (
            datetime.datetime(2009, 1, 2, 3, 4, 5, 6),
            '{"__jsonclass__": ["datetime", 2009, 1, 2, 3, 4, 5, 6]}',
        ),
        'unicode-ascii': (
            u'Абвг',
            r'"\u0410\u0431\u0432\u0433"',
        ),
        'unicode-utf8': (
            u'Абвг',
            '"Абвг"',
        ),
        'int': (
            1,
            '1',
        ),
        'dict': (
            {'a': 'b'},
            '{"a": "b"}',
        ),
    }

    def testDate(self):
        self.doTest('date')

    def testDatetime(self):
        self.doTest('datetime')

    def testUnicode(self):
        self.doTest('unicode-utf8')

    def testInt(self):
        self.doTest('int')

    def testDict(self):
        self.doTest('dict')


class SafeEncoderTest(unittest.TestCase, SafeCodecTest):
    def doTest(self, type_, encoder=None):
        encoder = encoder or SafeEncoder()
        obj, json = self.data[type_]
        dout = encoder.encode(obj)
        self.assertEqual(dout, json)

    def testUnicodeAsciiEncoding(self):
        self.doTest('unicode-ascii', encoder=SafeEncoder(utf8_output=False))
        

class SafeDecoderTest(unittest.TestCase, SafeCodecTest):
    def doTest(self, type_, decoder=None):
        decoder = decoder or SafeDecoder()
        obj, json = self.data[type_]
        dout = decoder.decode(json)
        self.assertEqual(obj, dout)

    def testUnicodeAsciiEncoding(self):
        self.doTest('unicode-ascii')

