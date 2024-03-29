import time, asyncio
from tornado import ioloop
from tbot import config, logger

SHUTDOWN_WAIT = 5 # seconds
def sig_handler(server, application, sig, frame):
    io_loop = ioloop.IOLoop.instance()
    if hasattr(application, 'shutting_down') and application.shutting_down == True:
        io_loop.stop()
        return

    application.shutting_down = True

    def stop_loop(server, deadline: float):
        now = time.time()
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
        if (now < deadline and len(tasks) > 0) and not config.data.debug:
            logger.debug(f'Awaiting {len(tasks)} pending tasks {tasks}')
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
            return

        pending_connection = len(server._connections)
        if (now < deadline and pending_connection > 0) and not config.data.debug:
            logger.debug(f'Waiting on {pending_connection} connections to finish {server._connections}')
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
        else:
            logger.debug(f'Shutting down. {pending_connection} connections left')
            try:
                application.db.close()
                application.redis.close()
                asyncio.run(application.db.wait_closed())
                asyncio.run(application.redis.wait_closed())
            except:
                pass
            io_loop.stop()

    def shutdown():
        logger.debug(f'Waiting for up to {SHUTDOWN_WAIT} seconds to shutdown ...')
        try:
            stop_loop(server, time.time() + SHUTDOWN_WAIT)
        except BaseException as e:
            logger.error(f'Error trying to shutdown Tornado: {str(e)}')

    io_loop.add_callback_from_signal(shutdown)