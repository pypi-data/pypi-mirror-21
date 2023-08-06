#   Simplegen is a simple program to generate static sites
#   Copyright (C) 2016  Mohamed Aziz Knani

from __future__ import print_function
import sys
import glob
import os
import collections
sys.path.append(os.getcwd())
import markdown # noqa
import htmlmin # noqa
from six import PY2 # noqa
from datetime import datetime # noqa
from jinja2 import Environment, FileSystemLoader, exceptions as jexceptions # noqa
from sconfig import THEME_DIR # noqa
from colorama import init as colorama_init, Fore # noqa
from math import ceil # noqa
import shutil # noqa
from codecs import open as uopen # noqa


if PY2:
    reload(sys) # noqa
    sys.setdefaultencoding('utf8')

colorama_init(autoreset=True)

try:
    # dirty but needed to register to the environment scope
    from sconfig import * # noqa
except ImportError:
    pass


try:
    from sconfig import OUTPUT_DIR
    output_dir = OUTPUT_DIR
except ImportError:
    output_dir = 'output/'

try:
    from sconfig import CONTENT_DIR
    content_dir = CONTENT_DIR
except ImportError:
    content_dir = 'content/'

try:
    from sconfig import PAGINATOR_MAX
    per_page = PAGINATOR_MAX
except ImportError:
    per_page = 20

try:
    from sconfig import MINIFY_HTML
except ImportError:
    MINIFY_HTML = False

env = Environment(
    loader=FileSystemLoader(THEME_DIR))

# add the global variable scope to the environment scope
env.globals.update(globals())


##
# Markdown extensions should be inited here
##

from markdown.extensions.codehilite import CodeHiliteExtension # noqa
codehilite = CodeHiliteExtension(linenums=False)
md = markdown.Markdown(extensions=['markdown.extensions.meta', codehilite, 'markdown.extensions.tables', 'mdx_math'])


##
# Helper functions
##


def find_content(content_dir):
    """
    Returns all markdown files.

    Keyword Arguments:
    content_dir -- the path of the content to make.
    """

    return sorted(glob.glob(os.path.join(content_dir, '*.md')))


def compile_html(content_path):
    """
    Actually compiles the markdown into html files and minfies them.
    Returns a tuple of minfied html and the markdown metadata.

    Keyword Arguments:
    content_path -- the path of the content to make.
    """
    html = md.convert(open(content_path, 'r').read())
    return html, md.Meta


def remove_it(nodename):
    """
    Removes a nodename, if it's a file it justs removes it,
    if it's a directory it recursively deletes it.

    Keyword Arguments:
    nodename -- the node name
    """

    try:
        os.unlink(nodename)
    except OSError:
        shutil.rmtree(nodename)


def _print(*args, **kwargs):
    if not kwargs['quite']:
        print(*args)


def minify(func):
    def wrapper(*args):
        if MINIFY_HTML: # noqa
            return htmlmin.minify(func(*args))
        return func(*args)
    return wrapper

##
# Core functioning stuff
##


class Blogger(object):
    def render_html(self):
        """
        Override this method
        """

    def save_page(self):
        with uopen(os.path.join(self.output_dir, self.page_url), 'w', 'utf-8') as myfile:
            myfile.write(self.render_html())


class Paginator(object):
    def __init__(self, curr_page, articles, per_page):
        self.curr_page = curr_page
        self.articles = articles
        self.per_page = per_page

    def pages(self):
        """
        Returns the number of pages.
        """
        return int(ceil(len(self.articles) / float(self.per_page)))

    def has_prev(self):
        """
        Does a curr_page have a previous page?
        """
        return self.curr_page > 1

    def has_next(self):
        """
        Does a curr_page have a next page?
        """
        return self.curr_page < self.pages()

    def page_content(self):
        """
        Returns the content that needs to be in some curr_page
        """
        return self.articles[(self.curr_page - 1) * self.per_page:
                             self.curr_page * self.per_page]

    def next(self):
        """
        Returns the name of the next page.
        """
        if self.has_next():
            return str(self.curr_page + 1)

    def previous(self):
        """
        Returns the name of the previous page.
        """
        if self.has_prev():
            if self.curr_page == 2:
                return ''
            return str(self.curr_page - 1)


