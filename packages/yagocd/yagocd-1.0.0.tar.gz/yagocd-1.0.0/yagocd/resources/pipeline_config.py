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

from yagocd.resources import Base, BaseManager
from yagocd.util import RequireParamMixin, since


@since('15.3.0')
class PipelineConfigManager(BaseManager, RequireParamMixin):
    """
    The pipeline config API allows users with administrator role to manage pipeline config.

    `Official documentation. <https://api.go.cd/current/#pipeline-config>`_

    :versionadded: 15.3.0.
    """

    RESOURCE_PATH = '{base_api}/admin/pipelines'

    ACCEPT_HEADER = 'application/vnd.go.cd.v3+json'

    VERSION_TO_ACCEPT_HEADER = {
        '16.6.0': 'application/vnd.go.cd.v1+json',
        '16.12.0': 'application/vnd.go.cd.v2+json',
    }

    def __init__(self, session, pipeline_name=None):
        super(PipelineConfigManager, self).__init__(session)
        self._pipeline_name = pipeline_name

    def __getitem__(self, pipeline_name):
        """
        Method add possibility to get pipeline config by the name using dictionary like syntax.

        :param pipeline_name: name of the pipeline.
        :return: pipeline config object.
        :rtype: yagocd.resources.pipeline_config.PipelineConfig
        """
        return self.get(pipeline_name=pipeline_name)

    def get(self, pipeline_name=None):
        """
        Gets pipeline config for specified pipeline name.

        :versionadded: 15.3.0.

        :param pipeline_name: name of the pipeline. Could be skipped
          if name was configured from constructor.
        :return: pipeline config object.
        :rtype: yagocd.resources.pipeline_config.PipelineConfig
        """
        pipeline_name = self._require_param('pipeline_name', locals())

        response = self._session.get(
            path=self._session.urljoin(self.RESOURCE_PATH, pipeline_name).format(base_api=self.base_api),
            headers={'Accept': self._accept_header()},
        )

        etag = response.headers['ETag']
        return PipelineConfig(session=self._session, data=response.json(), etag=etag)

    def edit(self, config, etag, pipeline_name=None):
        """
        Update pipeline config for specified pipeline name.

        :versionadded: 15.3.0.

        :param config: dictionary containing new configuration
          for a given pipeline.
        :param etag: etag value from current configuration resource.
        :param pipeline_name: name of the pipeline. Could be skipped
          if name was configured from constructor.
        :return: updated pipeline config object.
        :rtype: yagocd.resources.pipeline_config.PipelineConfig
        """
        pipeline_name = self._require_param('pipeline_name', locals())

        response = self._session.put(
            path=self._session.urljoin(self.RESOURCE_PATH, pipeline_name).format(base_api=self.base_api),
            data=json.dumps(config),
            headers={
                'Accept': self._accept_header(),
                'Content-Type': 'application/json',
                'If-Match': etag,
            },
        )

        etag = response.headers['ETag']
        return PipelineConfig(session=self._session, data=response.json(), etag=etag)

    def create(self, config):
        """
        Creates new pipeline.

        :versionadded: 15.3.0.

        :param config: configuration data.
        :return: created pipeline config object.
        :rtype: yagocd.resources.pipeline_config.PipelineConfig
        """
        response = self._session.post(
            path=self.RESOURCE_PATH.format(base_api=self.base_api),
            data=json.dumps(config),
            headers={
                'Accept': self._accept_header(),
                'Content-Type': 'application/json',
            },
        )

        etag = response.headers['ETag']
        return PipelineConfig(session=self._session, data=response.json(), etag=etag)

    @since('16.6.0')
    def delete(self, pipeline_name=None):
        """
        Deletes a pipeline.

        :versionadded: 16.6.0.

        :param pipeline_name: name of pipeline to delete
        :return: A message confirmation if the pipeline was deleted.
        :rtype: str
        """
        pipeline_name = self._require_param('pipeline_name', locals())

        response = self._session.delete(
            path=self._session.urljoin(self.RESOURCE_PATH, pipeline_name).format(base_api=self.base_api),
            headers={
                'Accept': self._accept_header(),
            },
        )

        return response.json().get('message')


class PipelineConfig(Base):
    pass
