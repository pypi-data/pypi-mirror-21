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

import pytest
from mock import mock

from yagocd.resources import Base
from yagocd.resources import pipeline
from yagocd.resources import stage
from yagocd.resources.pipeline_config import PipelineConfigManager


class TestPipelineEntity(object):
    @pytest.fixture()
    def pipeline_instance(self, mock_session):
        data = json.load(open('tests/fixtures/resources/pipeline/pipeline_instance.json'))
        return pipeline.PipelineInstance(session=mock_session, data=data)

    @mock.patch('yagocd.resources.pipeline.PipelineInstance.stage')
    def test_indexed_based_access(self, stage_mock, pipeline_instance):
        name = mock.MagicMock()
        _ = pipeline_instance[name]  # noqa
        stage_mock.assert_called_once_with(name=name)

    @mock.patch('yagocd.resources.pipeline.PipelineInstance.stages')
    def test_iterator_access(self, stages_mock, pipeline_instance):
        for _ in pipeline_instance:
            pass
        stages_mock.assert_called_once_with()

    def test_instance_is_not_none(self, pipeline_instance):
        assert pipeline_instance is not None

    def test_is_instance_of_base(self, pipeline_instance):
        assert isinstance(pipeline_instance, Base)

    def test_getting_name(self, pipeline_instance):
        assert pipeline_instance.data.name == 'Shared_Services'

    def test_getting_url(self, pipeline_instance):
        assert pipeline_instance.url == 'http://example.com/go/pipelines/value_stream_map/Shared_Services/2'

    def test_getting_pipeline_url(self, pipeline_instance):
        assert pipeline_instance.pipeline_url == 'http://example.com/go/tab/pipeline/history/Shared_Services'

    def test_stages_are_not_empty(self, pipeline_instance):
        assert len(pipeline_instance.stages()) > 0

    def test_stages_instances(self, pipeline_instance):
        assert all(isinstance(i, stage.StageInstance) for i in pipeline_instance.stages())

    @mock.patch('yagocd.resources.pipeline.PipelineInstance.stages')
    def test_stage(self, stages_mock, pipeline_instance):
        foo = mock.MagicMock()
        foo.data.name = 'foo'
        bar = mock.MagicMock()
        bar.data.name = 'bar'
        baz = mock.MagicMock()
        baz.data.name = 'baz'
        stages_mock.return_value = [foo, bar, baz]

        result = pipeline_instance.stage(name='bar')
        assert result == bar

    @mock.patch('yagocd.resources.pipeline.PipelineManager.value_stream_map')
    def test_value_stream_map_call(self, value_stream_map_mock, pipeline_instance):
        pipeline_instance.value_stream_map()
        value_stream_map_mock.assert_called_with(
            name=pipeline_instance.data.name,
            counter=pipeline_instance.data.counter
        )

    def test_config(self, pipeline_instance):
        assert isinstance(pipeline_instance.config, PipelineConfigManager)
