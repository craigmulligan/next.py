# coding: mixt
from pathlib import Path
import importlib
import glob
import os
import logging
from inspect import iscoroutinefunction

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route

from components import Hello, Layout, Document


class NotPageException(Exception):
    pass


def response_decorator(fn,fetcher, layout, document):
    async def inner(req):
        props = {}

        if callable(fetcher):
            if iscoroutinefunction(fetcher):
                data = await fetcher(req)
            else:
                data = fetcher(req)
            props = data.get("props")

        res = document(layout(fn(**props))).to_string()
        return HTMLResponse(res)

    return inner


class Builder():
    def __init__(self):
        self.routes = []
        self.cwd = os.getcwd()
        self.pages_dir = self.cwd + "/pages"

    def fmt_url(self, root, f):
        """
            Creates a url relative to pages_dir
            /home/myapp/pages/x/y.py --> /x/y
        """
        if f == "__init__.py":
            url = Path(f"{root}").relative_to(self.pages_dir)
            # special case page_dir.__str__ == "." we want "/"
            if len(url.parents) == 0:
                return "/"
            return f"/{url}"


        if f.startswith("_"):
            # ingore _layout + _document 
            raise NotPageException
        
        url = Path(f"{root}/{f}").relative_to(self.pages_dir).with_suffix("")
        return f"/{url}" 

    def load_module(self, root, f):
        import_path = Path(f"{root}/{f}").relative_to(self.cwd).with_suffix("")
        return importlib.import_module(".".join(import_path.parts))

    def get_routes(self):
        layout = Layout
        document = Document

        for root, dirs, files in os.walk(self.pages_dir):
            for f in files:
                # First get & set layout/doc
                if f == "_layout.py":
                    layout = self.load_module(root, f).default
                    continue
                if f == "_document.py":
                    document = self.load_module(root, f).default
                    continue

            # handle pages + apis
            for f in files:
                if f.endswith("py"):
                    # handle apis
                    if "api" in Path(root).parts:
                        url = self.fmt_url(root, f)
                        api_module = self.load_module(root, f)
                        self.routes.append(Route(url, api_module.default))
                        continue

                    # handle pages
                    try:
                        url = self.fmt_url(root, f)
                        page_module = self.load_module(root, f)
                        data_fn = None

                        for attr in ("get_server_props", "get_static_props"):
                            # should only have one
                            if hasattr(page_module, attr):
                                data_fn = getattr(page_module, attr)

                        self.routes.append(Route(url, response_decorator(page_module.handler, data_fn, layout, document)))

                    except NotPageException:
                        pass

        return self.routes

builder = Builder()
routes = builder.get_routes()
app = Starlette(debug=True, routes=routes)
