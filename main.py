from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = FastAPI()

# HTMLテンプレートの設定
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # index.htmlを表示
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analyze")
async def analyze():
    # 1. サンプルデータの生成（X-Yプロット）
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # 2. グラフの作成
    plt.figure(figsize=(5, 4))
    plt.plot(x, y, label="sin(x)")
    plt.title("Analysis Result")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.legend()

    # 3. グラフをメモリ上のバッファに保存
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    # 4. 画像をBase64文字列に変換してフロントエンドに送る
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return {"image": f"data:image/png;base64,{img_str}"}
