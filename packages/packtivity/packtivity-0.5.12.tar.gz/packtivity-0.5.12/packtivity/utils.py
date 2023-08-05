import os
import errno
import jq
import jsonpointer
import logging

def handler_decorator():
    handlers = {}
    def decorator(name, implementation = 'default'):
        def wrap(func):
            handlers.setdefault(name,{})[implementation] = func
        return wrap
    return handlers,decorator

def mkdir_p(path):
    #http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import asyncbackends
import syncbackends

def proxy_from_json(jsondata, best_effort_backend = True):
    if jsondata['proxyname'] == 'CeleryProxy':
        from asyncbackends import CeleryProxy
        proxy = CeleryProxy.fromJSON(jsondata)
        _, backend = backend_from_string('celery')
    if 'PACKTIVITY_ASYNCBACKEND' in os.environ:
        import importlib
        module, _, proxyclass = os.environ['PACKTIVITY_ASYNCBACKEND'].split(':')
        module = importlib.import_module(module)
        proxyclass = getattr(module,proxyclass)
        proxy = proxyclass.fromJSON(jsondata)
        _, backend = backend_from_string('fromenv')
    if best_effort_backend:
        return proxy, backend
    return proxy

def backend_from_string(backendstring):
    '''
    creates (a)sync backends from strings
    returns tuple (boolean,backend) where boolean
    specifies whether this is a syncbackend (True) or
    asyncbackend (False)
    '''
    is_sync, is_async = True, False
    if backendstring == 'defaultsync':
        return is_sync, syncbackends.defaultsyncbackend()
    if backendstring.startswith('multiproc'):
        _,poolsize = backendstring.split(':')
        backend = asyncbackends.MultiProcBackend(poolsize = poolsize)
        return is_async, backend
    if  backendstring == 'ipcluster':
        backend = asyncbackends.IPythonParallelBackend()
        return is_async, backend
    if backendstring == 'celery':
        backend = asyncbackends.CeleryBackend()
        return is_async, backend
    if backendstring == 'fromenv':
        import importlib
        module, backend, _ = os.environ['PACKTIVITY_ASYNCBACKEND'].split(':')
        module = importlib.import_module(module)
        backendclass = getattr(module,backend)
        return is_async, backendclass()
    raise RuntimeError('Unknown Backend')

def leaf_iterator(jsonable):
    allleafs = jq.jq('leaf_paths').transform(jsonable, multiple_output = True)
    leafpointers = [jsonpointer.JsonPointer.from_parts(x) for x in allleafs]
    for x in leafpointers:
        yield x,x.get(jsonable)

def setup_logging(nametag, context):
    ## prepare logging for the execution of the job. We're ready to handle up to DEBUG
    log  = logging.getLogger('step_logger_{}'.format(nametag))
    log.propagate = False
    log.setLevel(logging.DEBUG)


    #reset loggers .. 
    log.handlers = []
    ## this is all internal loggin, we don't want to escalate to handlers of parent loggers
    ## we will have two handlers, a stream handler logging to stdout at INFO
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    fh  = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    log.addHandler(fh)

    # Now that we have  place to store meta information we put a file based logger in place
    # to log at DEBUG
    logname = '{}/{}.step.log'.format(context['metadir'],nametag)
    fh  = logging.FileHandler(logname)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    log.addHandler(fh)

