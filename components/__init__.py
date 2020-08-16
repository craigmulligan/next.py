# coding: mixt
from mixt import html
from ._layout import Layout
from ._document import Document 
from ._error import Error
from ._not_found import NotFound

def Hello(name):
    return (
        <div>
            <div>Hello, {name}</div>
        </div>
    )
