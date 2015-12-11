"""The main application.

This application creates a Flask webserver intended to fetch and parse the html
content of other provided websites.
"""

from urllib2 import Request, HTTPError, URLError, urlopen
from flask import Flask, make_response, jsonify, render_template, request
import chardet

from tag_highlighter import TagHighlighter

app = Flask(__name__)

def try_urlopen(entered_url):
    """Attempts to open the user-entered url using urlopen.

    First attempts urlopen directly on the provided url. Returns the result if
    it succeeds. If a ValueError indicating that the page could not be found is
    produced, attempts again by prepending 'http://' to the requested url. If
    this also fails due to a ValueError, returns the *first* ValueError to the
    caller.

    Args:
        entered_url (str): The url to fetch as entered by the user.
    """
    try:
        return urlopen(Request(entered_url, headers={'User-Agent' : 'Robot'}))
    except ValueError as error:
        first_error = error
    try:
        return urlopen(
            Request('http://' + entered_url, headers={'User-Agent' : 'Robot'}))
    except ValueError as error:
        raise first_error

def get_encoding(http_message, encoded_html):
    """Computes and returns the encoding of the webpage.

    Attempts to determine the encoding of the provided webpage. First, attempts
    to read the specified encoding specified in the 'charset' header directly
    from the http message headers that were received when requesting the web
    page. If the headers do not contain an encoding, then uses the chardet
    module to attempt to infer the encoding based on examining the source of the
    page. Finally, if none of the above works, falls back to utf-8 as a
    reasonable default.

    Args:
        http_message (urllib.addinfourl): Response from urlopen containing
            metadata about the website.
        encoded_html (str): String of the encoded webpage html. Even though this
            can be determined from http_message, this must be provided so that
            the webpage's html does not get re-read by both this function and
            the caller.
    Returns:
        str: The encoding used for the webpage.
    """
    param_encoding = http_message.headers.getparam('charset')
    if param_encoding:
        return param_encoding
    chardet_encoding = chardet.detect(encoded_html)
    if chardet_encoding and 'encoding' in chardet_encoding:
        return chardet_encoding['encoding']
    return 'utf-8'

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/parse_url', methods=['POST'])
def parse_url():
    """Fetches the provided webpage, wraps its tags, and returns it.

    Attempts to fetch the webpage found in the form's fetch_url field. Marks up
    the source by escaping the fetched characters and wrapping tags in spans
    with a class attribute named 'tag-' followed by the name of the tag. Returns
    a JSON object containing the marked up source html and the tags.

    If there is an error fetching or decoding the webpage, returns an HTTP error
    with an error code and message indicating the nature of the issue.

    Returns:
        json: A JSON object containing:
            formatted_html (str): The marked up webpage
            tag_to_count (dict): Mappings from each tag name to the number
                encountered in the webpage
    """
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

    marked_up_html = TagHighlighter(html)
    return jsonify(
        formatted_html=''.join(marked_up_html.formatted_html),
        tag_to_count=marked_up_html.tag_to_count)

if __name__ == '__main__':
    app.run(debug=True)
