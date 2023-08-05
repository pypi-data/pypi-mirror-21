from mock import call
from mock import patch

import mock

from kiwi.container.docker import ContainerImageDocker


class TestContainerImageDocker(object):
    def setup(self):
        self.docker = ContainerImageDocker(
            'root_dir', {
                'container_name': 'foo/bar'
            }
        )

    def test_init_custom_args(self):
        ContainerImageDocker(
            'root_dir', {
                'container_name': 'foo',
                'container_tag': '1.0',
                'entry_command': [
                    "--config.entrypoint=/bin/bash",
                    "--config.entrypoint=-x"
                ],
                'entry_subcommand': [
                    "--config.cmd=ls",
                    "--config.cmd=-l"
                ],
                'maintainer': ['--author=tux'],
                'user': ['--config.user=root'],
                'workingdir': ['--config.workingdir=/root'],
                'expose_ports': [
                    "--config.exposedports=80",
                    "--config.exposedports=42"
                ],
                'volumes': [
                    "--config.volume=/var/log",
                    "--config.volume=/tmp"
                ],
                'environment': [
                    "--config.env=PATH=/bin'",
                    "--config.env=FOO=bar"
                ],
                'labels': [
                    "--config.label=a=value",
                    "--config.label=b=value"
                ]
            }
        )

    @patch('kiwi.container.docker.Path.wipe')
    def test_del(self, mock_wipe):
        self.docker.docker_dir = 'dir_a'
        self.docker.docker_root_dir = 'dir_b'
        self.docker.__del__()
        assert mock_wipe.call_args_list == [
            call('dir_a'), call('dir_b')
        ]

    @patch('kiwi.container.docker.Compress')
    @patch('kiwi.container.docker.Command.run')
    @patch('kiwi.container.docker.DataSync')
    @patch('kiwi.container.docker.mkdtemp')
    @patch('kiwi.container.docker.Path.wipe')
    @patch('kiwi.container.docker.Defaults.get_shared_cache_location')
    def test_create(
        self, mock_cache, mock_wipe, mock_mkdtemp,
        mock_sync, mock_command, mock_compress
    ):
        mock_cache.return_value = 'var/cache/kiwi'
        compressor = mock.Mock()
        mock_compress.return_value = compressor
        docker_root = mock.Mock()
        mock_sync.return_value = docker_root
        tmpdirs = ['kiwi_docker_root_dir', 'kiwi_docker_dir']

        def call_mkdtemp(prefix):
            return tmpdirs.pop()

        mock_mkdtemp.side_effect = call_mkdtemp

        self.docker.create('result.tar.xz', None)

        mock_wipe.assert_called_once_with('result.tar')

        assert mock_command.call_args_list == [
            call([
                'umoci', 'init', '--layout',
                'kiwi_docker_dir/umoci_layout'
            ]),
            call([
                'umoci', 'new', '--image',
                'kiwi_docker_dir/umoci_layout:latest'
            ]),
            call([
                'umoci', 'unpack', '--image',
                'kiwi_docker_dir/umoci_layout:latest', 'kiwi_docker_root_dir'
            ]),
            call([
                'umoci', 'repack', '--image',
                'kiwi_docker_dir/umoci_layout:latest', 'kiwi_docker_root_dir'
            ]),
            call([
                'umoci', 'config', '--config.cmd=/bin/bash', '--image',
                'kiwi_docker_dir/umoci_layout:latest'
            ]),
            call([
                'umoci', 'gc', '--layout', 'kiwi_docker_dir/umoci_layout'
            ]),
            call([
                'skopeo', 'copy', 'oci:kiwi_docker_dir/umoci_layout:latest',
                'docker-archive:result.tar:foo/bar:latest'
            ])
        ]
        mock_sync.assert_called_once_with(
            'root_dir/', 'kiwi_docker_root_dir/rootfs'
        )
        docker_root.sync_data.assert_called_once_with(
            exclude=[
                'image', '.profile', '.kconfig', 'boot', 'dev', 'sys', 'proc',
                'var/cache/kiwi'
            ],
            options=['-a', '-H', '-X', '-A']
        )
        mock_compress.assert_called_once_with('result.tar')
        compressor.xz.assert_called_once_with()

    @patch('kiwi.container.docker.ArchiveTar')
    @patch('kiwi.container.docker.Compress')
    @patch('kiwi.container.docker.Command.run')
    @patch('kiwi.container.docker.DataSync')
    @patch('kiwi.container.docker.mkdtemp')
    @patch('kiwi.container.docker.Path.wipe')
    @patch('kiwi.container.docker.Path.create')
    @patch('kiwi.container.docker.Defaults.get_shared_cache_location')
    def test_create_derived(
        self, mock_cache, mock_create, mock_wipe, mock_mkdtemp,
        mock_sync, mock_command, mock_compress, mock_tar
    ):
        mock_cache.return_value = 'var/cache/kiwi'
        compressor = mock.Mock()
        mock_compress.return_value = compressor
        docker_root = mock.Mock()
        mock_sync.return_value = docker_root
        tmpdirs = ['kiwi_docker_root_dir', 'kiwi_docker_dir']

        def call_mkdtemp(prefix):
            return tmpdirs.pop()

        mock_mkdtemp.side_effect = call_mkdtemp

        self.docker.create('result.tar.xz', 'root_dir/image/image_file')

        mock_wipe.assert_called_once_with('result.tar')
        mock_tar.assert_called_once_with('root_dir/image/image_file')
        mock_create.assert_called_once_with('kiwi_docker_dir/umoci_layout')

        assert mock_command.call_args_list == [
            call([
                'umoci', 'config', '--image',
                'kiwi_docker_dir/umoci_layout', '--tag', 'latest'
            ]),
            call([
                'umoci', 'unpack', '--image',
                'kiwi_docker_dir/umoci_layout:latest', 'kiwi_docker_root_dir'
            ]),
            call([
                'umoci', 'repack', '--image',
                'kiwi_docker_dir/umoci_layout:latest', 'kiwi_docker_root_dir'
            ]),
            call([
                'umoci', 'config', '--config.cmd=/bin/bash', '--image',
                'kiwi_docker_dir/umoci_layout:latest'
            ]),
            call([
                'umoci', 'gc', '--layout', 'kiwi_docker_dir/umoci_layout'
            ]),
            call([
                'skopeo', 'copy', 'oci:kiwi_docker_dir/umoci_layout:latest',
                'docker-archive:result.tar:foo/bar:latest'
            ])
        ]
        mock_sync.assert_called_once_with(
            'root_dir/', 'kiwi_docker_root_dir/rootfs'
        )
        docker_root.sync_data.assert_called_once_with(
            exclude=[
                'image', '.profile', '.kconfig', 'boot', 'dev', 'sys', 'proc',
                'var/cache/kiwi'
            ],
            options=['-a', '-H', '-X', '-A']
        )
        mock_compress.assert_called_once_with('result.tar')
        compressor.xz.assert_called_once_with()
