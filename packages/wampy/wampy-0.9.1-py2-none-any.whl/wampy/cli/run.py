""" usage

wampy run module:app

Largely experimental for now.... sorry.

"""
import os
import sys
from urlparse import urlparse

from wampy.peers.routers import Crossbar


class CommandError(Exception):
    pass


def import_module(module_name):

    try:
        __import__(module_name)
    except ImportError:
        if module_name.endswith(".py") and os.path.exists(module_name):
            raise CommandError(
                "Failed to find module, did you mean '{}'?".format(
                    module_name[:-3].replace('/', '.')
                )
            )

        raise

    module = sys.modules[module_name]
    return module


class AppRunner(object):

    def __init__(self):
        self.apps = []

    def add_app(self, app):
        self.apps.append(app)

    def run(self):
        for app in self.apps:
            app.start()

    def stop(self):
        for app in self.apps:
            app.stop()

    def wait(self):
        for app in self.apps:
            try:
                app.session._managed_thread.wait()
            except Exception as exc:
                print(exc)
                app.stop()


def run(app, host, port):
    module_name, app_name = app[0].split(':')
    mod = import_module(module_name)
    app_class = getattr(mod, app_name)

    # TODO: realm and roles should be passed in too
    router = Crossbar(host=host, port=port)
    app = app_class(router=router)

    runner = AppRunner()
    runner.add_app(app)
    print("starting up service....")
    runner.run()

    print("{} is now running and connected to {}.".format(app_name, host))

    while True:
        try:
            runner.wait()
        except KeyboardInterrupt:

            try:
                runner.stop()
            except KeyboardInterrupt:
                runner.stop()

        else:
            # runner.wait completed
            break

    print('disconnected')


def main(args):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    app = args.application
    router_url = args.router
    parsed_connection_details = urlparse(router_url)
    host = parsed_connection_details.hostname
    port = parsed_connection_details.port

    if host is None:
        # guess!
        host, port = router_url.split(':')

    run(app, host, int(port))


def init_parser(parser):
    parser.add_argument(
        'application', nargs='+',
        metavar='module[:application class]',
        help='python path to one wampy application class to run')

    parser.add_argument(
        '--router', default='http://localhost:8080',
        help='WAMP router url')

    return parser
