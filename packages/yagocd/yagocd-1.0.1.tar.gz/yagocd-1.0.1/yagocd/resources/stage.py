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
from yagocd.resources import Base, BaseManager
from yagocd.resources.job import JobInstance
from yagocd.util import RequireParamMixin, since


@since('14.3.0')
class StageManager(BaseManager, RequireParamMixin):
    """
    The stages API allows users to view stage information and operate on it.

    `Official documentation. <https://api.go.cd/current/#stages>`_

    :versionadded: 14.3.0.
    """

    RUN_RESOURCE_PATH = '{base_api}/run/{pipeline_name}/{pipeline_counter}/{stage_name}'
    RESOURCE_PATH = '{base_api}/stages/{pipeline_name}/{stage_name}'

    def __init__(
        self,
        session,
        pipeline_name=None,
        pipeline_counter=None,
        stage_name=None,
        stage_counter=None,
    ):
        super(StageManager, self).__init__(session)

        self._pipeline_name = pipeline_name
        self._pipeline_counter = pipeline_counter
        self._stage_name = stage_name
        self._stage_counter = stage_counter

    def run(self, pipeline_name=None, pipeline_counter=None, stage_name=None):
        """
        Run stage, configured for manual trigger.

        :versionadded: 14.3.0.

        :param pipeline_name: pipeline name.
        :param stage_name: stage name.
        :param pipeline_counter: pipeline counter.
        :return: Nothing.
        """
        assert self._pipeline_name or pipeline_name
        assert self._pipeline_counter or pipeline_counter
        assert self._stage_name or stage_name

        self._session.post(
            path=self.RUN_RESOURCE_PATH.format(
                base_api=self._session.base_api(api_path=''),
                pipeline_name=self._pipeline_name or pipeline_name,
                pipeline_counter=self._pipeline_counter or pipeline_counter,
                stage_name=self._stage_name or stage_name
            ),
            headers={
                'Confirm': 'true'
            },
        )

    def cancel(self, pipeline_name=None, stage_name=None):
        """
        Cancel an active stage of a specified stage.

        :versionadded: 14.3.0.

        :param pipeline_name: pipeline name.
        :param stage_name: stage name.
        :return: a text confirmation.
        """
        func_args = locals()
        pipeline_name = self._require_param('pipeline_name', func_args)
        stage_name = self._require_param('stage_name', func_args)

        response = self._session.post(
            path=self._session.urljoin(self.RESOURCE_PATH, 'cancel').format(
                base_api=self.base_api,
                pipeline_name=pipeline_name,
                stage_name=stage_name
            ),
            headers={
                'Accept': 'application/json',
                'Confirm': 'true'
            },
        )
        return response.text

    @since('15.1.0')
    def get(
        self,
        pipeline_name=None,
        pipeline_counter=None,
        stage_name=None,
        stage_counter=None
    ):
        """
        Gets stage instance object.

        :versionadded: 15.1.0.

        :param pipeline_name: pipeline name.
        :param stage_name: stage name.
        :param pipeline_counter: pipeline counter.
        :param stage_counter: stage counter.
        :return: a stage instance object :class:`yagocd.resources.stage.StageInstance`.
        :rtype: yagocd.resources.stage.StageInstance
        """
        func_args = locals()
        pipeline_name = self._require_param('pipeline_name', func_args)
        pipeline_counter = self._require_param('pipeline_counter', func_args)
        stage_name = self._require_param('stage_name', func_args)
        stage_counter = self._require_param('stage_counter', func_args)

        response = self._session.get(
            path=self._session.urljoin(self.RESOURCE_PATH, 'instance', pipeline_counter, stage_counter).format(
                base_api=self.base_api,
                pipeline_name=pipeline_name,
                stage_name=stage_name
            ),
            headers={'Accept': 'application/json'},
        )

        return StageInstance(session=self._session, data=response.json(), pipeline=None)

    def history(self, pipeline_name=None, stage_name=None, offset=0):
        """
        The stage history allows users to list stage instances of specified stage.
        Supports pagination using offset which tells the API how many instances to skip.

        :versionadded: 14.3.0.

        :param pipeline_name: pipeline name.
        :param stage_name: stage name.
        :param offset: how many instances to skip.
        :return: an array of stage instances :class:`yagocd.resources.stage.StageInstance`.
        :rtype: list of yagocd.resources.stage.StageInstance
        """
        func_args = locals()
        pipeline_name = self._require_param('pipeline_name', func_args)
        stage_name = self._require_param('stage_name', func_args)

        response = self._session.get(
            path=self._session.urljoin(self.RESOURCE_PATH, 'history', offset).format(
                base_api=self.base_api,
                pipeline_name=pipeline_name,
                stage_name=stage_name
            ),
            headers={'Accept': 'application/json'},
        )

        instances = list()
        for instance in response.json().get('stages'):
            instances.append(StageInstance(session=self._session, data=instance, pipeline=None))

        return instances

    def full_history(self, pipeline_name=None, stage_name=None):
        """
        The stage history allows users to list stage instances of specified stage.

        This method uses generator to get full stage history.
        :param pipeline_name: pipeline name.
        :param stage_name: stage name.
        :return: an array of stage instances :class:`yagocd.resources.stage.StageInstance`.
        :rtype: list of yagocd.resources.stage.StageInstance
        """
        offset = 0
        instances = self.history(pipeline_name, stage_name, offset)
        while instances:
            for instance in instances:
                yield instance

            offset += len(instances)
            instances = self.history(pipeline_name, stage_name, offset)

    def last(self, pipeline_name=None, stage_name=None):
        """
        Get last stage instance.

        :param pipeline_name: name of the pipeline.
        :param stage_name: name of the stage.
        :rtype: yagocd.resources.pipeline.PipelineInstance
        """
        stage_history = self.history(pipeline_name=pipeline_name, stage_name=stage_name)
        if stage_history:
            return stage_history[0]


