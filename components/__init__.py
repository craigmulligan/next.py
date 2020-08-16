# coding: mixt
from mixt import html
from ._layout import Layout
from ._document import Document 

def Hello(name):
    return (
        <div>
            <div>Hello, {name}</div>
        </div>
    )
