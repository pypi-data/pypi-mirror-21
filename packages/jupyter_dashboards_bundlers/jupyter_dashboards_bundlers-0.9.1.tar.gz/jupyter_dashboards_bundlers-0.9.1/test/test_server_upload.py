# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import copy
import errno
import os
import shutil
import tempfile
import unittest
import zipfile
from os.path import exists, join as pjoin

import dashboards_bundlers.server_upload as converter
import notebook.bundler.tools
from jupyter_core.paths import jupyter_data_dir
from tornado import web

dashboard_link = 'http://notebook-server:3000/dashboards/test'


class MockResult(object):
    def __init__(self, status_code, include_link=True):
        self.status_code = status_code
        if (include_link):
            self.json = lambda: {'link': dashboard_link}
        else:
            self.json = lambda: {}


class MockPost(object):
    def __init__(self, status_code, include_result_link=True):
        self.args = None
        self.kwargs = None
        self.status_code = status_code
        self.include_result_link = include_result_link

    def __call__(self, *args, **kwargs):
        if self.args or self.kwargs:
            raise RuntimeError('MockPost already invoked')
        self.args = args
        self.kwargs = kwargs
        return MockResult(self.status_code, self.include_result_link)


class MockZipPost(object):
    '''
    Explicitly checks for a posted zip file
    '''
    def __init__(self, status_code):
        self.args = None
        self.kwargs = None
        self.status_code = status_code

    def __call__(self, *args, **kwargs):
        if self.args or self.kwargs:
            raise RuntimeError('MockZipPost already invoked')
        self.args = args
        self.kwargs = kwargs
        uploaded_zip = zipfile.ZipFile(kwargs['files']['file'], 'r')
        self.zipped_files = uploaded_zip.namelist()
        return MockResult(self.status_code)


class MockRequest(object):
    def __init__(self, host, protocol):
        self.host = host
        self.protocol = protocol


class MockContentsManager(object):
    def __init__(self):
        self.root_dir = '.'


class MockHandler(object):
    def __init__(self, host='notebook-server:8888', protocol='http'):
        self.settings = {
            'base_url': '/',
            'contents_manager': MockContentsManager()
        }
        self.request = MockRequest(host, protocol)
        self.last_redirect = None
        self.tools = notebook.bundler.tools

    def redirect(self, location):
        self.last_redirect = location


