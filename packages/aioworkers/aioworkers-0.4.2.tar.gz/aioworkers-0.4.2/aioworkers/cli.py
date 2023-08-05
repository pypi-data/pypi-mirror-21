import argparse
import asyncio
import logging.config
import multiprocessing
import os
import signal
import time

from . import config
from .core.context import Context


parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('-p', '--port', type=int)
parser.add_argument('-i', '--interact', action='store_true')
parser.add_argument('-l', '--logging', help='Root logger level')


try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main(*config_files, args=None, config_dirs=()):
    if args is None:
        args = parser.parse_args()
        if getattr(args, 'config', None):
            config_files += tuple(args.config)
        if args.logging:
            logging.getLogger().setLevel(args.logging.upper())
    conf = config.load_conf(*config_files, search_dirs=config_dirs)

    if 'logging' in conf:
        logging.config.dictConfig(conf.logging)

    if args.host:
        conf['http.host'] = args.host
    if args.port is not None:
        conf['http.port'] = args.port

    if not conf.get('app.cls'):
        if conf.get('http.port'):
            conf['app.cls'] = 'aioworkers.http.Application'
        else:
            conf['app.cls'] = 'aioworkers.app.Application'

    loop = asyncio.get_event_loop()
    context = Context(conf, loop=loop)

    loop.run_until_complete(context.init())

    if args.interact:
        from .core.interact import shell
        shell(context)

    if isinstance(conf.http.port, str):
        conf.http.port = int(conf.http.port)

    try:
        context.app.run_forever(host=conf.http.host, port=conf.http.port)
    finally:
        sig = signal.SIGTERM
        while multiprocessing.active_children():
            for p in multiprocessing.active_children():
                os.kill(p.pid, sig)
            time.sleep(0.3)
            print('killall children')
            sig = signal.SIGKILL


def main_with_conf():
    parser.add_argument(
        '-c', '--config', nargs='+',
        type=argparse.FileType('r', encoding='utf-8'))
    main()


if __name__ == '__main__':
    main_with_conf()
