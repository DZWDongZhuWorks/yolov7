#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detect_video.py
===============
以 YOLOv7 ONNX 模型偵測影片，輸出標註後影片並顯示每格推理耗時。

使用方法（範例）：
python detect_video.py \
    --input demo.mp4 \
    --output demo_detect.mp4 \
    --weights best.onnx \
    --data data.yaml \
    --img-size 640 \
    --device gpu       # 或 cpu
"""

import argparse, time, random, yaml, sys
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
from tqdm import tqdm

# ---------- 影像前處理 ---------- #
def letterbox(im, new_shape=(640, 640), color=(114, 114, 114),
              auto=False, scaleup=True, stride=32):
    """保持長寬比縮放並補邊到指定大小（取自官方範例）"""
    shape = im.shape[:2]                       # h, w
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0],           # 縮放倍率
            new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)

    # 計算補邊
    new_unpad = (int(round(shape[1] * r)),
                 int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], \
             new_shape[0] - new_unpad[1]
    if auto:                                   # 取 stride 的整數倍
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)
    dw, dh = dw / 2, dh / 2

    # 調整尺寸並補邊
    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad,
                        interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right,
                            cv2.BORDER_CONSTANT, value=color)
    return im, r, (dw, dh)

# ---------- 後處理 / 繪圖 ---------- #
def draw_detections(img, dets, names, ratio, dwdh, colors):
    """將偵測結果 (x0,y0,x1,y1,cls,conf) 繪製到 img 上"""
    for x0, y0, x1, y1, cls, conf in dets:
        box = np.array([x0, y0, x1, y1])
        box -= np.array(dwdh * 2)
        box /= ratio
        box = box.round().astype(int).tolist()
        cls, conf = int(cls), float(conf)
        label = f"{names[cls]} {conf:.2f}"
        color = colors[cls]
        cv2.rectangle(img, box[:2], box[2:], color, 2, cv2.LINE_AA)
        cv2.putText(img, label, (box[0], box[1]-2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2,
                    cv2.LINE_AA)
    return img

# ---------- 主函式 ---------- #
def main(opt):
    # 讀 class 名稱
    if opt.data and Path(opt.data).is_file():
        with open(opt.data, "r", encoding="utf-8") as f:
            names = yaml.safe_load(f)["names"]
    else:
        # 沒提供 data.yaml 則先給空白名
        names = [f"cls{i}" for i in range(100)]
    colors = {i: [random.randint(0,255) for _ in range(3)]
              for i in range(len(names))}

    # 建立 ONNX Session
    providers = (["CUDAExecutionProvider",
                  "CPUExecutionProvider"] if opt.device=="gpu"
                 else ["CPUExecutionProvider"])
    session = ort.InferenceSession(opt.weights, providers=providers)
    in_name  = session.get_inputs()[0].name
    out_name = [o.name for o in session.get_outputs()]

    # 開啟影片
    cap = cv2.VideoCapture(opt.input)
    if not cap.isOpened():
        sys.exit(f"無法開啟影片：{opt.input}")
    fps  = cap.get(cv2.CAP_PROP_FPS)
    w    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h    = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 建立輸出
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out    = cv2.VideoWriter(opt.output, fourcc, fps, (w, h))

    # 主迴圈
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                unit="frame")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 前處理
        img, ratio, dwdh = letterbox(frame, (opt.img_size, opt.img_size),
                                     auto=False)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.transpose(2,0,1)[None].astype(np.float32) / 255.0

        # 推理計時
        t0 = time.time()
        det = session.run(out_name, {in_name: img})[0]
        infer_ms = (time.time() - t0) * 1000

        # 後處理＋繪圖
        frame = draw_detections(frame, det[:,1:], names,
                                ratio, dwdh, colors)
        cv2.putText(frame, f"inference {infer_ms:6.1f} ms",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("YOLOv7", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        out.write(frame)
        pbar.update(1)

    # 收尾
    pbar.close()
    cap.release()
    out.release()
    print(f"輸出完成：{opt.output}")

# ---------- CLI ---------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="以 YOLOv7 ONNX 模型偵測影片並輸出結果")
    parser.add_argument("--input",  required=True,
                        help="輸入影片路徑")
    parser.add_argument("--output", required=True,
                        help="輸出影片路徑")
    parser.add_argument("--weights",required=True,
                        help="ONNX 權重路徑")
    parser.add_argument("--data",   default=None,
                        help="YOLO data.yaml（含 class 名稱）")
    parser.add_argument("--img-size", type=int, default=640,
                        help="推理輸入尺寸（方形邊長）")
    parser.add_argument("--device", choices=["cpu","gpu"],
                        default="cpu", help="執行設備")
    main(parser.parse_args())
