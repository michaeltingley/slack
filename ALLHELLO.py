# import cgi
# import urllib2
# from collections import defaultdict
# from HTMLParser import HTMLParser

# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # class TagFinder(HTMLParser):

# #     def __init__(self, html):
# #         HTMLParser.__init__(self)

# #         self.tag_and_line_and_offset = []
# #         self.feed(html)

# #     def handle_starttag(self, tag, attrs):
# #         self.tag_and_line_and_offset.append(
# #             (tag, self.getpos()[0], self.getpos()[1])
# #         )
# #         # print "Encountered a start tag:", self.getpos(), tag, attrs, self.get_starttag_text()
# #     # def handle_endtag(self, tag):
# #     #     print "Encountered an end tag :", self.getpos(), tag
# #     # def handle_data(self, data):
# #     #     print "Encountered some data  :", data

# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # @app.route('/parse_url', methods=['POST'])
# # def parse_url():
# #     request_url = request.form['fetch_url']
# #     fetched_html = urllib2.urlopen(request_url).read()

# #     print fetched_html
# #     formatted_html = enrich(
# #         fetched_html.split("\n"), 
# #         TagFinder(fetched_html).tag_and_line_and_offset
# #     )
# #     print formatted_html
# #     return jsonify(fetched_html=formatted_html)

# # def enrich(html_lines, tag_and_line_and_offset):
# #     print tag_and_line_and_offset
# #     for tag, line, offset in reversed(tag_and_line_and_offset):
# #         html_lines[line - 1] = \
# #             updated_line(html_lines[line - 1], tag, offset + 1)

# #     return "<pre>" + "\n".join(html_lines) + "</pre>"

# # def updated_line(html_line, tag, tag_start_index):
# #     return (
# #         html_line[:tag_start_index] +
# #         "</pre><pre class=\"tag-" + tag + "\">" +
# #         html_line[tag_start_index:tag_start_index + len(tag)] +
# #         "</pre><pre>" +
# #         html_line[tag_start_index + len(tag)]
# #     )

# def wrap_tag(tag):
#     return "<code class=\"tag-" + tag + "\">" + cgi.escape(tag) + "</code>"

# def wrap_attrs(attrs):
#     return (
#         " " + cgi.escape(" ".join([k + "=\"" + v + "\"" for k, v in attrs]))
#         if attrs else ""
#     )

# def enclose_in_angle_brackets(string):
#     return cgi.escape("<") + string + cgi.escape(">")

# class TagHighlighter(HTMLParser):

#     def __init__(self, html):
#         HTMLParser.__init__(self)

#         self.indent_level = 0
#         self.formatted_html = []
#         self.tag_to_count = defaultdict(int)
#         self.feed(html)

#     def handle_starttag(self, tag, attrs):
#         self.tag_to_count[tag] += 1
#         self.formatted_html.append(
#             enclose_in_angle_brackets(wrap_tag(tag) + wrap_attrs(attrs))
#         )
#     def handle_endtag(self, tag):
#         self.tag_to_count[tag] += 1
#         self.formatted_html.append(enclose_in_angle_brackets(wrap_tag(tag)))
#     def handle_startendtag(self, tag, attrs):
#         self.tag_to_count[tag] += 1
#         self.formatted_html.append(enclose_in_angle_brackets(
#             wrap_tag(tag) + wrap_attrs(attrs) + cgi.escape(" /")
#         ))
#     def handle_data(self, data):
#         self.formatted_html.append(cgi.escape(data))
#     # def handle_entityref(self, name):
#     #     self.formatted_html.append(cgi.escape(name))
#     # def handle_charref(self, name):
#     #     self.formatted_html.append()
#     def handle_comment(self, data):
#         self.formatted_html.append(cgi.escape(data))
#     def handle_decl(self, decl):
#         self.formatted_html.append(
#             enclose_in_angle_brackets(cgi.escape("!" + decl))
#         )
#     def handle_pi(self, data):
#         self.formatted_html.append(cgi.escape("?" + data))
#     def unknown_decl(self, data):
#         self.formatted_html.append(
#             enclose_in_angle_brackets(cgi.escape("![" + data + "]"))
#         )

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/parse_url', methods=['POST'])
# def parse_url():
#     request_url = request.form['fetch_url']
#     fetched_html = urllib2.urlopen(request_url).read()

#     result = TagHighlighter(fetched_html)
#     print "".join(result.formatted_html)
#     return jsonify(
#         formatted_html="".join(result.formatted_html),
#         tag_to_count=result.tag_to_count
#     )

# if __name__ == '__main__':
#     app.run(debug=True)




