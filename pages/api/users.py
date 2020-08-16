from starlette.responses import JSONResponse

def default(req):
    return JSONResponse([{
        "id": 1,
        "name":  "foo" 
        }, {
        "id": 2,
        "name":  "bar" 
    }])
