import tempfile
import os
import shutil
from unittest import TestCase

class SourceTestCase(TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.debian = os.path.join(self.directory, 'debian')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'debian'),
                        self.debian)

    def tearDown(self):
        shutil.rmtree(self.directory)

    def testBlah(self):
        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        self.assertEqual(source.name, 'python-irgsh')
        self.assertEqual(source.maintainer, 'BlankOn Developers <blankon-dev@googlegroups.com>')
        self.assertEqual(source.changed_by, 'mdamt <mdamt@di.blankon.in>')
        self.assertEqual(source.version, '0.1')
        self.assertEqual(source.distribution, 'ombilin')

        # TODO source.last_changelog
        # TODO source.binaries

