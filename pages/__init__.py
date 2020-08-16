# coding: mixt
from components import Hello
from mixt import html 

def handler(request, **kwargs):
    return (
        <div>
            <Hello name="World"/>
            <div>
            <a href="/posts/x">x post</a>
            </div>
            <div>
            <a href="/about">about</a>
            </div>
        </div>
    )
