import requests

BASE_URL = "http://127.0.0.1:8000"

def librion_api(method: str,route: str, *,params=None,json=None,token=None, data=None,timeout=10):
    url = BASE_URL + route

    # Salvva o token
    headers = {}
    
    if token:
        headers["Authorization"] =  f"Bearer {token}"

    # Monta o objeto
    kwargs = {
        "params": params,
        "json": json,
        "data": data,
        "headers": headers,
        "timeout": timeout
    }

    # remove os None
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    try:
        response = requests.request(method, url, **kwargs)

        # Sucesso
        if 200 <= response.status_code < 300:
            return {
                "success": True,
                "data": response.json(),
                "status": response.status_code
            }
        # Erro na API
        return {
            "success": False,
            "error": response.json(),
            "status": response.status_code
        }

    # Erro de conexão
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "status": None
        }