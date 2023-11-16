from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import mysql.connector
import httpx

app = FastAPI()

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")

db_config = {
    "host": "mysql_container",
    "user": "root",
    "password": "1234",
    "database": "users",
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Página de inicio
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Página de inicio de sesión
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Verificar las credenciales del usuario en la base de datos
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    user = cursor.fetchone()

    if user:
        # Credenciales válidas, redirigir a www.google.com
        url = "http://fastapi_api_container:8001/nasa_apod"
    
        client = httpx.AsyncClient()
        apod_data = await client.get(url)
        import pdb; pdb.set_trace()
        return templates.TemplateResponse("apod_data.html", {"request": request, "apod_data": apod_data.json()})
    else:
        # Credenciales no válidas, regresar a la página de login
        return templates.TemplateResponse("login.html", {"request": request, "message": "Credenciales incorrectas"})

# Página de registro
@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    # Insertar el usuario en la base de datos
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (username, password)
    cursor.execute(query, values)
    connection.commit()
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

# Redireccionar desde la página de inicio a las páginas de login y registro
@app.get("/redirect-to-login")
async def redirect_to_login():
    return RedirectResponse("/login")


@app.get("/redirect-to-register")
async def redirect_to_register():
    return RedirectResponse("/register")

@app.get("/redirect-to-index")
async def redirect_to_index():
    return RedirectResponse("/")

