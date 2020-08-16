# coding: mixt
from mixt import html

def Error(request, exc):
    return (
        <div style="background:red;">
            {error} 
        </div>
    )
