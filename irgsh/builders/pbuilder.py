import os
from subprocess import Popen, PIPE

from debian_bundle.deb822 import Changes

from . import BaseBuilder, BuildFailedError
from ..utils import read_rcfile

class Pbuilder(BaseBuilder):
    def __init__(self, distro, **opts):
        super(Pbuilder, self).__init__(distro, **opts)

        self.path = opts['path']
        self.config_file = os.path.join(self.path, self.distro.name,
                                        'pbuilder.conf')
        self.config = read_rcfile(self.config_file)
        self.build_directory = opts.get('build_directory', None)
        self.results_directory = opts.get('results_directory', None)

    def build(self, dsc, stdout=PIPE, stderr=PIPE):
        try:
            current_dir = os.getcwd()
            dirname = os.dirname(dsc)
            os.chdir(dirname)

            # FIXME
            if self.hookdir is not None:
                pass

            args = self.generate_build_arguments(dsc)
            cmd = 'sudo pbuilder %s' % args
            p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
            p.communicate()

            changes = self.get_changes_file(dsc)
            if not os.path.exists(changes):
                raise BuildFailedError(dsc)

            return changes
        finally:
            os.chdir(current_dir)

    def get_changes_file(self, dsc):
        changes = Changes(open(dsc))
        version = changes['Version'].split(':')[-1]

        changes_name = '%s_%s_%s.changes' % (changes['Source'], version,
                                             self.architecture)
        fname = os.path.join(self.result_directory, changes_name)

        return fname

    def generate_arguments(self):
        args = []

        if self.build_directory is not None:
            args.append('--buildplace %s' % self.build_directory)

        if self.results_directory is not None:
            args.append('--buildresult %s' % self.results_directory)

        # FIXME
        self.components = None
        if self.components is not None:
            # FIXME
            self.hookdir = None
            if os.path.isdir(self.hookdir)

        # FIXME
        self.pbuilder_path = "/var/lib/irgsh/pbuilder"
        configfile = os.path.join(self.pbuilder_path, self.distro.name,
                                  'pbuilder.conf')
        args.append('--configfile %s' % configfile)

        return ' '.join(args)

    def generate_build_arguments(self, dsc):
        args = ['build']
        args.append(self.generate_arguments())
        args.append(dsc)

        return ' '.join(args)

