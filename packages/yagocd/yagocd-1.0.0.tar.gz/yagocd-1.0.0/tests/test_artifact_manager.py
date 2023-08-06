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
import zipfile

import mock
import pytest
from six import binary_type, BytesIO, string_types

from tests import AbstractTestManager, ReturnValueMixin
from yagocd.resources import artifact
from yagocd.util import Since


class BaseTestArtifactManager(object):
    PIPELINE_NAME = 'Shared_Services'
    PIPELINE_COUNTER = 7
    STAGE_NAME = 'Commit'
    STAGE_COUNTER = '1'
    JOB_NAME = 'build'

    @pytest.fixture()
    def manager(self, session_fixture):
        return artifact.ArtifactManager(
            session=session_fixture,
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME
        )

    @pytest.fixture()
    def mock_manager(self, mock_session):
        return artifact.ArtifactManager(
            session=mock_session,
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME
        )

    def _get_artifact_json(self, tests_dir, session_fixture, name):
        with open(os.path.join(tests_dir, 'fixtures/resources/artifact/{}.json'.format(name))) as f:
            data = json.load(f)

        return artifact.Artifact(session_fixture, data)

    @pytest.fixture()
    def artifact_all(
        self,
        artifact_another_directory,
        artifact_cruise_output,
        artifact_dummy_txt,
        artifact_yet_another_directory,
    ):
        return [
            artifact_another_directory,
            artifact_cruise_output,
            artifact_dummy_txt,
            artifact_yet_another_directory,
        ]

    @pytest.fixture()
    def artifact_another_directory(self, tests_dir, session_fixture):
        return self._get_artifact_json(tests_dir, session_fixture, 'another-directory')

    @pytest.fixture()
    def artifact_cruise_output(self, tests_dir, session_fixture):
        return self._get_artifact_json(tests_dir, session_fixture, 'cruise-output')

    @pytest.fixture()
    def artifact_dummy_txt(self, tests_dir, session_fixture):
        return self._get_artifact_json(tests_dir, session_fixture, 'dummy.txt')

    @pytest.fixture()
    def artifact_yet_another_directory(self, tests_dir, session_fixture):
        return self._get_artifact_json(tests_dir, session_fixture, 'yet-another-directory')


class TestList(AbstractTestManager, BaseTestArtifactManager, ReturnValueMixin):
    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_list") as cass:
            return cass, manager.list()

    @pytest.fixture()
    def expected_request_url(self):
        return (
            '/go'
            '/files'
            '/{pipeline_name}'
            '/{pipeline_counter}'
            '/{stage_name}'
            '/{stage_counter}'
            '/{job_name}.json'
        ).format(
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME
        )

    @pytest.fixture()
    def expected_request_method(self):
        return 'GET'

    @pytest.fixture()
    def expected_return_type(self):
        return list

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            len(result) > 0
            all(isinstance(i, artifact.Artifact) for i in result)

        return check_value


