from http_router import Router
from http_router.exceptions import NotFoundError

router = Router()

@router.route('/')
def home():
    return "Roger Risson da Silva"

def application (env, start_response):    
    try:
        match = router(env['REQUEST_URI'], method=env['REQUEST_METHOD'])
        response = match.target().encode('utf-8')
        start_response('200', [('Content-Type','text/html')])
        return response
    except NotFoundError:
        start_response('404', [('Content-Type','text/html')])
        return b''
    except:
        start_response('500', [('Content-Type','text/html')])
        return b''