# code from requests.structures
class CaseInsensitiveDict(collections.MutableMapping):
    """
    A case-insensitive ``dict``-like object.
    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.
    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive:
        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True
    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.
    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
         return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, dict(self.items()))


class TagsHandler(CaseInsensitiveDict):
    """
    Tags Handler, subclass of dict.
    """

    def __init__(self):
        super(TagsHandler, self).__init__()

    def add_article(self, article):
        """
        Take article with tags and registers it
        """
        for eachTag in article.tags:
            if eachTag not in self:
                self[eachTag] = [article]
            else:
                self[eachTag].append(article)


class Blog(Blogger):
    ARTICLES = []
    page_url = 'index.html'

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.tags = TagsHandler()

    def add_article(self, article):
        if article.tags:
            self.tags.add_article(article)
        if article.hideindex:
            return None
        self.ARTICLES += [article]

    @minify
    def render_html(self, paginator):
        template = env.get_template('index.html')
        return template.render(paginator=paginator)

    @minify
    def render_archive_page(self):
        try:
            template = env.get_template('archive.html')
        except jexceptions.TemplateNotFound:
            return False
        return template.render(articles=self.ARTICLES)

    @minify
    def render_tag_page(self):
        try:
            template = env.get_template('tags.html')
        except jexceptions.TemplateNotFound:
            return False
        return template.render(tags=self.tags)

    def save_page(self):
        self.ARTICLES = self.ARTICLES[::-1]
        for page in range(1,
                          int(ceil(len(self.ARTICLES) / float(per_page))) + 1):
            # maybe slow, making a new instance of a paginator for every article?
            paginator = Paginator(page, self.ARTICLES, per_page)
            if (page != 1):
                self.page_url = 'index%i.html' % page
            with uopen(os.path.join(self.output_dir, self.page_url),
                       'w', 'utf-8') as myfile:
                myfile.write(self.render_html(paginator))

        # make the tags?
        html = self.render_tag_page()
        if html:
            with uopen(os.path.join(self.output_dir, 'tags.html'), 'w', 'utf-8') as myfile:
                myfile.write(html)

        # make the archive
        html = self.render_archive_page()
        if html:
            with uopen(os.path.join(self.output_dir, 'archive.html'), 'w', 'utf-8') as myfile:
                myfile.write(html)

    def finalizer(self):
        # sorts the articles by date
        self.ARTICLES = sorted(self.ARTICLES, key=lambda x: x.date)


class Article(Blogger):
    URLS = {}

    def __init__(self, html, title, date, props, output_dir, **kwargs):
        self.output_dir = output_dir
        self.title = title
        self.html = html
        self.hideindex = 'hideindex' in props

        if kwargs['tags']:
            self.tags = set(map(lambda x: x.strip(), kwargs['tags'][0].split(',')))
        else:
            self.tags = None

        try:
            # TODO: Change this hardcoded date layout
            self.date = datetime.strptime(date, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValueError('Your date is not well structured')

        # sharing the URLS variable between all article instances and
        # saving all maked slugs, if it already exists just add the number
        # simple mechanism but it works
        sep_title = self.urlizer(self.title)
        if sep_title in self.URLS:
            self.URLS[sep_title] += 1
            self.url = "%s-%i" % (sep_title, self.URLS[sep_title])
        else:
            self.URLS[sep_title] = 1
            self.url = sep_title
        self.page_url = self.url + '.html'

    @staticmethod
    def urlizer(title):
        """
        This just a fancy name for a simple slug method.

        Keyword Arguments:
        title -- the actual title to make a slug
        """
        return '-'.join(title.lower().split())

    @minify
    def render_html(self):
        # TODO: Change this hardcoded article file name.
        template = env.get_template('article.html')
        return template.render(
            article_content=self.html,
            article_title=self.title,
            article_date=self.date)


def make_blog_object(content_dir=content_dir, output_dir=output_dir):
    """
    Returns the blog, object.
    """

    blog = Blog(output_dir)

    for content in find_content(content_dir=content_dir):
        html_content, meta_content = compile_html(content)
        article = Article(
            html_content,
            title=meta_content['title'][0],
            date=meta_content['date'][0],
            props=list(map(lambda x: x.lower(), meta_content['props'][0].split(','))) if 'props' in meta_content else [],
            tags=meta_content['tags'] if 'tags' in meta_content else None,
            output_dir=output_dir)

        article.save_page()
        blog.add_article(article)

    blog.finalizer()

    return blog


def make(quite=False):
    """
    Makes the stuff baby :)
    quite -- for testing ?
    """

    if not os.path.exists(output_dir):
        _print('[*] Making %s.' % output_dir, quite=quite)
        os.makedirs(output_dir)


    _print(Fore.YELLOW + '[*] Cleaning output dir.', quite=quite)

    if os.path.exists(output_dir):
        for node in glob.glob(os.path.join(output_dir, '*')):
            remove_it(node)

    _print(Fore.YELLOW + '[*] Buidling %i page.' % len(find_content(content_dir=content_dir)),
           quite=quite
    )

    blog = make_blog_object(content_dir, output_dir)
    _print(Fore.YELLOW + '[*] Linking the index.', quite=quite)
    blog.save_page()

    if os.path.exists(os.path.join(THEME_DIR, 'assets')):
        _print(Fore.YELLOW + '[*] Copying static files.', quite=quite)
        shutil.copytree(os.path.join(THEME_DIR, 'assets'),
                        os.path.join(output_dir, 'assets'))

    try:
        ASSETS_PATH # noqa
        _print(Fore.YELLOW + '[*] Copying users static files.', quite=quite)
        if not os.path.exists(os.path.join(output_dir, 'assets')):
            shutil.copytree(ASSETS_PATH, os.path.join(output_dir, 'assets')) # noqa
        else:
            from distutils.dir_util import copy_tree # noqa
            copy_tree(ASSETS_PATH, os.path.join(output_dir, 'assets')) # noqa
    except NameError:
        pass
