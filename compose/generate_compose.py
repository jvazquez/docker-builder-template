#!/usr/local/bin/python2.7
# encoding: utf-8
'''
compose.generate_compose -- docker file generator

compose.generate_compose is a simple command line application that generates a
docker-compose.yml file

It defines classes_and_methods

@author:     jvazquez

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    jorgeomar.vazquez@gmail.com
@deffield    updated: Updated
'''
import codecs

import logging
import os
import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from os import getenv

from jinja2 import Environment, FileSystemLoader

from constants import get_config, setup_log  # @UnresolvedImport

__all__ = []
__version__ = 0.1
__date__ = "2016-04-10"
__updated__ = "2016-04-10"

DEBUG = os.getenv("DEBUG", 0)
TESTRUN = os.getenv("TESTRUN", 0)
PROFILE = os.getenv("PROFILE", 0)
CONFIG_SECTION = "generator"
conf_class = getenv("CONFIG", None)

logger = logging.getLogger(__name__)


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        setup_log()
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose",
                            action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include",
                            help="only include paths matching this regex "
                            "pattern. "
                            "Note: exclude is given preference over include. "
                            "[default: %(default)s]", metavar="RE")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)
        parser.add_argument("-g", "--generate", help="This program generates "
                            "the docker compose file")
        # Process arguments
        args = parser.parse_args()
        logger.info("The config section is {}".format(CONFIG_SECTION))

        config = get_config()
        if args.generate:
            template_dir = config.get(CONFIG_SECTION, "template_dir")
            template_file = config.get(CONFIG_SECTION, "template_file")
            output_template = config.get(CONFIG_SECTION, "output_template")
            logger.debug("Template dir: {}\nTemplate file:{}\nOutput name:{}"
                         .format(template_dir, template_file, output_template))
            env = Environment(loader=FileSystemLoader(template_dir))
            configuration = env.get_template(template_file)
            config_variables = {}

            configured = configuration.render(config_variables)
            configuration_template = codecs.open(output_template,
                                                 "w", "utf8")
            configuration_template.write(configured)
            configuration_template.close()

        return 0
    except KeyboardInterrupt:
        # ## handle keyboard interrupt ###
        logger.exception("User interrupted the execution")
        return 0
    except Exception:
        logger.exception("Error while running the application")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'compose.generate_compose_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    logger.debug("Application launched using {}".format(conf_class))
    sys.exit(main())