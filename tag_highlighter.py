import cgi
from collections import defaultdict
from HTMLParser import HTMLParser

def _wrap_tag(tag):
    return ('<code class=\"highlightable-tag tag-%s">%s</code>' %
            (tag, cgi.escape(tag)))

def _wrap_attrs(attrs):
    wrapped = ''
    if attrs:
        for key, value in attrs:
            wrapped += ' ' + key
            if value:
                wrapped += '="%s"' % value
    return cgi.escape(wrapped)

def _enclose_in_angle_brackets(string):
    return cgi.escape('<') + string + cgi.escape('>')

class TagHighlighter(HTMLParser):

    def __init__(self, html):
        HTMLParser.__init__(self)

        self.formatted_html = []
        self.tag_to_count = defaultdict(int)
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(
            _enclose_in_angle_brackets(_wrap_tag(tag) + _wrap_attrs(attrs)))

    def handle_endtag(self, tag):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(_enclose_in_angle_brackets(_wrap_tag(tag)))

    def handle_startendtag(self, tag, attrs):
        self.tag_to_count[tag] += 1
        self.formatted_html.append(_enclose_in_angle_brackets(
            _wrap_tag(tag) + _wrap_attrs(attrs) + cgi.escape(" /")))

    def handle_data(self, data):
        self.formatted_html.append(cgi.escape(data))

    def handle_entityref(self, name):
        self.formatted_html.append(cgi.escape(name))

    def handle_charref(self, name):
        self.formatted_html.append(cgi.escape(name))

    def handle_comment(self, data):
        self.formatted_html.append(cgi.escape(data))

    def handle_decl(self, decl):
        self.formatted_html.append(
            _enclose_in_angle_brackets(cgi.escape("!" + decl)))

    def handle_pi(self, data):
        self.formatted_html.append(cgi.escape("?" + data))

    def unknown_decl(self, data):
        self.formatted_html.append(
            _enclose_in_angle_brackets(cgi.escape("![" + data + "]")))
