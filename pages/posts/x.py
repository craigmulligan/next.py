# coding: mixt
from components import Hello
from time import sleep

def handler(request):
    sleep(1)
    return (<Hello name="posts - x"/>)
