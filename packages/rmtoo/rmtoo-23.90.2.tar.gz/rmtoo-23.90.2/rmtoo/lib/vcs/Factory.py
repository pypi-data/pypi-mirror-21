'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Factory for different input types.
   
 (c) 2010-2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.vcs.Git import Git
from rmtoo.lib.vcs.FileSystem import FileSystem
from rmtoo.lib.logging import tracer

#pylint: disable=W0232
class Factory:

    known_input_types = \
        { "git": Git,
          "filesystem": FileSystem }

    @staticmethod
    def create(input_method, input_config):
        '''Create new input handler from given parameters.'''
        tracer.info("Called: name [%s]." % input_method)

        if input_method.startswith("ignore:"):
            tracer.info("Ignoring factory entry.")
            return None

        if input_method not in Factory.known_input_types:
            assert False

        return Factory.known_input_types[input_method](input_config)
