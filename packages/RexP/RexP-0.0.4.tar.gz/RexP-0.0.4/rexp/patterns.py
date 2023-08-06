#!/usr/bin/python

import re

class Pattern(object):
    def escepable(self):
        return True

    def __call__(self, *args, **kwargs):
        return '' if not len(args) else re.escape(args[0])

class DateTimePattern(Pattern):
    WILDCARD_RE = re.compile(r'%(?P<c>((?!%)[a-zA-Z])|%)', re.IGNORECASE)

    def __init__(self):
        self.__wildcards = [
            ('d', r'(([0-2][0-9])|(3[01]))'),
            ('H', r'(([0-1][0-9])|(2[0-3]))'),
            ('I', r'((0[0-9])|(1[12]))'),
            ('m', r'((0[0-9])|(1[12]))'),
            ('M', r'([0-5][0-9])'),
            ('p', r'((AM)|(PM))'),
            ('S', r'(([0-5][0-9])|(6[0-1]))'),
            ('Y', r'((?:19|20)[0-9]{2})'),
            ('y', r'([0-9]{2})'),
            ('z', r'((-|\+)(([0-1][0-9])|(2[0-3])):([0-5][0-9]))'),
            ('%', r'(%)')
        ]

    def __call__(self, *args, **kwargs):
        if not len(args):
            raise ValueError('Invalid format')

        f = str(args[0])
        l = []
        for x in self.WILDCARD_RE.finditer(f):
            c = x.group('c')
            w = [x for x in self.__wildcards if x[0] == c]
            if len(w):
                l.append(w[0])

        for x in l:
            f = f.replace('%{0}'.format(x[0]), x[1])

        return f



class IPAddressPattern(Pattern):
    __V4_EXPR = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    __V6_EXPR = r'((([0-9A-Fa-f]{1,4}:){1,6}:)|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4})'

    def __call__(self, *args, **kwargs):
        if not len(args) or not re.match(r'^(v4)|(v6)$', args[0]):
            raise ValueError('Invalid IP address type!')

        return self.__V6_EXPR  if str(args[0]).lower() == 'v6' \
            else self.__V4_EXPR

class RegexPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        return args[0]

class RegexGroupPattern(Pattern):
    def __call__(self, *args, **kwargs):
        is_negative = kwargs['is_negative'] or False
        return '[%s%s]' % ('^' if is_negative else '', args[0])

class RegexNotPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        return '(?!%s)' % args[0]

class KeyValuePairPattern(Pattern):
    def escepable(self):
        return False

    def __call__(self, *args, **kwargs):
        sep = r'=' if not len(args) else args[0]
        esced = re.escape(sep)
        cn = kwargs['capture_name']
        return r'\b(?P<{1}key>[^{0}\s]+)\s*{0}\s*(?P<{1}value>[^{0}]+)[\b\,\;]'.format(
            sep if sep == esced else esced, '%s_' % cn if cn else '')

DEFAULT_PATTERN_SET = dict(
    RE=RegexPattern(),
    BEGIN=r'^',
    END=r'$',
    GR=RegexGroupPattern(),
    NOT=RegexNotPattern(),
    SPACE=r'\s',
    ANY=r'.',
    INT=r'\d+',
    NUM=r'(\d+([,\.]\d+)*)',
    CH="\w",
    STR=r'("["]+")|(\'[\'+]\')',
    WORD=r'\b\w+\b',
    WORDS=r'\b(\w+\s*)*\b',
    DATE=DateTimePattern(),
    IP=IPAddressPattern(),
    IP4='${IP(v4)}',
    IP6='${IP(v6)}',
    PAIR=KeyValuePairPattern()
)