class StageInstance(Base):
    """
    Class representing instance of specific stage.
    """

    def __init__(self, session, data, pipeline):
        super(StageInstance, self).__init__(session, data)
        self._pipeline = pipeline

        self._manager = StageManager(session=self._session)

    def __iter__(self):
        """
        Method for iterating over jobs of a current stage.

        :return: arrays of jobs.
        :rtype: list of yagocd.resources.job.JobInstance
        """
        return iter(self.jobs())

    def __getitem__(self, name):
        """
        Method for accessing to specific job in array-like manner by name.

        :param name: name of the job to get.
        :return: found job or None.
        :rtype: yagocd.resources.job.JobInstance
        """
        return self.job(name=name)

    @property
    def url(self):
        """
        Returns url for accessing stage instance.
        """
        return "{server_url}/go/pipelines/{pipeline_name}/{pipeline_counter}/{stage_name}/{stage_counter}".format(
            server_url=self._session.server_url,
            pipeline_name=self.pipeline_name,
            pipeline_counter=self.pipeline_counter,
            stage_name=self.data.name,
            stage_counter=self.data.counter,
        )

    @property
    def pipeline_name(self):
        """
        Get pipeline name of current stage instance.

        Because instantiating stage instance could be performed in different ways and those return different results,
        we have to check where from to get name of the pipeline.

        :return: pipeline name.
        """
        if 'pipeline_name' in self.data:
            return self.data.get('pipeline_name')
        elif self.pipeline is not None:
            return self.pipeline.data.name

    @property
    def pipeline_counter(self):
        """
        Get pipeline counter of current stage instance.

        Because instantiating stage instance could be performed in different ways and those return different results,
        we have to check where from to get counter of the pipeline.

        :return: pipeline counter.
        """
        if 'pipeline_counter' in self.data:
            return self.data.get('pipeline_counter')
        elif self.pipeline is not None:
            return self.pipeline.data.counter

    @property
    def stage_name(self):
        """
        Get stage name of current instance.

        This method is to be inline with others.

        :return: stage name.
        """
        if 'name' in self.data:
            return self.data.get('name')

    @property
    def stage_counter(self):
        """
        Get stage counter of current instance.

        This method is to be inline with others.

        :return: stage counter.
        """
        if 'counter' in self.data:
            return self.data.get('counter')

    @property
    def pipeline(self):
        return self._pipeline

    def cancel(self):
        """
        Cancel an active stage of a specified stage.

        :return: a text confirmation.
        """
        return self._manager.cancel(pipeline_name=self.pipeline_name, stage_name=self.stage_name)

    def jobs(self):
        """
        Method for getting jobs from stage instance.

        :return: arrays of jobs.
        :rtype: list of yagocd.resources.job.JobInstance
        """
        jobs = list()
        for data in self.data.jobs:
            jobs.append(JobInstance(session=self._session, data=data, stage=self))

        return jobs

    def job(self, name):
        """
        Method for searching specific job by it's name.

        :param name: name of the job to search.
        :return: found job or None.
        :rtype: yagocd.resources.job.JobInstance
        """
        for job in self.jobs():
            if job.data.name == name:
                return job


class StageResult(object):
    """
    Enumeration of the Stage results.

    These values are used to represent real status of a Stage.
    Looks like they're calculated as aggregated value of each
    Job's status.

    :url: https://github.com/gocd/gocd/blob/master/domain/src/com/thoughtworks/go/domain/StageResult.java
    """
    Passed = 'Passed'
    Failed = 'Failed'
    Cancelled = 'Cancelled'
    Unknown = 'Unknown'


class StageState(object):
    """
    Enumeration of the Stage statuses.

    These statuses are used to determine general status of a given Stage
    from the status of it's Jobs. The values from this enum are used in
    Jobs `state` parameter.

    :url: https://github.com/gocd/gocd/blob/master/domain/src/com/thoughtworks/go/domain/StageState.java
    """
    Building = 'Building'
    Failing = 'Failing'
    Passed = 'Passed'
    Failed = 'Failed'
    Unknown = 'Unknown'
    Cancelled = 'Cancelled'

    StateToResult = {
        Building: StageResult.Unknown,
        Failing: StageResult.Failed,
        Passed: StageResult.Passed,
        Failed: StageResult.Failed,
        Unknown: StageResult.Unknown,
        Cancelled: StageResult.Cancelled,
    }
