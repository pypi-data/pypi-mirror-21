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
from yagocd.resources.job import JobInstance
from yagocd.util import since


@since('15.2.0')
class AgentManager(BaseManager):
    """
    The agents API allows users with administrator role to manage agents.

    `Official documentation. <https://api.go.cd/current/#agents>`_

    :versionadded: 15.2.0.

    :warning: Please note that this API requires using v4 of the API using `Accept: application/vnd.go.cd.v4+json`
    """

    RESOURCE_PATH = '{base_api}/agents'

    ACCEPT_HEADER = 'application/vnd.go.cd.v4+json'

    VERSION_TO_ACCEPT_HEADER = {
        '16.1.0': 'application/vnd.go.cd.v1+json',
        '16.7.0': 'application/vnd.go.cd.v2+json',
        '16.9.0': 'application/vnd.go.cd.v3+json',
    }

    def __iter__(self):
        """
        Method add iterator protocol for the manager.

        :return: an array of agents.
        :rtype: list of yagocd.resources.agent.AgentEntity
        """
        return iter(self.list())

    def __getitem__(self, uuid):
        """
        Method add possibility to get agent by the uuid using dictionary like syntax.

        :param uuid: uuid of the agent
        :return: Agent entity.
        :rtype: yagocd.resources.agent.AgentEntity
        """
        return self.get(uuid=uuid)

    def list(self):
        """
        Lists all available agents, these are agents that are present in the
        <agents/> tag inside cruise-config.xml and also agents that are in
        Pending state awaiting registration.

        :versionadded: 15.2.0.

        :return: an array of agents.
        :rtype: list of yagocd.resources.agent.AgentEntity
        """
        response = self._session.get(
            path=self.RESOURCE_PATH.format(base_api=self.base_api),
            headers={'Accept': self._accept_header()},
        )

        agents = list()
        # Depending on Go version, return value would be either list of dict.
        # Support both cases here.
        json_response = response.json()
        if isinstance(json_response, list):
            agents_json = json_response
        elif isinstance(json_response, dict):
            agents_json = json_response.get('_embedded', {}).get('agents', {})
        else:
            raise ValueError("Expected response to be in [list, dict], but '{}' found!".format(json_response))

        for data in agents_json:
            agents.append(AgentEntity(session=self._session, data=data))

        return agents

    def dict(self):
        """
        Wrapper for `list()` method, that transforms founded agents to
        dictionary by `uuid` key.

        :return: dictionary of agents with `uuid` as a key and agent as a value.
        :rtype: dict[str, yagocd.resources.agent.AgentEntity]
        """
        agents = self.list()
        result = dict()
        for agent in agents:
            result[agent.data.uuid] = agent

        return result

    def get(self, uuid):
        """
        Gets an agent by its unique identifier (uuid).

        :versionadded: 15.2.0.

        :param uuid: uuid of the agent
        :return: Agent entity.
        :rtype: yagocd.resources.agent.AgentEntity
        """
        response = self._session.get(
            path=self._session.urljoin(self.RESOURCE_PATH, uuid).format(
                base_api=self.base_api
            ),
            headers={'Accept': self._accept_header()},
        )

        return AgentEntity(session=self._session, data=response.json())

    def update(self, uuid, config):
        """
        Update some attributes of an agent.

        :versionadded: 15.2.0.

        :param uuid: uuid of the agent
        :param config: dictionary of parameters for update
        :return: Agent entity.
        :rtype: yagocd.resources.agent.AgentEntity
        """
        response = self._session.patch(
            path=self._session.urljoin(self.RESOURCE_PATH, uuid).format(
                base_api=self.base_api
            ),
            data=json.dumps(config),
            headers={
                'Accept': self._accept_header(),
                'Content-Type': 'application/json'
            },
        )

        return AgentEntity(session=self._session, data=response.json())

    def delete(self, uuid):
        """
        Deletes an agent.

        :versionadded: 15.2.0.

        :param uuid: uuid of the agent.
        :return: a message confirmation if the agent was deleted.
        """
        response = self._session.delete(
            path=self._session.urljoin(self.RESOURCE_PATH, uuid).format(
                base_api=self.base_api
            ),
            headers={'Accept': self._accept_header()},
        )

        return response.json().get('message')

    @since('14.3.0')
    def job_history(self, uuid, offset=0):
        """
        Lists the jobs that have executed on an agent.

        :versionadded: 14.3.0.

        :param uuid: uuid of the agent.
        :param offset: number of jobs to be skipped.
        :return: an array of :class:`yagocd.resources.job.JobInstance` along with the job transitions.
        :rtype: list of yagocd.resources.job.JobInstance
        """
        response = self._session.get(
            path=self._session.urljoin(self.RESOURCE_PATH, uuid, 'job_run_history', offset).format(
                base_api=self.base_api
            ),
            headers={'Accept': 'application/json'},
        )

        jobs = list()
        for data in response.json()['jobs']:
            jobs.append(JobInstance(session=self._session, data=data, stage=None))
        return jobs


class AgentEntity(Base):
    pass
