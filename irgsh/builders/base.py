from debian_bundle.deb822 import Changes 

class BuildFailedError(Exception):
    def __init__(self, source):
        self.source = source
    def __str__(self):
        return 'Build failed: %s' % self.source

class BaseBuilder(object):
    def __init__(self, distro, build_directory, result_directory, architecture):
        self.distro = distro
        self.build_directory = directory
        self.result_directory = result_directory
        self.architecture = architecture

    def get_changes_file(self, dsc):
        changes = Changes(open(dsc))
        version = changes['Version'].split(':')[-1]

        changes_name = '%s_%s_%s.changes' % (changes['Source'], version,
                                             self.architecture)
        fname = os.path.join(self.result_directory, changes_name)

        return fname

