# coding: mixt
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from components import Hello
from pathlib import Path
import importlib
import glob
import os

def response_decorator(fn):
    def inner(req):
        # TODO check if is HTML 
        res = fn(req).to_string()
        return HTMLResponse(res)

    return inner


def build_routes(page_dir):
    pages = glob.glob(f"{page_dir}/*.py")
    routes = []

    for page in pages:
        print(page)
        page_path = Path(page)
        if page_path.stem == "__init__":
            r = "/"
        else:
            r = f"/{page_path.stem}"

        page_module = importlib.import_module("pages")
        routes.append(Route(r, response_decorator(page_module.handler)))

    return routes


page_dir = os.getcwd() + "/pages"
app = Starlette(debug=True, routes=build_routes(page_dir))
