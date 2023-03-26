import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/')
def homepage(request: Request):
    """homepage routing"""
    return templates.TemplateResponse('home/index.html', {'request': request})


@router.get('/favicon.ico')
def favicon():
    """favicon"""
    return fastapi.responses.RedirectResponse(url='/static/img/favicon.ico', status_code=301)
