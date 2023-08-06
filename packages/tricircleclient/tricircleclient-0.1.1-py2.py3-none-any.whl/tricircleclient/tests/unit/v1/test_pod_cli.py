#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from tricircleclient.tests.unit import utils
from tricircleclient.v1 import pods_cli


class TestCreatePod(utils.TestCommand):

    def setUp(self):
        super(TestCreatePod, self).setUp()
        self.cmd = pods_cli.CreatePod(self.app, None)

        self._local_data = {
            'region_name': 'central_region',
        }

        self._local_data_with_az = dict(self._local_data)
        self._local_data_with_az.update({
            'az_name': 'availability_zone',
        })
        self._pod_all_options = dict(self._local_data_with_az)
        self._pod_all_options.update({
            'pod_az_name': 'pod',
            'dc_name': 'datacenter',
        })

        self.pod_manager = self.app.client_manager.multiregion_networking.pod

    def test_create_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(
            utils.ParserException, self.check_parser, self.cmd, arglist,
            verifylist)

    def test_create_all_options(self):
        arglist = [
            '--region-name', self._pod_all_options['region_name'],
            '--availability-zone', self._pod_all_options['az_name'],
            '--pod-availability-zone', self._pod_all_options['pod_az_name'],
            '--data-center', self._pod_all_options['dc_name']
        ]
        verifylist = [
            ('region_name', self._pod_all_options['region_name']),
            ('availability_zone', self._pod_all_options['az_name']),
            ('pod_availability_zone', self._pod_all_options['pod_az_name']),
            ('data_center', self._pod_all_options['dc_name']),
        ]
        self.pod_manager.create = mock.Mock(
            return_value={'pod': self._pod_all_options})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(
            sorted(self._pod_all_options.keys()), sorted(columns))
        self.assertEqual(
            sorted(self._pod_all_options.values()), sorted(data))

    def test_create_local_region_with_availability_zone(self):
        arglist = [
            '--region-name', self._local_data_with_az['region_name'],
            '--availability-zone', self._local_data_with_az['az_name']
        ]
        verifylist = [
            ('region_name', self._local_data_with_az['region_name']),
            ('availability_zone', self._local_data_with_az['az_name']),
        ]
        self.pod_manager.create = mock.Mock(
            return_value={'pod': self._local_data_with_az})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(
            sorted(self._local_data_with_az.keys()), sorted(columns))
        self.assertEqual(
            sorted(self._local_data_with_az.values()), sorted(data))

    def test_create_central_region(self):
        arglist = [
            '--region-name', self._local_data['region_name']
        ]
        verifylist = [
            ('region_name', self._local_data['region_name']),
        ]
        self.pod_manager.create = mock.Mock(
            return_value={'pod': self._local_data})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(self._local_data.keys()), sorted(columns))
        self.assertEqual(sorted(self._local_data.values()), sorted(data))


class TestShowPod(utils.TestCommand):

    def setUp(self):
        super(TestShowPod, self).setUp()
        self.cmd = pods_cli.ShowPod(self.app, None)
        self.pod_manager = self.app.client_manager.multiregion_networking.pod

    def test_show_without_pod_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(
            utils.ParserException, self.check_parser, self.cmd, arglist,
            verifylist)

    def test_show_valid_pod(self):
        _pod = utils.FakePod.create_single_pod()
        arglist = [
            _pod['pod']['pod_id'],
            ]
        verifylist = [
            ("pod", _pod['pod']['pod_id']),
            ]
        self.pod_manager.get = mock.Mock(
            return_value={'pod': _pod})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))
        self.assertEqual(
            sorted(_pod.keys()), sorted(columns))
        self.assertEqual(
            sorted(_pod.values()), sorted(data))

    def test_show_valid_pod_with_empty_fields(self):
        keys = ["dc_name", "pod_az_name", "az_name"]
        _pod = utils.FakePod.create_single_pod({key: " " for key in keys})
        arglist = [
            _pod['pod']['pod_id'],
            ]
        verifylist = [
            ("pod", _pod['pod']['pod_id']),
            ]
        self.pod_manager.get = mock.Mock(
            return_value={'pod': _pod})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))
        self.assertEqual(
            sorted(_pod.keys()), sorted(columns))
        self.assertEqual(
            sorted(_pod.values()), sorted(data))


class TestListPod(utils.TestCommand):

    _pod = utils.FakePod.create_single_pod()
    columns = [
        'Id',
        'Region name',
    ]

    data = []
    data.append((_pod['pod']['pod_id'], _pod['pod']['region_name']))

    def setUp(self):
        super(TestListPod, self).setUp()
        self.cmd = pods_cli.ListPods(self.app, None)
        self.pod_manager = self.app.client_manager.multiregion_networking.pod

    def test_list(self):
        arglist = []
        verifylist = []
        self.pod_manager.list = mock.Mock(
            return_value={'pods': [self._pod['pod']]})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))
        self.assertEqual(self.columns, sorted(columns))
        self.assertEqual(self.data, sorted(data))


class TestDeletePod(utils.TestCommand):

    def setUp(self):
        super(TestDeletePod, self).setUp()
        self.cmd = pods_cli.DeletePod(self.app, None)
        self.pod_manager = self.app.client_manager.multiregion_networking.pod

    def test_delete_pod_without_options(self):
        self.assertRaises(
            utils.ParserException, self.check_parser, self.cmd, [], [])

    def test_delete_pod(self):
        arglist = [utils.FakePod.create_single_pod()['pod']['pod_id']]
        verifylist = [
            ('pod', arglist),
            ]
        self.pod_manager.delete = mock.Mock(
            return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        self.assertIsNone(result)

    def test_delete_multiple_pod(self):
        arglist = [pod['pod_id'] for pod in
                   utils.FakePod.create_multiple_pods()]
        verifylist = [
            ('pod', arglist),
            ]
        self.pod_manager.delete = mock.Mock(
            return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        self.assertIsNone(result)
