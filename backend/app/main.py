"""齿轮系转速求解台 —— FastAPI 入口。

API 路由优先于静态文件挂载：
  POST /api/solve               提交轴/传动关系/已知转速，返回精确求解结果
  POST /api/gear-options        目标转速配齿：枚举一个齿数字段 1~500，逐一精确求解
  POST /api/torque-balance      理想传动转矩平衡：已知外加转矩 + 待求轴，精确求解
  POST /api/transmission-paths  传动链路追踪：最短链路总数、字典序最小链路与必经关系
  其余路径                      提供前端静态页面
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .solver import (
    GearOptionsRequest,
    SolveRequest,
    TorqueBalanceRequest,
    TransmissionPathsRequest,
    gear_options,
    solve,
    torque_balance,
    transmission_paths,
)

app = FastAPI(title="齿轮系转速求解台", version="1.3.0")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.post("/api/solve")
def api_solve(req: SolveRequest) -> dict:
    return solve(req)


@app.post("/api/gear-options")
def api_gear_options(req: GearOptionsRequest) -> dict:
    return gear_options(req)


@app.post("/api/torque-balance")
def api_torque_balance(req: TorqueBalanceRequest) -> dict:
    return torque_balance(req)


@app.post("/api/transmission-paths")
def api_transmission_paths(req: TransmissionPathsRequest) -> dict:
    return transmission_paths(req)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
