from conductr_cli import bndl_utils
from conductr_cli.constants import \
    BNDL_DEFAULT_COMPATIBILITY_VERSION, \
    BNDL_DEFAULT_DISK_SPACE, \
    BNDL_DEFAULT_MEMORY, \
    BNDL_DEFAULT_NR_OF_CPUS, \
    BNDL_DEFAULT_ROLES, \
    BNDL_DEFAULT_VERSION
from conductr_cli.test.cli_test_case import CliTestCase, create_attributes_object
from io import BytesIO
from pyhocon import ConfigFactory
import os
import shutil
import tempfile


class TestBndlUtils(CliTestCase):
    def test_detect_format_stream(self):
        # empty stream is none
        self.assertEqual(
            bndl_utils.detect_format_stream(b''),
            None
        )

        # unrelated stream is none
        self.assertEqual(
            bndl_utils.detect_format_stream(b'hello world this is a test'),
            None
        )

        # docker save without tag starts with a hex digest tar dir entry
        self.assertEqual(
            bndl_utils.detect_format_stream(b'194853445611786369d26c17093e481cdc14c838375091037f780fe22aa760e7/'
                                            b'\x00\x00\x00'),
            'docker'
        )

        # docker save with a tag starts with a json tar file entry
        self.assertEqual(
            bndl_utils.detect_format_stream(b'4a415e3663882fbc554ee830889c68a33b3585503892cc718a4698e91ef2a526.json'
                                            b'\x00\x00\x00'),
            'docker'
        )

        # docker from a tar stream of a dir on disk, we just hope the order works out
        self.assertEqual(
            bndl_utils.detect_format_stream(b'\x00/manifest.json\x00\x00\x00/layer.tar\x00\x00\x00'),
            'docker'
        )

        # oci image from a tar stream of a dir on disk, we just hope the order works out
        self.assertEqual(
            bndl_utils.detect_format_stream(b'\x00/oci-layout\x00\x00\x00/refs/\x00\x00\x00'),
            'oci-image'
        )

    def test_detect_format_dir(self):
        docker_dir = tempfile.mkdtemp()
        oci_image_dir = tempfile.mkdtemp()
        nothing_dir = tempfile.mkdtemp()

        try:
            os.mkdir(os.path.join(oci_image_dir, 'refs'))
            os.mkdir(os.path.join(oci_image_dir, 'blobs'))

            open(os.path.join(oci_image_dir, 'oci-layout'), 'a').close()
            open(os.path.join(docker_dir, 'repositories'), 'a').close()
            open(os.path.join(docker_dir, 'manifest.json'), 'a').close()
            open(os.path.join(nothing_dir, 'hello'), 'a').close()

            self.assertEqual(bndl_utils.detect_format_dir(oci_image_dir), 'oci-image')
            self.assertEqual(bndl_utils.detect_format_dir(docker_dir), 'docker')
            self.assertEqual(bndl_utils.detect_format_dir(nothing_dir), None)
        finally:
            shutil.rmtree(docker_dir)
            shutil.rmtree(oci_image_dir)
            shutil.rmtree(nothing_dir)

    def test_digest_reader_writer(self):
        data = b'some data'
        digest = '1307990e6ba5ca145eb35e99182a9bec46531bc54ddf656a602c780fa0240dee'
        digest_empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

        bytes_io = BytesIO(data)

        reader = bndl_utils.DigestReaderWriter(bytes_io)
        writer = bndl_utils.DigestReaderWriter(BytesIO())

        shutil.copyfileobj(reader, writer)

        self.assertEqual(reader.digest_in.hexdigest(), digest)
        self.assertEqual(reader.digest_out.hexdigest(), digest_empty)
        self.assertEqual(reader.size_in, 9)
        self.assertEqual(reader.size_out, 0)
        self.assertEqual(writer.digest_in.hexdigest(), digest_empty)
        self.assertEqual(writer.digest_out.hexdigest(), digest)
        self.assertEqual(writer.size_in, 0)
        self.assertEqual(writer.size_out, 9)

    def test_load_bundle_args_into_conf(self):
        base_args = create_attributes_object({
            'name': 'world',
            'component_description': 'testing desc 1',
            'tag': 'testing',
            'annotations': {}
        })

        extended_args = create_attributes_object({
            'name': 'world',
            'component_description': 'testing desc 2',
            'version': '4',
            'compatibilityVersion': '5',
            'system': 'myapp',
            'systemVersion': '3',
            'nrOfCpus': '8',
            'memory': '65536',
            'diskSpace': '16384',
            'roles': ['web', 'backend'],
            'tag': 'latest',
            'annotations': ['com.lightbend.test=hello world', 'description=this is a test']
        })

        # test that config value is specified, with defaults etc
        simple_config = ConfigFactory.parse_string('')
        bndl_utils.load_bundle_args_into_conf(simple_config, base_args)
        self.assertEqual(simple_config.get('name'), 'world')
        self.assertEqual(simple_config.get('compatibilityVersion'), BNDL_DEFAULT_COMPATIBILITY_VERSION)
        self.assertEqual(simple_config.get('diskSpace'), BNDL_DEFAULT_DISK_SPACE)
        self.assertEqual(simple_config.get('memory'), BNDL_DEFAULT_MEMORY)
        self.assertEqual(simple_config.get('nrOfCpus'), BNDL_DEFAULT_NR_OF_CPUS)
        self.assertEqual(simple_config.get('roles'), BNDL_DEFAULT_ROLES)
        self.assertEqual(simple_config.get('system'), 'world')
        self.assertEqual(simple_config.get('version'), BNDL_DEFAULT_VERSION)
        self.assertEqual(simple_config.get('tags'), ['testing'])

        # test that config value is overwritten
        name_config = ConfigFactory.parse_string('name = "hello"')
        bndl_utils.load_bundle_args_into_conf(name_config, base_args)
        self.assertEqual(name_config.get('name'), 'world')

        # test that config value is retained
        cpu_config = ConfigFactory.parse_string('nrOfCpus = 0.1')
        bndl_utils.load_bundle_args_into_conf(cpu_config, base_args)
        self.assertEqual(cpu_config.get('nrOfCpus'), 0.1)

        config = ConfigFactory.parse_string('')
        bndl_utils.load_bundle_args_into_conf(config, extended_args)

        # test that various args are set correctly
        self.assertEqual(config.get('name'), 'world')
        self.assertEqual(config.get('version'), '4')
        self.assertEqual(config.get('compatibilityVersion'), '5')
        self.assertEqual(config.get('system'), 'myapp')
        self.assertEqual(config.get('systemVersion'), '3')
        self.assertEqual(config.get('nrOfCpus'), '8')
        self.assertEqual(config.get('memory'), '65536')
        self.assertEqual(config.get('diskSpace'), '16384')
        self.assertEqual(config.get('roles'), ['web', 'backend'])

        # test that the "latest" tag is ignored
        self.assertEqual(config.get('tags'), [])

        # test that we add to tags that exist
        tag_config = ConfigFactory.parse_string('{ tags = ["hello"] }')
        bndl_utils.load_bundle_args_into_conf(tag_config, base_args)
        self.assertEqual(tag_config.get('tags'), ['hello', 'testing'])

        # test that we only retain unique tags
        tag_config = ConfigFactory.parse_string('{ tags = ["testing"] }')
        bndl_utils.load_bundle_args_into_conf(tag_config, base_args)
        self.assertEqual(tag_config.get('tags'), ['testing'])

        # annotations added
        annotations_config = ConfigFactory.parse_string('{ annotations = { name = "my-name" } }')
        bndl_utils.load_bundle_args_into_conf(annotations_config, extended_args)
        self.assertEqual(annotations_config.get('annotations'), {
            'name': 'my-name',
            'com': {
                'lightbend': {
                    'test': 'hello world'
                }
            },
            'description': 'this is a test'
        })
