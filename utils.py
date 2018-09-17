import os
from textwrap import dedent

import config

def StaticUrlPath(resource):
    if not os.path.exists(os.path.join('assets/images', resource)):
        raise Exception(dedent('''
            The file "{}" does not exist in the "assets/images" folder.
        '''.format(resource, resource)))
    if 'DYNO' in os.environ and config.PATH_BASED_ROUTING:
        return '/{}/assets/images/{}'.format(config.DASH_APP_NAME, resource)
    else:
        return '/assets/images/{}'.format(resource)
