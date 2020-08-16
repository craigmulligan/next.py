# coding: mixt
from components import Hello
from mixt import html 

def handler(**kwargs):
    return (
        <div>
            <Hello name="World"/>
            <div>
            <a href="/posts/x">x post</a>
            </div>
            <div>
            <a href="/about">about</a>
            </div>
            <div>
            <a href="/xyz">404</a>
            </div>
        </div>
    )
