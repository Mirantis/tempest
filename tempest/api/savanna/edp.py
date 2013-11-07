# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import string
import time
import uuid

from tempest.api.savanna import base
from tempest.openstack.common import excutils


class EDPTest(base.BaseSavannaTest):

    def __create_data_source(self, name, data_type, url, description=''):
        return self.savanna.data_sources.create(
            name, description, data_type, url, self.config.identity.username,
            self.config.identity.password).id

    def __create_job_binary_internals(self, name, data):
        return self.savanna.job_binary_internals.create(name, data).id

    def __create_job_binary(self, name, url):
        return self.savanna.job_binaries.create(name, url,
                                                description='', extra={}).id

    def __create_job(self, name, job_type, mains, libs):
        return self.savanna.jobs.create(name, job_type, mains, libs,
                                        description='').id

    def __await_job_execution(self, job):

        timeout = self.config.savanna_common.job_launch_timeout * 60
        status = self.savanna.job_executions.get(job.id).info['status']

        while status != 'SUCCEEDED':

            print('JOB STATUS: ' + status)
            print (timeout)

            if status == 'KILLED':
                self.fail('Job status == \'KILLED\'.')

            if timeout <= 0:
                self.fail(
                    'Job did not return to \'SUCCEEDED\' status within '
                    '%d minute(s).' %
                    self.config.savanna_common.job_launch_timeout)
            time.sleep(10)
            status = self.savanna.job_executions.get(job.id).info['status']
            timeout -= 10

    def __crete_job_biraries(self, job_data_list, job_binary_internal_list,
                             job_binary_list):

        for job_data in job_data_list:

            name = 'binary-job-%s' % str(uuid.uuid4())[:8]

            if isinstance(job_data, dict):
                for key, value in job_data.items():
                        name = 'binary-job-%s.%s' % (str(uuid.uuid4())[:8],
                                                     key)
                        data = value

            else:
                data = job_data

            job_binary_internal_list.append(
                self.__create_job_binary_internals(name, data))

            job_binary_list.append(
                self.__create_job_binary(
                    name, "savanna-db://%s" % job_binary_internal_list[-1]))

    def __delete_job(self, execution_job, job_id, job_binary_list,
                     job_binary_internal_list, input_id, output_id):

        if execution_job:
            self.savanna.job_executions.delete(execution_job.id)

        if job_id:
            self.savanna.jobs.delete(job_id)

        if job_binary_list:
            for job_binary_id in job_binary_list:
                self.savanna.job_binaries.delete(job_binary_id)

        if job_binary_internal_list:
            for internal_id in job_binary_internal_list:
                self.savanna.job_binary_internals.delete(internal_id)

        if input_id:
            self.savanna.data_sources.delete(input_id)

        if output_id:
            self.savanna.data_sources.delete(output_id)

    @base.skip_test('SKIP_EDP_TEST',
                    'Test for EDP was skipped.')
    def _edp_testing(self, job_type, job_data_list, lib_data_list=None,
                     configs=None):

        resp, body = self.container_client.create_container(
            self.container_name)

        if resp.status != 201:

            self.fail("swift container is not created: %s" % str(body))

        resp, body = self.object_client.create_object(
            self.container_name, 'input',
            ''.join(random.choice(':' + ' ' + '\n' + string.ascii_lowercase)
                    for x in range(10000)))

        if resp.status != 201:

            self.delete_swift_container(self.container_name)

            self.fail("swift object is not created: %s" % str(body))

        input_id = None
        output_id = None
        job_id = None
        job_execution = None

        try:

            job_binary_list = []
            lib_binary_list = []
            job_binary_internal_list = []

            input_id = self.__create_data_source(
                'input-%s' % str(uuid.uuid4())[:30], 'swift',
                'swift://%s.savanna/input' % self.container_name)

            output_id = self.__create_data_source(
                'output-%s' % str(uuid.uuid4())[:30], 'swift',
                'swift://%s.savanna/output' % self.container_name)

            if job_data_list:
                self.__crete_job_biraries(
                    job_data_list, job_binary_internal_list, job_binary_list)

            if lib_data_list:
                self.__crete_job_biraries(
                    lib_data_list, job_binary_internal_list, lib_binary_list)

            job_id = self.__create_job(
                'Edp-test-job-%s' % str(uuid.uuid4())[:8], job_type,
                job_binary_list, lib_binary_list)

            if not configs:
                configs = {}

            job_execution = self.savanna.job_executions.create(
                job_id, self.cluster_id, input_id, output_id, configs=configs)

            if job_execution:

                self.__await_job_execution(job_execution)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(str(e))

        finally:

            self.delete_swift_container(self.container_name)

            self.__delete_job(job_execution, job_id,
                              job_binary_list + lib_binary_list,
                              job_binary_internal_list, input_id, output_id)
