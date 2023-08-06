#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# The MIT License
#
# Copyright (c) 2016 Grigory Chernyshev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################
import json
import os
from distutils.version import LooseVersion

import pytest
from mock import mock
from six import string_types

from tests import AbstractTestManager, ReturnValueMixin
from yagocd.resources import template


@pytest.fixture()
def manager(session_fixture):
    return template.TemplateManager(session=session_fixture)


class BaseManager(AbstractTestManager):
    @pytest.fixture()
    def template_foo(self, tests_dir):
        path = os.path.join(tests_dir, 'fixtures/resources/template/template-foo.json')
        return json.load(open(path))

    @pytest.fixture()
    def template_bar(self, tests_dir):
        path = os.path.join(tests_dir, 'fixtures/resources/template/template-bar.json')
        return json.load(open(path))

    @pytest.fixture()
    def template_dummy(self, tests_dir):
        path = os.path.join(tests_dir, 'fixtures/resources/template/template-dummy.json')
        return json.load(open(path))

    @pytest.fixture()
    def expected_accept_headers(self, server_version):
        if LooseVersion(server_version) <= LooseVersion('16.10.0'):
            return 'application/vnd.go.cd.v1+json'
        elif LooseVersion(server_version) <= LooseVersion('16.11.0'):
            return 'application/vnd.go.cd.v2+json'
        else:
            return 'application/vnd.go.cd.v3+json'


class TestList(BaseManager, ReturnValueMixin):
    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("template/list") as cass:
            return cass, manager.list()

    @pytest.fixture()
    def expected_request_url(self):
        return '/go/api/admin/templates'

    @pytest.fixture()
    def expected_request_method(self):
        return 'GET'

    @pytest.fixture()
    def expected_return_type(self):
        return list

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            assert all(isinstance(i, template.TemplateConfig) for i in result)

        return check_value


class TestGet(BaseManager, ReturnValueMixin):
    NAME = 'Development'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("template/get_{}".format(self.NAME)) as cass:
            return cass, manager.get(self.NAME)

    @pytest.fixture()
    def expected_request_url(self):
        return '/go/api/admin/templates/{}'.format(self.NAME)

    @pytest.fixture()
    def expected_request_method(self):
        return 'GET'

    @pytest.fixture()
    def expected_return_type(self):
        return template.TemplateConfig

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            assert result.data.name == self.NAME

        return check_value


class TestCreate(BaseManager, ReturnValueMixin):
    NAME = 'foo'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr, template_foo):
        with my_vcr.use_cassette("template/create_{}".format(self.NAME)) as cass:
            return cass, manager.create(config=template_foo)

    @pytest.fixture()
    def expected_request_url(self):
        return '/go/api/admin/templates'

    @pytest.fixture()
    def expected_request_method(self):
        return 'POST'

    @pytest.fixture()
    def expected_return_type(self):
        return template.TemplateConfig

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            assert result.data.name == self.NAME

        return check_value


class TestUpdate(BaseManager, ReturnValueMixin):
    NAME = 'bar'
    STAGE_NAME = 'BAZ-STAGE'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr, template_bar):
        with my_vcr.use_cassette("template/prepare_update_{}".format(self.NAME)):
            manager.create(config=template_bar)
            original = manager.get(self.NAME)  # noqa

        with my_vcr.use_cassette("template/update_{}".format(self.NAME)) as cass:
            template_bar['stages'][0]['name'] = self.STAGE_NAME
            return cass, manager.update(
                name=self.NAME,
                config=template_bar,
                etag=original.etag
            )

    @pytest.fixture()
    def expected_request_url(self):
        return '/go/api/admin/templates/{}'.format(self.NAME)

    @pytest.fixture()
    def expected_request_method(self, manager):
        return 'PUT'

    @pytest.fixture()
    def expected_return_type(self):
        return template.TemplateConfig

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            assert result.data['stages'][0]['name'] == self.STAGE_NAME

        return check_value


class TestDelete(BaseManager, ReturnValueMixin):
    NAME = 'dummy'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr, template_dummy):
        with my_vcr.use_cassette("template/prepare_delete_{}".format(self.NAME)):
            manager.create(config=template_dummy)

        with my_vcr.use_cassette("template/delete_{}".format(self.NAME)) as cass:
            return cass, manager.delete(name=self.NAME)

    @pytest.fixture()
    def expected_request_url(self):
        return '/go/api/admin/templates/{}'.format(self.NAME)

    @pytest.fixture()
    def expected_request_method(self, manager):
        return 'DELETE'

    @pytest.fixture()
    def expected_return_type(self):
        return string_types

    @pytest.fixture()
    def expected_return_value(self):
        return "The template '{}' was deleted successfully.".format(self.NAME)


class TestMagicMethods(object):
    @mock.patch('yagocd.resources.template.TemplateManager.get')
    def test_indexed_based_access(self, get_mock, manager):
        name = mock.MagicMock()
        _ = manager[name]  # noqa
        get_mock.assert_called_once_with(name=name)

    @mock.patch('yagocd.resources.template.TemplateManager.list')
    def test_iterator_access(self, list_mock, manager):
        for _ in manager:
            pass
        list_mock.assert_called_once_with()
