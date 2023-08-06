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

from yagocd.resources import BaseManager
from yagocd.util import RequireParamMixin, since


@since('14.3.0')
class FeedManager(BaseManager, RequireParamMixin):
    """
    The feed API allows users to view feed information.

    `Official documentation. <https://api.go.cd/current/#feeds>`_

    :versionadded: 14.3.0.
    """

    PIPELINES_RESOURCE_PATH = '{base_api}/pipelines'
    STAGES_RESOURCE_PATH = '{base_api}/stages'

    def __init__(
        self,
        session,
        pipeline_name=None,
        pipeline_counter=None,
        stage_name=None,
        stage_counter=None,
    ):
        super(FeedManager, self).__init__(session)

        self._pipeline_name = pipeline_name
        self._pipeline_counter = pipeline_counter
        self._stage_name = stage_name
        self._stage_counter = stage_counter

    def pipelines(self):
        """
        Lists all pipelines.

        :versionadded: 14.3.0.

        :return: an array of pipelines in XML format.
        """
        response = self._session.get(
            path=(self.PIPELINES_RESOURCE_PATH + '.xml').format(base_api=self.base_api),
            headers={'Accept': 'application/xml'},
        )

        return response.text

    def pipeline_by_id(self, pipeline_id):
        """
        Gets XML representation of pipeline.

        :versionadded: 14.3.0.

        :param pipeline_id: id of pipeline. Note: this is *not* a counter.
        :return: a pipeline object in XML format.
        """
        response = self._session.get(
            path=self._session.urljoin(
                self.PIPELINES_RESOURCE_PATH,
                'THIS_PARAMETER_IS_USELESS',  # WTF?!!
                '{}.xml'.format(pipeline_id)
            ).format(
                base_api=self.base_api
            ),
            headers={'Accept': 'application/xml'},
        )

        return response.text

    def stages(self, pipeline_name):
        """
        Gets feed of all stages for the specified pipeline with links to the pipeline and stage details.

        :versionadded: 14.3.0.

        :param pipeline_name: name of pipeline, for which to list stages
        :return: an array of feed of stages in XML format.
        """

        pipeline_name = self._require_param('pipeline_name', locals())

        response = self._session.get(
            path=self._session.urljoin(self.PIPELINES_RESOURCE_PATH, pipeline_name, 'stages.xml').format(
                base_api=self.base_api
            ),
            headers={'Accept': 'application/xml'},
        )

        return response.text

    def stage_by_id(self, stage_id):
        """
        Gets XML representation of stage.

        :versionadded: 14.3.0.

        :param stage_id: id of stage. Note: this is *not* a counter.
        :return: a stage object in XML format.
        """
        response = self._session.get(
            path=self._session.urljoin(
                self.STAGES_RESOURCE_PATH,
                '{}.xml'.format(stage_id)
            ).format(
                base_api=self.base_api
            ),
            headers={'Accept': 'application/xml'},
        )

        return response.text

    def stage(self, pipeline_name, pipeline_counter, stage_name, stage_counter):
        """
        Gets XML representation of stage.

        :versionadded: 14.3.0.

        :param pipeline_name: name of pipeline.
        :param pipeline_counter: pipeline counter.
        :param stage_name: name of stage.
        :param stage_counter: stage counter.
        :return: a stage object in XML format.
        """

        func_args = locals()
        pipeline_name = self._require_param('pipeline_name', func_args)
        pipeline_counter = self._require_param('pipeline_counter', func_args)
        stage_name = self._require_param('stage_name', func_args)
        stage_counter = self._require_param('stage_counter', func_args)

        response = self._session.get(
            path=self._session.urljoin(
                self.PIPELINES_RESOURCE_PATH,
                pipeline_name,
                pipeline_counter,
                stage_name,
                '{}.xml'.format(stage_counter)
            ).format(
                base_api=self._session.base_api(api_path=''),  # WTF?!!
            ),
            headers={'Accept': 'application/xml'},
        )

        return response.text

    def job_by_id(self, job_id):
        """
        Gets XML representation of job.

        :versionadded: 14.3.0.

        :param job_id: id of job. Note: this is *not* a counter.
        :return: a job object in XML format.
        """
        response = self._session.get(
            path='{base_api}/jobs/{job_id}.xml'.format(
                base_api=self.base_api,
                job_id=job_id
            ),
            headers={'Accept': 'application/xml'},
        )

        return response.text
