from mock import patch, call

import mock

from .test_helper import raises

from kiwi.partitioner.gpt import PartitionerGpt
from kiwi.exceptions import KiwiPartitionerGptFlagError


class TestPartitionerGpt(object):
    def setup(self):
        disk_provider = mock.Mock()
        disk_provider.get_device = mock.Mock(
            return_value='/dev/loop0'
        )
        self.partitioner = PartitionerGpt(disk_provider)

    @patch('kiwi.partitioner.gpt.Command.run')
    @patch('kiwi.partitioner.gpt.PartitionerGpt.set_flag')
    def test_create(self, mock_flag, mock_command):
        self.partitioner.create('name', 100, 't.linux', ['t.csm'])
        mock_command.assert_called_once_with(
            ['sgdisk', '-n', '1:0:+100M', '-c', '1:name', '/dev/loop0']
        )
        call = mock_flag.call_args_list[0]
        assert mock_flag.call_args_list[0] == \
            call(1, 't.linux')
        call = mock_flag.call_args_list[1]
        assert mock_flag.call_args_list[1] == \
            call(1, 't.csm')

    @patch('kiwi.partitioner.gpt.Command.run')
    @patch('kiwi.partitioner.gpt.PartitionerGpt.set_flag')
    def test_create_all_free(self, mock_flag, mock_command):
        self.partitioner.create('name', 'all_free', 't.linux')
        mock_command.assert_called_once_with(
            ['sgdisk', '-n', '1:0:0', '-c', '1:name', '/dev/loop0']
        )

    @raises(KiwiPartitionerGptFlagError)
    def test_set_flag_invalid(self):
        self.partitioner.set_flag(1, 'foo')

    @patch('kiwi.partitioner.gpt.Command.run')
    def test_set_flag(self, mock_command):
        self.partitioner.set_flag(1, 't.csm')
        mock_command.assert_called_once_with(
            ['sgdisk', '-t', '1:EF02', '/dev/loop0']
        )

    @patch('kiwi.logger.log.warning')
    def test_set_flag_ignored(self, mock_warn):
        self.partitioner.set_flag(1, 'f.active')
        assert mock_warn.called

    @patch('kiwi.partitioner.gpt.Command.run')
    def test_set_hybrid_mbr(self, mock_command):
        self.partitioner.partition_id = 5
        self.partitioner.set_hybrid_mbr()
        mock_command.assert_called_once_with(
            ['sgdisk', '-h', '1:2:3', '/dev/loop0']
        )

    @patch('kiwi.partitioner.gpt.Command.run')
    def test_set_mbr(self, mock_command):
        command_output = mock.Mock()
        command_output.output = '...(EFI System)'
        self.partitioner.partition_id = 4
        mock_command.return_value = command_output
        self.partitioner.set_mbr()
        assert mock_command.call_args_list == [
            call(['sgdisk', '-i=1', '/dev/loop0']),
            call(['sgdisk', '-i=2', '/dev/loop0']),
            call(['sgdisk', '-i=3', '/dev/loop0']),
            call(['sgdisk', '-i=4', '/dev/loop0']),
            call(['sgdisk', '-m', '1:2:3:4', '/dev/loop0']),
            call(['sgdisk', '-t', '4:8300', '/dev/loop0'])
        ]
