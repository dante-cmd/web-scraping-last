from typing import List
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Create the server
app = FastAPI(debug=True)

# Add the directory where the files templates are
# HTML files
templates = Jinja2Templates(directory='templates')

# mount a route where is the static files
# CSS, JavaScript and images if exists
app.mount('/static', StaticFiles(directory='static'), name='static')

# Create a route 
@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context=context)


@app.post("/", response_class=HTMLResponse)
def get_form(request: Request,
             email: str = Form(alias='email'),
             password: str = Form(alias='password')):  

    context = {'request': request}

    if (password  == '123456') and (email == 'danteca.dtc@gmail.com'):
        return templates.TemplateResponse('success.html', context=context )
    
    return templates.TemplateResponse('index.html', context=context )