def handler(request):
    return ("{\"status\": \"ok\", \"msg\": \"hello from SignApp test function\"}", {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    })
