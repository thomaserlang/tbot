# type: ignore
# flake8: noqa
"""
The MIT License

Copyright (C) 2006, Riku 'Shrike' Lindblad
Copyright (C) 2007, Marko Koivusalo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Provides small event framework
"""

from typing import Any
from typing import Awaitable

_events = {}


class Event:
    """Represents one registered event."""

    def __init__(self, name, func, priority=128):
        self.name = name
        self.func = func
        self.priority = priority

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __str__(self):
        return '<Event(name=%s,func=%s,priority=%s)>' % (
            self.name,
            self.func.__name__,
            self.priority,
        )

    __repr__ = __str__


def event(name, priority=128):
    """Register event to function with a decorator"""

    def decorator(func):
        add_event_handler(name, func, priority)
        return func

    return decorator


def get_events(name):
    """
    :param String name: event name
    :return: List of :class:`Event` for *name* ordered by priority
    """
    if name not in _events:
        raise KeyError('No such event %s' % name)
    _events[name].sort(reverse=True)
    return _events[name]


def add_event_handler(name: str, func: Any, priority: int = 128) -> Event:
    """
    :param name: Event name
    :param func: Function that acts as event handler
    :param priority: Priority for this hook
    :return: Event created
    :raises ValueError: If *func* is already registered in an event
    """
    events = _events.setdefault(name, [])
    for event in events:
        if event.func == func:
            raise ValueError(
                '%s has already been registered as event listener under name %s'
                % (func.__name__, name)
            )
    event = Event(name, func, priority)
    events.append(event)
    return event


def remove_event_handlers(name):
    """Removes all handlers for given event `name`."""
    _events.pop(name, None)


def remove_event_handler(name, func):
    """Remove `func` from the handlers for event `name`."""
    for e in list(_events.get(name, [])):
        if e.func is func:
            _events[name].remove(e)


def fire_event(name: str, *args, **kwargs) -> list[Any]:
    """
    :param name: Name of event to be called
    :param args: List of arguments passed to handler function
    :param kwargs: Key Value arguments passed to handler function
    """
    if name not in _events:
        return []
    results = []
    for event in get_events(name):
        results.append(event(*args, **kwargs))
    return results


async def fire_event_async(name: str, *args: Any, **kwargs: Any) -> list[Any]:
    """
    :param name: Name of event to be called
    :param args: List of arguments passed to handler function
    :param kwargs: Key Value arguments passed to handler function
    """
    if name not in _events:
        return []
    results: list[Any] = []
    for event in get_events(name):
        results.append(await event(*args, **kwargs))
    return results
