import tempfile
import os
import shutil
from unittest import TestCase

from mock import Mock, patch

class SourceTestCase(TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.debian = os.path.join(self.directory, 'debian')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'debian'),
                        self.debian)

    def tearDown(self):
        shutil.rmtree(self.directory)

class OrderedTestCase(SourceTestCase):
    def testContent(self):
        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        self.assertEqual(source.name, 'python-irgsh')
        self.assertEqual(source.maintainer, 'BlankOn Developers <blankon-dev@googlegroups.com>')
        self.assertEqual(source.changed_by, 'mdamt <mdamt@di.blankon.in>')
        self.assertEqual(source.version, '0.1')
        self.assertEqual(source.distribution, 'ombilin')

        changelog = source.last_changelog
        self.assertEqual(changelog.package, 'python-irgsh')
        self.assertEqual(changelog.distributions, 'ombilin')
        self.assertEqual(changelog.urgency, 'low')
        self.assertEqual(changelog.author, 'mdamt <mdamt@di.blankon.in>')
        self.assertEqual(changelog.date, 'Sun, 21 Mar 2010 10:44:56 +0200')

        # TODO source.binaries

class UnorderedTestCase(OrderedTestCase):
    def setUp(self):
        super(UnorderedTestCase, self).setUp()
        shutil.copy(os.path.join(self.debian, 'control.unordered'),
                    os.path.join(self.debian, 'control'))

class DscCallTestCase(SourceTestCase):
    def testNative(self):
        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        generate_dsc_native = Mock()
        generate_dsc_with_orig = Mock()

        @patch.object(source, '_generate_dsc_native', generate_dsc_native)
        @patch.object(source, '_generate_dsc_with_orig', generate_dsc_with_orig)
        def test():
            source.generate_dsc(self.directory)

        test()

        self.assertTrue(generate_dsc_native.called)
        self.assertFalse(generate_dsc_with_orig.called)

    def testWithOrig(self):
        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory, self.directory)

        generate_dsc_native = Mock()
        generate_dsc_with_orig = Mock()

        @patch.object(source, '_generate_dsc_native', generate_dsc_native)
        @patch.object(source, '_generate_dsc_with_orig', generate_dsc_with_orig)
        def test():
            source.generate_dsc(self.directory)

        test()

        self.assertFalse(generate_dsc_native.called)
        self.assertTrue(generate_dsc_with_orig.called)

class FindChangelogTestCase(SourceTestCase):
    def testDefault(self):
        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory)
        self.assertEqual(res, self.directory)

    def testPackageVersion(self):
        package_version = 'python-irgsh-0.1'
        directory = os.path.join(self.directory, package_version)
        os.makedirs(directory)
        shutil.move(self.debian, directory)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory, package_version)
        self.assertEqual(res, directory)

    def testPackageVersionExtraDirectory(self):
        package_version = 'python-irgsh-0.1'
        directory = os.path.join(self.directory, package_version)
        shutil.copytree(self.debian, directory)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory, package_version)
        self.assertEqual(res, self.directory)

    def testPackageVersionMultiple(self):
        package_version_1 = 'python-irgsh'
        directory_1 = os.path.join(self.directory, package_version_1)
        shutil.copytree(self.debian, os.path.join(directory_1, 'debian'))

        package_version_2 = 'python-irgsh-0.1'
        directory_2 = os.path.join(self.directory, package_version_2)
        os.makedirs(directory_2)
        shutil.move(self.debian, directory_2)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory, package_version_1)
        self.assertEqual(res, directory_1)
        self.assertNotEqual(res, directory_2)

        res = source._find_changelog(self.directory, package_version_2)
        self.assertNotEqual(res, directory_1)
        self.assertEqual(res, directory_2)

    def testSingle(self):
        package_version = 'python-irgsh-0.1'
        directory = os.path.join(self.directory, package_version)
        os.makedirs(directory)
        shutil.move(self.debian, directory)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory)
        self.assertEqual(res, directory)

    def testPackageVersionMultiple(self):
        package_version_1 = 'python-irgsh'
        directory_1 = os.path.join(self.directory, package_version_1)
        shutil.copytree(self.debian, os.path.join(directory_1, 'debian'))

        package_version_2 = 'python-irgsh-0.1'
        directory_2 = os.path.join(self.directory, package_version_2)
        os.makedirs(directory_2)
        shutil.move(self.debian, directory_2)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory)
        self.assertEqual(res, None)

    def testNoDebian(self):
        shutil.rmtree(self.debian)

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory)
        self.assertEqual(res, None)

    def testNoDebianChangelog(self):
        os.unlink(os.path.join(self.debian, 'changelog'))

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory)
        self.assertEqual(res, None)

    def testPackageVersionNoDebianChangelog(self):
        package_version = 'python-irgsh-0.1'
        directory = os.path.join(self.directory, package_version)
        os.makedirs(directory)
        shutil.move(self.debian, directory)
        os.unlink(os.path.join(directory, 'debian', 'changelog'))

        from irgsh.packages.source import SourcePackage
        source = SourcePackage(self.directory)

        res = source._find_changelog(self.directory, package_version)
        self.assertEqual(res, None)