class TestServerUpload(unittest.TestCase):
    def setUp(self):
        self.origin_env = copy.deepcopy(os.environ)
        converter.requests.post = MockPost(200)

    def tearDown(self):
        os.environ = self.origin_env

    def test_no_server(self):
        '''Should error if no server URL is set.'''
        handler = MockHandler('fake-host:8000', 'http')
        self.assertRaises(web.HTTPError, converter.bundle, handler,
                          {'path': 'test/resources/no_imports.ipynb'})

    def test_upload_notebook(self):
        '''Should POST the notebook and redirect to the dashboard server.'''
        os.environ['DASHBOARD_SERVER_URL'] = 'http://dashboard-server'
        handler = MockHandler()
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})

        args = converter.requests.post.args
        kwargs = converter.requests.post.kwargs
        self.assertEqual(args[0],
                         'http://dashboard-server/_api/notebooks/no_imports')
        self.assertTrue(kwargs['files']['file'])
        self.assertEqual(kwargs['headers'], {})
        self.assertEqual(handler.last_redirect, dashboard_link)

    def test_upload_zip(self):
        '''
        Should POST the notebook in a zip with resources and redirect to
        the dashboard server.
        '''
        os.environ['DASHBOARD_SERVER_URL'] = 'http://dashboard-server'
        handler = MockHandler()
        converter.requests.post = MockZipPost(200)
        converter.bundle(handler, {'path': 'test/resources/some.ipynb'})

        args = converter.requests.post.args
        kwargs = converter.requests.post.kwargs
        self.assertEqual(args[0],
                         'http://dashboard-server/_api/notebooks/some')
        self.assertTrue(kwargs['files']['file'])
        self.assertEqual(kwargs['headers'], {})
        self.assertEqual(handler.last_redirect, dashboard_link)
        self.assertTrue('index.ipynb' in converter.requests.post.zipped_files)
        self.assertTrue('some.csv' in converter.requests.post.zipped_files)

    def test_upload_token(self):
        '''Should include an auth token in the request.'''
        os.environ['DASHBOARD_SERVER_URL'] = 'http://dashboard-server'
        os.environ['DASHBOARD_SERVER_AUTH_TOKEN'] = 'fake-token'
        handler = MockHandler()
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})

        kwargs = converter.requests.post.kwargs
        self.assertEqual(kwargs['headers'],
                         {'Authorization': 'token fake-token'})

    def test_url_interpolation(self):
        '''Should build the server URL from the request Host header.'''
        os.environ['DASHBOARD_SERVER_URL'] = '{protocol}://{hostname}:8889'
        handler = MockHandler('notebook-server:8888', 'https')
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})

        args = converter.requests.post.args
        self.assertEqual(args[0],
                         'https://notebook-server:8889/_api/notebooks/no_imports')
        self.assertEqual(handler.last_redirect, dashboard_link)

    def test_redirect_fallback(self):
        '''Should redirect to the given URL'''
        converter.requests.post = MockPost(200, False)
        os.environ['DASHBOARD_SERVER_URL'] = '{protocol}://{hostname}:8889'
        os.environ['DASHBOARD_REDIRECT_URL'] = 'http://{hostname}:3000'
        handler = MockHandler('notebook-server:8888', 'https')
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})

        args = converter.requests.post.args
        self.assertEqual(args[0],
                         'https://notebook-server:8889/_api/notebooks/no_imports')
        self.assertEqual(handler.last_redirect,
                         'http://notebook-server:3000/dashboards/no_imports')

    def test_ssl_verify(self):
        '''Should verify SSL certificate by default.'''
        handler = MockHandler()
        os.environ['DASHBOARD_SERVER_URL'] = '{protocol}://{hostname}:8889'
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})
        kwargs = converter.requests.post.kwargs
        self.assertEqual(kwargs['verify'], True)

    def test_no_ssl_verify(self):
        '''Should skip SSL certificate verification.'''
        os.environ['DASHBOARD_SERVER_NO_SSL_VERIFY'] = 'yes'
        os.environ['DASHBOARD_SERVER_URL'] = '{protocol}://{hostname}:8889'
        handler = MockHandler()
        converter.bundle(handler, {'path': 'test/resources/no_imports.ipynb'})
        kwargs = converter.requests.post.kwargs
        self.assertEqual(kwargs['verify'], False)


# Mock existence of declarative widgets
DECL_WIDGETS_DIR = pjoin(jupyter_data_dir(), 'nbextensions/urth_widgets/')
DECL_WIDGETS_JS_DIR = pjoin(DECL_WIDGETS_DIR, 'js')
DECL_VIZ_DIR = pjoin(DECL_WIDGETS_DIR, 'components/urth-viz')
DECL_CORE_DIR = pjoin(DECL_WIDGETS_DIR, 'components/urth-core')
BOWER_COMPONENT_DIR = pjoin(jupyter_data_dir(),
                            'nbextensions/urth_widgets/urth_components/component-a')


class TestBundleWidgets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for d in (DECL_WIDGETS_DIR, DECL_WIDGETS_JS_DIR, DECL_CORE_DIR,
                  DECL_VIZ_DIR, BOWER_COMPONENT_DIR):
            try:
                os.makedirs(d)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    raise

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_bundle_declarative_widgets(self):
        '''Should write declarative widgets to output.'''
        converter.bundle_declarative_widgets(self.tmp,
                                             'test/resources/env.ipynb')
        self.assertTrue(exists(pjoin(self.tmp, 'static/urth_widgets')),
                        'urth_widgets should exist')
        self.assertTrue(exists(pjoin(self.tmp, 'static/urth_components')),
                        'urth_components should exist')

    def test_skip_declarative_widgets(self):
        '''Should not write declarative widgets to output.'''
        # Testing to make sure we do not add bower components unnecessarily
        converter.bundle_declarative_widgets(self.tmp,
                                             'test/resources/no_imports.ipynb')
        self.assertFalse(exists(pjoin(self.tmp, 'static/urth_widgets')),
                         'urth_widgets should not exist')
        self.assertFalse(exists(pjoin(self.tmp, 'static/urth_components')),
                         'urth_components should not exist')
