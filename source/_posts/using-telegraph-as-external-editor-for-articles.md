---
title: Using Telegra.ph as external editor for articles
date: 2018-02-15 12:59:56
tags: [python, telegram, html, parser, grabber, urllib]
author: Misha Behersky
language: en
---

In this article I will show an interesting use case about using [telegraph](http://telegra.ph/) as external [wysiwyg](https://en.wikipedia.org/wiki/WYSIWYG) editor. Actually you can use this approach as a grabber from any resource or for parsing/converting html to different structure.

So, let's begin. We will be using Python 3 and just standard library without any third-party modules and extensions. The initial purpose is to grab desired html structure for the article and save images to serve them from our server.

First we need to download the page, [urllib](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) is on a duty

```python
from urllib import request
from urllib.parse import urljoin

response = request.urlopen(url).read().decode()
base_url = urljoin(url, '/')
```

After that we need to omit tags that will not be used, update their attributes or replace with another one. The tool for parsing the stucture is [html.parser](https://docs.python.org/3/library/html.parser.html)

```python
class ArticleParser(HTMLParser):

    def __init__(self, base_url):
        super().__init__()

        self.base_url = base_url
        self.resulting_html = ''
        self._appending = False
        self._data_buf = ''
        self._tags_stack = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
```

There are three main function each behaves as a callback when openning tag is encountered, closed tag is currently in the feed or data within a tag that is processing now. We will use stack to restore correct structure of the document and transorm it on the fly as needed. Flag appending shows whether we add data to the resulting document of skip it.

On image tag we need to download it first from remote url and function below will help us with that

```python
import os

...

IMAGES_DIR = 'images'

def download_file(self, path):
    filename = os.path.basename(path)
    filepath = os.path.join(self.IMAGES_DIR, filename)
    url = urljoin(self.base_url, path)
    request.urlretrieve(url, filename=filepath)
    return filename
```

And the full code of `handle_starttag` method

```python
def handle_starttag(self, tag, attrs):
    # We can omit anything we want, but make sure closing handles that as well
    if tag == 'br':
        return

    # Download images
    if tag == 'img':
        for attr, value in attrs:
            if attr == 'src':
                filename = self.download_file(value)
                new_url_path = os.path.join('/', self.IMAGES_DIR, filename)
                self.resulting_html += self._wrap_in_tag(
                    'figure', '<img src="{}" />'.format(new_url_path))
                return

    # Select tags we want to get in
    if tag in ('p', 'h3', 'blockquote'):
        self._appending = True

    self._tags_stack.append(tag)
```

Another helper method that we use is `wrap_in_tag`. It ensures that data will be properly enclosed within a tag

```python
@staticmethod
def _wrap_in_tag(tag, data):
    return '<{tag}>{data}</{tag}>'.format(tag=tag, data=data.lstrip())
```

Function for handling closing tag should be symmetrical to one the handles oppening like this

```python
def handle_endtag(self, tag):
    if tag == 'br':
        return

    if not self._tags_stack:
        raise ValueError('Open/closing tags are not balanced')

    current_tag = self._tags_stack.pop()

    if tag in ('p', 'h3', 'blockquote'):
        if current_tag != tag:
            raise ValueError('Invalid closing tag: %s. Current on stack: %s.', tag, current_tag)
        if self._data_buf:
            self.resulting_html += self._wrap_in_tag(current_tag, self._data_buf)

        self._appending = False
        self._data_buf = ''
```

Also this code does simple validation of balancing tags and shows errors if any.

Finally we are handling the data enclosed and append it to an intermediate buffer

```python
def handle_data(self, data):
    if self._appending:
       self._data_buf += data
```

The same result can be achieved with a help of regular expressions but that would be much complex and error prone. For example we can look up for a title to the article using such a helper method

```python
def find_tag(tag_name, html_data):
    exp = '<{tag_name}[^>]*>(.*?)</{tag_name}>'.format(tag_name=tag_name)
    m = re.search(exp, html_data)
    result = m.group(1)  # Match within a tag
    return result
```

### Summary

We have built a grabber + parser for articles to fetch and format them in a way we want evaluating only tools from standard library. You might extend this example adding different providers and that can be a tool for populating your own blog with aggregated articles from different resources. If you want to rely on more user-friendly libraries see links below.

### Resouces

* [Link to gist with full code](https://gist.github.com/bmwant/6aa277eb22093f619a9c59b0dde36152)
* [Parsing html with Beautiful Soup](http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/)
* [Making requests easily](http://www.pythonforbeginners.com/requests/using-requests-in-python)
