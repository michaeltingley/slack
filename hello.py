from urllib2 import Request, HTTPError, URLError, urlopen
from flask import Flask, make_response, jsonify, render_template, request
import chardet

from tag_highlighter import TagHighlighter

app = Flask(__name__)

def get_encoding(http_message, encoded_html):
    param_encoding = http_message.headers.getparam('charset')
    if param_encoding:
        return param_encoding
    chardet_encoding = chardet.detect(encoded_html)
    if chardet_encoding and 'encoding' in chardet_encoding:
        return chardet_encoding['encoding']
    return 'utf-8'

def try_urlopen(entered_url):
    try:
        return urlopen(Request(entered_url, headers={'User-Agent' : 'Robot'}))
    except ValueError as error:
        first_error = error
    try:
        return urlopen(
            Request('http://' + entered_url, headers={'User-Agent' : 'Robot'}))
    except ValueError as error:
        raise first_error

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse_url', methods=['POST'])
def parse_url():
    entered_url = request.form['fetch_url']
    try:
        http_message = try_urlopen(entered_url)
        encoded_html = http_message.read()
        html = encoded_html.decode(get_encoding(http_message, encoded_html))
    except ValueError:
        return make_response(
            'Could not read the HTML from %s. Please ensure that it is a valid '
            'URL.' % entered_url, 400)
    except HTTPError as error:
        return make_response(
            'The site %s rejected the attempt to read its html: %s.' %
            (entered_url, error.fp.read()), error.code)
    except URLError as error:
        return make_response(
            'The url %s could not be reached: %s.' %
            (entered_url, error.reason), 400)

    result = TagHighlighter(html)
    return jsonify(
        formatted_html=''.join(result.formatted_html),
        tag_to_count=result.tag_to_count)

if __name__ == '__main__':
    app.run(debug=True)
