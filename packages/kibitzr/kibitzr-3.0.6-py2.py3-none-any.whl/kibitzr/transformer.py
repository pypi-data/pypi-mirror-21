"""
Built-in transforms
"""
import sys
import logging
import contextlib
import functools
import json
from lxml import etree

import six
from bs4 import BeautifulSoup
import sh
from lazy_object_proxy import Proxy as Lazy

from .storage import PageHistory


logger = logging.getLogger(__name__)
jq = Lazy(lambda: sh.jq.bake('--monochrome-output', '--raw-output'))


def pipeline_factory(conf):
    rules = conf.get('transform', [])
    if isinstance(rules, six.string_types):
        rules = [rules]
    return functools.partial(
        pipeline,
        transformers=[
            transformer_factory(conf, rule)
            for rule in rules
        ]
    )


def pipeline(ok, content, transformers):
    for transformer in transformers:
        if ok:
            ok, content = transformer(content)
        else:
            break
    return ok, content


def transformer_factory(conf, rule):
    try:
        name, value = next(iter(rule.items()))
    except AttributeError:
        name, value = rule, None
    if name == 'css':
        return functools.partial(css_selector, value)
    elif name == 'xpath':
        return functools.partial(xpath_selector, value)
    elif name == 'tag':
        return functools.partial(tag_selector, value)
    elif name == 'text':
        return extract_text
    elif name == 'changes':
        if value and value.lower() == 'verbose':
            return functools.partial(PageHistory(conf).report_changes,
                                     verbose=True)
        else:
            return PageHistory(conf).report_changes
    elif name == 'json':
        return pretty_json
    elif name == 'jq':
        return functools.partial(run_jq, value)
    elif name == 'sort':
        return sort_lines
    elif name == 'cut':
        return functools.partial(cut_lines, value)
    else:
        raise RuntimeError(
            "Unknown transformer: %r" % (name,)
        )


def pretty_json(text):
    json_dump = json.dumps(
        json.loads(text),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        # encoding='utf-8',
    )
    return True, u'\n'.join([
        line.rstrip()
        for line in json_dump.splitlines()
    ])


def tag_selector(name, html):
    with deep_recursion():
        soup = BeautifulSoup(html, "html.parser")
        element = soup.find(name)
        if element:
            return True, six.text_type(element)
        else:
            logger.warning('Tag not found: %r', name)
            return False, html


def css_selector(selector, html):
    with deep_recursion():
        soup = BeautifulSoup(html, "html.parser")
        try:
            element = soup.select(selector)[0]
            return True, six.text_type(element)
        except IndexError:
            logger.warning('CSS selector not found: %r', selector)
            return False, html


def xpath_selector(selector, html):
    root = etree.fromstring(html, parser=etree.HTMLParser())
    elements = root.xpath(selector)
    if elements:
        return True, etree.tostring(
            next(iter(elements)),
            method='html',
            pretty_print=True,
            encoding='unicode',
        )
    else:
        logger.warning('XPath selector not found: %r', selector)
        return False, html


def extract_text(html):
    with deep_recursion():
        strings = BeautifulSoup(html, "html.parser").stripped_strings
        return True, u'\n'.join([
            line
            for line in strings
            if line
        ])


def sort_lines(text):
    return True, u''.join([
        line + u'\n'
        for line in sorted(text.splitlines())
        if line
    ])


def cut_lines(last_line, text):
    return True, u''.join([
        line + u'\n'
        for line in text.splitlines()[:last_line]
    ])


def run_jq(query, text):
    logger.debug("Running jq query %s against %s", query, text)
    try:
        command = jq(query, _in=text)
        if not command.stderr:
            success, result = True, command.stdout.decode('utf-8')
        else:
            success, result = False, command.stderr.decode('utf-8')
    except sh.ErrorReturnCode as exc:
        logger.exception("jq failure")
        success, result = False, exc.stderr
    logger.debug("jq transform success: %r, content: %r",
                 success, result)
    return success, result


@contextlib.contextmanager
def deep_recursion():
    old_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(100000)
        yield
    finally:
        sys.setrecursionlimit(old_limit)
