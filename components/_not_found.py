# coding: mixt
from mixt import html

def NotFound(request, exc):
    return (
        <div style="background:red;">
            Not Found!!!
        </div>
    )
