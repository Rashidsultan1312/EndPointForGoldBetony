from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

import config as cfg

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
POLICY_DIR = BASE_DIR / "PrivacyPolicy"


def is_webview_enabled() -> bool:
    return cfg.webview_power_state.strip().lower() == "on"


@app.get("/")
def root():
    return HTMLResponse(
        content="<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>",
        status_code=404
    )


@app.get("/api/webview-target")
async def get_webview_target() -> JSONResponse:
    if not is_webview_enabled():
        return JSONResponse(content={
            "enabled": False,
            "status": "webview_disabled",
        })

    return JSONResponse(content={
        "enabled": True,
        "status": "webview_enabled",
        "target_url": cfg.offer_url,
    })


# Статика для css/js/images из папки PrivacyPolicy
app.mount("/policy-static", StaticFiles(directory=POLICY_DIR), name="policy-static")


@app.get("/policy")
def policy_page():
    return FileResponse(POLICY_DIR / "index.html")
