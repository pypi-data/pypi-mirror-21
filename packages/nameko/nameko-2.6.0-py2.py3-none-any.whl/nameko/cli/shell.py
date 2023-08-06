import code
import os
import sys
import yaml
from types import ModuleType

from nameko.constants import AMQP_URI_CONFIG_KEY
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.standalone.events import event_dispatcher

from .commands import Shell


class ShellRunner(object):

    def __init__(self, banner, local):
        self.banner = banner
        self.local = local

    def bpython(self):
        import bpython  # pylint: disable=E0401
        bpython.embed(banner=self.banner, locals_=self.local)

    def ipython(self):
        from IPython import embed  # pylint: disable=E0401
        embed(banner1=self.banner, user_ns=self.local)

    def plain(self):
        code.interact(banner=self.banner, local=self.local)

    def start_shell(self, name):
        available_shells = [name] if name else Shell.SHELLS

        # Support the regular Python interpreter startup script if someone
        # is using it.
        startup = os.environ.get('PYTHONSTARTUP')
        if startup and os.path.isfile(startup):
            with open(startup, 'r') as f:
                eval(compile(f.read(), startup, 'exec'), self.local)
            del os.environ['PYTHONSTARTUP']

        for name in available_shells:
            try:
                return getattr(self, name)()
            except ImportError:
                pass
        self.plain()


def make_nameko_helper(config):
    """Create a fake module that provides some convenient access to nameko
    standalone functionality for interactive shell usage.
    """
    module = ModuleType('nameko')
    module.__doc__ = """Nameko shell helper for making rpc calls and dispatching
events.

Usage:
    >>> n.rpc.service.method()
    "reply"

    >>> n.dispatch_event('service', 'event_type', 'event_data')
"""
    proxy = ClusterRpcProxy(config)
    module.rpc = proxy.start()
    module.dispatch_event = event_dispatcher(config)
    module.config = config
    module.disconnect = proxy.stop
    return module


def main(args):
    banner = 'Nameko Python %s shell on %s\nBroker: %s' % (
        sys.version,
        sys.platform,
        args.broker.encode('utf-8'),
    )

    if args.config:
        with open(args.config) as fle:
            config = yaml.load(fle)
    else:
        config = {AMQP_URI_CONFIG_KEY: args.broker}

    ctx = {}
    ctx['n'] = make_nameko_helper(config)

    runner = ShellRunner(banner, ctx)
    runner.start_shell(name=args.interface)
