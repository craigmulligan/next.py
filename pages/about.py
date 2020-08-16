# coding: mixt
from components import Hello

def get_server_props(req):
    return {
        "props": {
                "name": "hobochild",
                "info": "A little about me"
        }         
    }

def handler(name, info):
    return (<Hello name={name} />)
