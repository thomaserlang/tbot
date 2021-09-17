import logging, functools, good
import http.client
from tornado import web, escape
from tbot.web.handlers.base import Base_handler
from tbot import utils

class Api_handler(Base_handler):

    def initialize(self):
        self.access_token = None
        if self.request.body:
            try:
                self.request.original_body = self.request.body
                self.request.body = utils.json_loads(self.request.body)
            except ValueError:
                self.request.body = {}
        else:
            self.request.body = {}

    def write_object(self, obj):
        self.write(
            utils.json_dumps(obj, indent=4, sort_keys=True),
        )

    def set_default_headers(self):
        self.set_header('Cache-Control', 'no-cache, must-revalidate')
        self.set_header('Expires', 'Sat, 26 Jul 1997 05:00:00 GMT')
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, X-Requested-With')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE')
        self.set_header('Access-Control-Expose-Headers', 'ETag, Link, X-Total-Count, X-Total-Pages, X-Page')
        self.set_header('Access-Control-Max-Age', '86400')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            if isinstance(kwargs['exc_info'][1], Api_exception):
                self.write_object({
                    'message': kwargs['exc_info'][1].message,
                    'errors': kwargs['exc_info'][1].errors,
                    'extra': kwargs['exc_info'][1].extra,
                })
                return
        msg = ''
        if 'exc_info' in kwargs and \
            isinstance(kwargs['exc_info'][1], web.HTTPError) and \
            kwargs['exc_info'][1].log_message:
            msg = kwargs['exc_info'][1].log_message
        else:
            msg = http.client.responses[status_code]
        self.write_object({
            'message': msg,
            'errors': None,
            'extra': None,
        })

    def _validate(self, data, schema, **kwargs):
        return validate_schema(schema, data, **kwargs)

    def validate(self, schema=None, **kwargs):
        if schema == None:
            schema = getattr(self, '__schema__', None)
            if schema == None:
                raise Exception('missing validation schema')
        return self._validate(
            self.request.body,
            schema,
            **kwargs
        )

    def validate_arguments(self, schema=None, **kwargs):
        if schema == None:
            schema = getattr(self, '__arguments_schema__', None)
            if schema == None:
                raise Exception('missing validation schema')
        return self._validate(
            escape.recursive_unicode(self.request.arguments),
            schema,
            **kwargs
        )

def Level(level):
    def decorator(method):
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            if not self.current_user:
                raise web.HTTPError(401, 'Not signed in!')
            if len(args) > 0:
                if args[0] != str(self.current_user['user_id']):
                    r = await self.db.fetchone(
                        'SELECT level FROM twitch_channel_admins WHERE channel_id=%s AND user_id=%s',
                        (args[0], self.current_user['user_id'])
                    )
                    if not r or r['level'] < level:
                        raise web.HTTPError(403, 'You do not have access to manage this channel')
            return await method(self, *args, **kwargs)
        return wrapper
    return decorator

class Api_exception(web.HTTPError):
    
    def __init__(self, status_code, message, errors=None, extra=None):
        super().__init__(status_code, message)
        self.status_code = status_code
        self.errors = errors
        self.message = message
        self.extra = extra

class Validation_exception(Api_exception):

    def __init__(self, errors):
        super().__init__(
            status_code=400,
            message='One or more fields failed validation',
            errors=errors,
        )

def validate_schema(schema, data, **kwargs):
    """Validates `schema` against `data`. Returns
    the data modified by the validator.

    ``schema`` can be a dict or an instance of `good.Schema`.
    If it's a dict a `good.Schema` instance will be created from it.

    Raises `Validation_exception`

    """
    try:
        if not isinstance(schema, good.Schema):        
            schema = good.Schema(schema, **kwargs)
        return schema(data)    
    except good.MultipleInvalid as ee:
        data = []
        for e in ee:
            data.append({
                'field': u'.'.join(str(x) for x in e.path),
                'message': e.message,
            })
        raise Validation_exception(errors=data)
    except good.Invalid as e:
        data = [{
            'field': u'.'.join(str(x) for x in e.path),
            'message': e.message,
        }]            
        raise Validation_exception(errors=data)