@mock.patch('yagocd.resources.artifact.ArtifactManager.list')
class TestWalk(BaseTestArtifactManager):

    @pytest.yield_fixture(autouse=True)
    def disable_since(self):
        _original = Since.ENABLED
        Since.ENABLED = False

        yield
        Since.ENABLED = _original

    def test_dummy_txt(self, list_mock, artifact_dummy_txt):
        """:type artifact_dummy_txt: artifact.Artifact"""

        list_mock.return_value = [artifact_dummy_txt]

        Since.ENABLED = False

        assert artifact_dummy_txt.data.type == 'file'
        assert artifact_dummy_txt.data.name == 'dummy.txt'

        assert artifact_dummy_txt.pipeline_name == self.PIPELINE_NAME
        assert artifact_dummy_txt.pipeline_counter == '33'
        assert artifact_dummy_txt.stage_name == self.STAGE_NAME
        assert artifact_dummy_txt.stage_counter == self.STAGE_COUNTER
        assert artifact_dummy_txt.job_name == self.JOB_NAME
        assert artifact_dummy_txt.path == '/dummy.txt'

        with pytest.raises(StopIteration):
            next(artifact_dummy_txt.walk())

    def test_another_directory(self, list_mock, artifact_another_directory):
        """:type artifact_another_directory: artifact.Artifact"""

        list_mock.return_value = [artifact_another_directory]

        assert artifact_another_directory.data.type == 'folder'
        assert artifact_another_directory.data.name == 'another-directory'

        assert artifact_another_directory.pipeline_name == self.PIPELINE_NAME
        assert artifact_another_directory.pipeline_counter == '33'
        assert artifact_another_directory.stage_name == self.STAGE_NAME
        assert artifact_another_directory.stage_counter == self.STAGE_COUNTER
        assert artifact_another_directory.job_name == self.JOB_NAME
        assert artifact_another_directory.path == '/another-directory/'

        assert ('/another-directory/', [], []) == next(artifact_another_directory.walk())

    def test_yet_another_directory(self, list_mock, artifact_yet_another_directory):
        """:type artifact_yet_another_directory: artifact.Artifact"""

        list_mock.return_value = [artifact_yet_another_directory]

        assert artifact_yet_another_directory.data.type == 'folder'
        assert artifact_yet_another_directory.data.name == 'yet-another-directory'

        walk_iter = artifact_yet_another_directory.walk()

        next_item = next(walk_iter)
        assert ('/yet-another-directory/',
                [
                    '/yet-another-directory/sub-dir-1/',
                    '/yet-another-directory/sub-dir-2/',
                ],
                [
                    '/yet-another-directory/some-file.txt',
                ]
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-1',
                ['/yet-another-directory/sub-dir-1/sub-dir-3/'],
                []
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-1/sub-dir-3',
                [],
                [
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-1.txt',
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-3.txt',
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-5.txt',
                ]
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-2',
                [],
                []
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        with pytest.raises(StopIteration):
            next(walk_iter)

    def test_yet_another_directory_not_topdown(self, list_mock, artifact_yet_another_directory):
        """:type artifact_yet_another_directory: artifact.Artifact"""

        list_mock.return_value = [artifact_yet_another_directory]

        assert artifact_yet_another_directory.data.type == 'folder'
        assert artifact_yet_another_directory.data.name == 'yet-another-directory'

        walk_iter = artifact_yet_another_directory.walk(topdown=False)

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-1/sub-dir-3',
                [],
                [
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-1.txt',
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-3.txt',
                    '/yet-another-directory/sub-dir-1/sub-dir-3/hello-5.txt',
                ]
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-1',
                ['/yet-another-directory/sub-dir-1/sub-dir-3/'],
                []
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/sub-dir-2',
                [],
                []
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        next_item = next(walk_iter)
        assert ('/yet-another-directory/',
                [
                    '/yet-another-directory/sub-dir-1/',
                    '/yet-another-directory/sub-dir-2/',
                ],
                [
                    '/yet-another-directory/some-file.txt',
                ]
                ) == (next_item[0],
                      [f.path for f in next_item[1]],
                      [f.path for f in next_item[2]],
                      )

        with pytest.raises(StopIteration):
            next(walk_iter)


class TestJsonWalk(BaseTestArtifactManager):
    pass


class TestGetChildren(BaseTestArtifactManager):
    @pytest.mark.parametrize('top, expected', [
        (None, [
            '/another-directory/',
            '/cruise-output/',
            '/dummy.txt',
            '/yet-another-directory/',
        ]),
        ('', [
            '/another-directory/',
            '/cruise-output/',
            '/dummy.txt',
            '/yet-another-directory/',
        ]),
        ('/', [
            '/another-directory/',
            '/cruise-output/',
            '/dummy.txt',
            '/yet-another-directory/',
        ]),

        ('/another-directory', []),
        ('/dummy.txt', None),
        (
            '/yet-another-directory',
            [
                '/yet-another-directory/sub-dir-1/',
                '/yet-another-directory/sub-dir-2/',
                '/yet-another-directory/some-file.txt'
            ]
        ),
        (
            '/cruise-output',
            [
                '/cruise-output/sub-directory-1/',
                '/cruise-output/sub-directory-2/',
                '/cruise-output/sub-directory-3/',
                '/cruise-output/console.log',
            ]
        ),
    ])
    def test_parametrized(self, manager, artifact_all, top, expected):
        result = manager._get_children(artifact_all, top)
        if not expected:
            assert result == expected
        else:
            assert [r.path for r in result] == expected

    @pytest.mark.parametrize('top', [
        'unknown-path',
        'another-directory',
        'another-directory/',
        '//dummy.txt',
        '/dummy',
    ])
    def test_non_existing_path(self, manager, artifact_all, top):
        with pytest.raises(ValueError):
            manager._get_children(artifact_all, top)


class TestFile(BaseTestArtifactManager):
    @mock.patch('yagocd.resources.artifact.ArtifactManager.directory')
    def test_directory_is_executed(self, directory_mock, mock_manager):
        path = mock.MagicMock()
        _ = mock_manager.file(path=path)  # noqa
        directory_mock.assert_called_once_with(
            path=path,
            pipeline_name=None,
            pipeline_counter=None,
            stage_name=None,
            stage_counter=None,
            job_name=None,
        )


class TestDirectoryNotReady(AbstractTestManager, BaseTestArtifactManager, ReturnValueMixin):
    TEST_METHOD_NAME = 'directory'

    DIRECTORY_PATH = 'path/to/the/.zip'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_directory_not_ready") as cass:
            return cass, manager.directory(path=self.DIRECTORY_PATH)

    @pytest.fixture()
    def expected_request_url(self):
        return (
            '/go'
            '/files'
            '/{pipeline_name}'
            '/{pipeline_counter}'
            '/{stage_name}'
            '/{stage_counter}'
            '/{job_name}'
            '/{dir_path}'
        ).format(
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME,
            dir_path=self.DIRECTORY_PATH
        )

    @pytest.fixture()
    def expected_request_method(self):
        return 'GET'

    @pytest.fixture()
    def expected_response_code(self, *args, **kwargs):
        return 202

    @pytest.fixture()
    def expected_return_type(self):
        return None

    @pytest.fixture()
    def expected_return_value(self, *args, **kwargs):
        def check_value(result):
            assert result is None

        return check_value


class TestDirectoryReady(TestDirectoryNotReady):
    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_directory_ready") as cass:
            return cass, manager.directory(path=self.DIRECTORY_PATH)

    @pytest.fixture()
    def expected_response_code(self, *args, **kwargs):
        return 200

    @pytest.fixture()
    def expected_return_type(self):
        return string_types, binary_type

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            myzipfile = zipfile.ZipFile(BytesIO(result))
            assert myzipfile.testzip() is None

        return check_value


class TestDirectoryNotReadyWait(TestDirectoryNotReady):
    TEST_METHOD_NAME = 'directory_wait'
    EXPECTED_CASSETTE_COUNT = 2

    DIRECTORY_PATH = 'path/to/.zip'

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_directory_not_ready_wait") as cass:
            return cass, manager.directory_wait(path=self.DIRECTORY_PATH)

    @mock.patch('yagocd.resources.artifact.ArtifactManager.directory')
    def test_directory_method_is_called(self, mock_directory, manager, my_vcr):
        self._execute_test_action(manager, my_vcr)
        mock_directory.assert_called()

    @pytest.fixture()
    def expected_return_type(self):
        return string_types, binary_type

    @pytest.fixture()
    def expected_return_value(self):
        def check_value(result):
            myzipfile = zipfile.ZipFile(BytesIO(result))
            assert myzipfile.testzip() is None

        return check_value


class TestDirectoryReadyWait(TestDirectoryNotReadyWait):
    EXPECTED_CASSETTE_COUNT = 1

    @pytest.fixture()
    def _execute_test_action(self, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_directory_ready_wait") as cass:
            return cass, manager.directory_wait(path=self.DIRECTORY_PATH)

    @pytest.fixture()
    def expected_response_code(self, *args, **kwargs):
        return 200


class TestCreate(AbstractTestManager, BaseTestArtifactManager):
    PATH_TO_FILE = 'path/to/the/file.txt'
    FILE_CONTENT = 'Sample test data.\nFoo and Bar.'

    @pytest.fixture(scope='session')
    def sample_artifact(self, tmpdir_factory):
        fn = tmpdir_factory.mktemp("gocd").join("artifact.txt")
        fn.write(self.FILE_CONTENT)
        return fn

    @pytest.fixture()
    def _execute_test_action(self, sample_artifact, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_create") as cass:
            return cass, manager.create(path=self.PATH_TO_FILE, filename=sample_artifact.strpath)

    @pytest.fixture()
    def expected_request_url(self):
        return (
            '/go'
            '/files'
            '/{pipeline_name}'
            '/{pipeline_counter}'
            '/{stage_name}'
            '/{stage_counter}'
            '/{job_name}'
            '/{path_to_file}'
        ).format(
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME,
            path_to_file=self.PATH_TO_FILE
        )

    @pytest.fixture()
    def expected_request_method(self):
        return 'POST'

    @pytest.fixture()
    def expected_response_code(self, *args, **kwargs):
        return 201

    @pytest.fixture()
    def expected_return_type(self):
        return string_types

    @pytest.fixture()
    def expected_return_value(self):
        return 'File {0} was created successfully'.format(self.PATH_TO_FILE)


class TestAppend(AbstractTestManager, BaseTestArtifactManager, ReturnValueMixin):
    PATH_TO_FILE = 'path/to/the/file-append.txt'
    FILE_CONTENT = 'Data to append.'

    @pytest.fixture(scope='session')
    def sample_artifact(self, tmpdir_factory):
        fn = tmpdir_factory.mktemp("gocd").join("artifact-append.txt")
        fn.write(self.FILE_CONTENT)
        return fn

    @pytest.fixture()
    def _execute_test_action(self, sample_artifact, manager, my_vcr):
        with my_vcr.use_cassette("artifact/artifact_append") as cass:
            return cass, manager.append(path=self.PATH_TO_FILE, filename=sample_artifact.strpath)

    @pytest.fixture()
    def expected_request_url(self):
        return (
            '/go'
            '/files'
            '/{pipeline_name}'
            '/{pipeline_counter}'
            '/{stage_name}'
            '/{stage_counter}'
            '/{job_name}'
            '/{path_to_file}'
        ).format(
            pipeline_name=self.PIPELINE_NAME,
            pipeline_counter=self.PIPELINE_COUNTER,
            stage_name=self.STAGE_NAME,
            stage_counter=self.STAGE_COUNTER,
            job_name=self.JOB_NAME,
            path_to_file=self.PATH_TO_FILE
        )

    @pytest.fixture()
    def expected_request_method(self):
        return 'PUT'

    @pytest.fixture()
    def expected_return_type(self):
        return string_types

    @pytest.fixture()
    def expected_return_value(self):
        return 'File {0} was appended successfully'.format(self.PATH_TO_FILE)


class TestMagicMethods(BaseTestArtifactManager):
    @mock.patch('yagocd.resources.artifact.ArtifactManager.directory_wait')
    def test_indexed_based_access(self, directory_wait_mock, manager):
        path = mock.MagicMock()
        _ = manager[path]  # noqa
        directory_wait_mock.assert_called_once_with(path=path)

    @mock.patch('yagocd.resources.artifact.ArtifactManager.list')
    def test_iterator_access(self, list_mock, mock_manager):
        for _ in mock_manager:
            pass
        list_mock.assert_called_once_with(
            job_name=None, pipeline_counter=None, pipeline_name=None, stage_counter=None, stage_name=None
        )
