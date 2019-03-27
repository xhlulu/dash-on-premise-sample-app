import os
from textwrap import dedent


def StaticUrlPath(resource):
    if not os.path.exists(os.path.join('assets', 'images', resource)):
        raise Exception(dedent('''
            The file "{}" does not exist in the "assets/images" folder.
        '''.format(resource, resource)))
    if 'DYNO' in os.environ:
        return '/{}/assets/images/{}'.format(os.environ['DASH_APP_NAME'], resource)
    else:
        return '/assets/images/{}'.format(resource)
