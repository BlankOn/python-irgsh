from unittest import TestCase

__all__ = ['DistributionTestCase']

class DistributionTestCase(TestCase):
    def testDefault(self):
        from irgsh.data import Distribution
        dist = Distribution('lucid', 'http://archive.ubuntu.com/ubuntu/',
                            'lucid')

        self.assertEqual(dist.name, 'lucid')
        self.assertEqual(dist.mirror, 'http://archive.ubuntu.com/ubuntu/')

        self.assertEqual(dist.dist, 'lucid')
        self.assertEqual(dist.components, ['main'])
        self.assertEqual(dist.extra, [])

    def testComplete(self):
        from irgsh.data import Distribution
        dist = Distribution('lucid', 'http://archive.ubuntu.com/ubuntu/',
                            'lucid', ['main', 'restricted'],
                            ['deb http://archive.ubuntu.com/ubuntu/ lucid-updates main restricted',
                             'deb http://archive.ubuntu.com/ubuntu/ lucid-security main restricted'])

        self.assertEqual(dist.name, 'lucid')
        self.assertEqual(dist.mirror, 'http://archive.ubuntu.com/ubuntu/')
        self.assertEqual(dist.dist, 'lucid')
        self.assertEqual(dist.components, ['main', 'restricted'])
        self.assertEqual(dist.extra, ['deb http://archive.ubuntu.com/ubuntu/ lucid-updates main restricted',
                                      'deb http://archive.ubuntu.com/ubuntu/ lucid-security main restricted'])

