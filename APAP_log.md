# ARPA Log

## ARPA EXP 1

    # prepare
        d:/dataset_utils/myTool/create_blank_xml.py
        d:/dataset_utils/label_format_converter.py xml txt D:\wan-hai\wan-hai-radar-label\RADAR-research d:\labelImg-windows_v1.8.1\data\predefined_classes.txt
        cd D:\wan-hai\wan-hai-radar-label\RADAR-research
        d:/dataset_utils/data_augmentation.py d:\dataset_utils\hyp.yaml D:\wan-hai\wan-hai-radar-label\RADAR-research --new-image 4 --no-background 
        d:/dataset_utils/myTool/generate_train_val_test_txt.py


    # train
        conda activate yolov7
        E:
        cd D:\yolov7\

        python train.py `
        --weights yolov7.pt `
        --device 0 `
        --batch-size 4 `
        --epochs 200 `
        --data data/ARPA_exp1.yaml `
        --name ARPA_yolov7 `
        --hyp data/hyp.scratch.p5.yaml `
        --img-size 640 `
        --adam

    # detect
        python detect.py  `
        --weights runs/train/ARPA_yolov7/weights/best.pt  `
        --img 640 --conf 0.3  `
        --source D:\wan-hai\wan-hai-radar-label\RADAR-research\temp

    # ONNX
        python export.py `
        --weights runs/train/ARPA_yolov7/weights/best.pt `
        --img-size 640 640 `
        --batch-size 1 `
        --device 0 `
        --dynamic `
        --simplify `
        --end2end `
        --grid `
        --max-wh 640 `
        --topk-all 100 --iou-thres 0.65 --conf-thres 0.3

    # ONNX detect    
        python tools/onnx_detect_video.py `
            --input d:\wan-hai\Test_Videos\Type-A\A_BLACK_good_2022_07_13_14_25_14_93.mp4 `
            --output d:\wan-hai\Test_Videos\Type-A\demo_detect.mp4 `
            --weights runs/train/ARPA_yolov7/weights/best.onnx `
            --data data.yaml `
            --img-size 640 `
            --device gpu


## ARPA EXP 2
    基於 exp1 的資料集，但是額外增加第六類 `red` 的標註
    
    # label format converter @ Anaconda PowerShell
        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/label_format_converter.py xml txt `
        D:\wan-hai\wan-hai-radar-label\RADAR-research\label-images `
        d:\labelImg-windows_v1.8.1\data\predefined_classes.txt `
    
    # data augmentation
        cd D:\wan-hai\wan-hai-radar-label\RADAR-research\label-images

        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/data_augmentation.py `
        d:\dataset_utils\hyp.yaml `
        D:\wan-hai\wan-hai-radar-label\RADAR-research\label-images --new-image 4 --no-background 

    # generate train val test txt
        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        D:\dataset_utils\myTool\generate_train_val_test_txt.py `
        D:\wan-hai\wan-hai-radar-label\RADAR-research\label-images `
        --ratio 8:1:1 `
        --no-reorganize

    # train
        conda activate yolov7

        cd D:\yolov7\

        python train.py `
        --weights yolov7.pt `
        --device 0 `
        --batch-size 4 `
        --epochs 200 `
        --data data/ARPA_exp2.yaml `
        --name ARPA_yolov7_exp2 `
        --hyp data/hyp.scratch.p5.yaml `
        --img-size 640 `
        --adam

    # detect
        python detect.py  `
        --weights runs/train/ARPA_yolov7_exp2/weights/best.pt  `
        --img 640 --conf 0.3  `
        --source D:\wan-hai\wan-hai-radar-label\RADAR-research\ORG_images


# ARPA RULE
    ## RULE-1
        標註三類，正樣本三類
        - RADAR-Detect
        - RADAR-Targeted
        - Association
        ### RULE-1A
            訓練標註正樣本三類
        ### RULE-1B
            訓練標註正樣本合併一類
    ## RULE-2
        標註五類，正樣本三類、負樣本二類
        - RADAR-Detect
        - RADAR-Targeted
        - AIS-Detect
        - AIS-Targeted
        - Association
        ### RULE-2A        
                訓練標註 正樣本三類、負樣本二類
        ### RULE-2B
            正樣本三類、負樣本二類
            訓練標註 正樣本合併一類、負樣本合併一類

# ARPA-ds-2
    
    原始資料製作
    
    # label format converter @ Anaconda PowerShell
        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/label_format_converter.py xml txt `
        D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\image `
        d:\labelImg-windows_v1.8.1\data\predefined_classes.txt `

    # data augmentation  
        cd D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\raw-label

        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/data_augmentation.py `
        d:\yolov7\data\ARPA_hyp2.yaml `
        D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\raw-label --new-image 3 --no-background 

## 使用已建置的docker 環境來進行訓練
https://hub.docker.com/layers/pytorch/pytorch/2.8.0-cuda12.8-cudnn9-devel/images/sha256-a7103283ea7113e10ae5d014bd2342acebda0bc53164b2f7b1dd6eb7a766bdb6

### 建立 torch:2.8.0-cuda12.8 的 docker 容器
    # 移動到工作目錄
    cd ~/Documents/Rontgen/

    # 建立docker容器
    docker run --gpus all \
    -d -it \
    --name rontgen-cu128 \
    -v "$(pwd)":/workspace \
    -w /workspace \
    -p 6007:6006 \
    pytorch/pytorch:2.8.0-cuda12.8-cudnn9-devel \
    bash

    # OpenCV 依賴的系統動態庫缺失：libGL.so.1
    apt-get update
    apt-get install -y libgl1 libglib2.0-0
    # 若仍報其它 X 相關錯誤再補：
    apt-get install -y libsm6 libxext6 libxrender1

    # 附加 shell
    docker exec -it rontgen-cu128 bash
    # 暫停容器
    docker stop rontgen-cu128
    # 重新啟動
    docker start rontgen-cu128


## ARPA EXP 3 @ rtx5090
  基於 ARPA-ds-2 資料集，使用 RULE-1A 標註規則

    # make RULE-1A label
        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/myTool/yolo_label_editor.py `
        -f D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\rule-1A `
        -c 2
        -c 3
        -c 5 
        -c 4 -t 2
    # CP
    cp -afv rule-1A/. image/

    # generate train val test txt @ docker
        docker exec -it ttgui bash

        python \
        /workspace/dataset_utils/myTool/generate_train_val_test_txt.py \
        /workspace/dataset/ARPA-ds-2/image \
        --ratio 8:1:1 \
        --no-reorganize

    # edit data yaml
        D:\yolov7\data\ARPA_exp3.yaml

    # train
        **先刪除位於影像標註資料夾內的 .cache 檔案，torch 2.6 導致 cache 導入失效**
        conda activate rontgen
        cd ~/Documents/Rontgen/yolov7

        nohup python train.py --weights ./yolov7.pt  \
        --device 0 --batch-size 32  \
        --epochs 600  \
        --data data/ARPA_exp3.yaml  \
        --name ARPA_yolov7_exp3  \
        --hyp data/hyp.scratch.p5_2.yaml  \
        --img-size 640 --adam  \
        --exist-ok &> train.txt & \

    # ONNX
        python export.py \
        --weights runs/train/ARPA_yolov7_exp3/weights/best.pt \
        --img-size 640 640 \
        --batch-size 1 \
        --device 0 \
        --dynamic \
        --simplify \
        --end2end \
        --grid \
        --max-wh 640 \
        --topk-all 100 --iou-thres 0.65 --conf-thres 0.3

## ARPA EXP 3.b4 @ rtx5090
  基於 ARPA-ds-2 資料集，使用 RULE-1A 標註規則
  基於 ARPA EXP 3，batch size 32 > 4 的訓練結果
    # CP
    cd /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2
    cp -afv arpa-rule-1A/. image/

    # train
        **先刪除位於影像標註資料夾內的 .cache 檔案，torch 2.6 導致 cache 導入失效**
        conda activate rontgen
        cd ~/Documents/Rontgen/yolov7
        rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/*.cache

        nohup python train.py --weights ./yolov7.pt  \
        --device 0 --batch-size 4  \
        --epochs 600  \
        --data data/ARPA_exp3.yaml  \
        --name ARPA_yolov7_exp3-b4 \
        --hyp data/hyp.scratch.p5_2.yaml  \
        --img-size 640 --adam  \
        --exist-ok &> train_exp3.b4.txt & \

    # ONNX
        python export.py \
        --weights runs/train/ARPA_yolov7_exp3-b4/weights/best.pt \
        --img-size 640 640 \
        --batch-size 1 \
        --device 0 \
        --dynamic \
        --simplify \
        --end2end \
        --grid \
        --max-wh 640 \
        --topk-all 100 --iou-thres 0.65 --conf-thres 0.3

## ARPA EXP 3.b32.ds21 @ rtx5090
  基於 ARPA-ds-2 資料集，使用 RULE-1A 標註規則
  基於 ARPA EXP 3，batch size 32 > 4 的訓練結果
  修正 augmentation 中的影像資料，移除當中的空白標註

### remove empty label and image
    python '/home/rtx5090/Documents/Rontgen/dataset_utils/myTool/clean_empty_labels.py' /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1 --yes

### generate train val test txt @ docker
    conda activate rontgen

    python \
    /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/generate_train_val_test_txt.py \
    /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1 \
    --ratio 8:1:1 \
    --no-reorganize

### edit data yaml
    /home/rtx5090/Documents/Rontgen/yolov7/data/ARPA_exp3.yaml

### train
    **先刪除位於影像標註資料夾內的 .cache 檔案，torch 2.6 導致 cache 導入失效**
    conda activate rontgen
    cd ~/Documents/Rontgen/yolov7
    rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/*.cache

    nohup python train.py --weights ./yolov7.pt  \
    --device 0 --batch-size 32  \
    --epochs 600  \
    --data data/ARPA_exp3.yaml  \
    --name ARPA_yolov7_exp3-b32ds21 \
    --hyp data/hyp.scratch.p5_2.yaml  \
    --img-size 640 --adam  \
    --exist-ok &> train_exp3.b32ds21.txt & \

### tensorboard
    tensorboard --logdir runs --bind_all

### ONNX
    python export.py \
    --weights runs/train/ARPA_yolov7_exp3-b4/weights/best.pt \
    --img-size 640 640 \
    --batch-size 1 \
    --device 0 \
    --dynamic \
    --simplify \
    --end2end \
    --grid \
    --max-wh 640 \
    --topk-all 100 --iou-thres 0.65 --conf-thres 0.3

## ARPA EXP 4
基於 ARPA-ds-2 資料集，使用 RULE-1B 標註規則
### make RULE-1B label
    C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
    d:/dataset_utils/myTool/yolo_label_editor.py `
    -f D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\rule-1B `
    -c 1 -t 0
    -c 4 -t 0
    -c 2 
    -c 3
    -c 5 
    
### move labels
    cp -afv ~/Documents/Rontgen/dataset/ARPA-ds-2/arpa-rule-1B/. ~/Documents/Rontgen/dataset/ARPA-ds-2/image/
### train
    **先刪除位於影像標註資料夾內的 .cache 檔案，troch 2.6 導致 cache 導入失效**
    rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/*.cache
    conda activate rontgen
    cd ~/Documents/Rontgen/yolov7

    nohup python train.py --weights ./yolov7.pt  \
    --device 0 --batch-size 32  \
    --epochs 600  \
    --data data/ARPA_exp4.yaml  \
    --name ARPA_yolov7_exp4  \
    --hyp data/hyp.scratch.p5_2.yaml  \
    --img-size 640 --adam  \
    --exist-ok &> train.txt & \

### ONNX
    python export.py \
    --weights runs/train/ARPA_yolov7_exp4/weights/best.pt \
    --img-size 640 640 \
    --batch-size 1 \
    --device 0 \
    --dynamic \
    --simplify \
    --end2end \
    --grid \
    --max-wh 640 \
    --topk-all 100 --iou-thres 0.65 --conf-thres 0.3

## check dataset
python /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/yolo_stats.py \
 -r /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/raw-label-rule-1

python /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/yolo_stats.py \
 -r /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-2

## ARPA EXP 3.b4-rebuild @ rtx5090
基於 APRA EXP 3.b4，但重新製作訓練資料集，基於 ARPA-ds-2 資料集，使用 RULE-1A 標註規則
### remove label in image-arpa-rule-1
    rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/*.txt
    rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/augmentation/*.txt
### cp raw txt label to image-arpa-rule-1
    cp -afv ~/Documents/Rontgen/dataset/ARPA-ds-2/raw-label-rule-1/*.txt ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/
    cp -afv ~/Documents/Rontgen/dataset/ARPA-ds-2/raw-label-rule-1/augmentation/*.txt ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/augmentation/
### make rule-1A label
    ``` < Raw Names >
    0    RADAR-Detect
    1    RADAR-Targeted
    2    AIS-Detect
    3    AIS-Targeted
    4    Association
    5    Red
    6    Other-Red
    ```
    ``` < Rule-1A Names >
    0    RADAR-Detect
    1    RADAR-Targeted
    2(4)    Association

    ```
    python /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/yolo_label_editor.py \
    -f /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1 \
    -c 2 
    -c 3 
    -c 5 
    -c 6
    -c 4 -t 2
### remove empty label
    python '/home/rtx5090/Documents/Rontgen/dataset_utils/myTool/clean_empty_labels.py' /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1 --yes
### check dataset status 
    python /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/yolo_stats.py \
    -r /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1
### backup labels
    cp -afv ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/*.txt ~/Documents/Rontgen/dataset/ARPA-ds-2/arpa-rule-1A/
    cp -afv ~/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1/augmentation/*.txt ~/Documents/Rontgen/dataset/ARPA-ds-2/arpa-rule-1A/augmentation/
### generate train val test txt
    python \
    /home/rtx5090/Documents/Rontgen/dataset_utils/myTool/generate_train_val_test_txt.py \
    /home/rtx5090/Documents/Rontgen/dataset/ARPA-ds-2/image-arpa-rule-1 \
    --ratio 8:1:1 \
    --no-reorganize

### train
    **先刪除位於影像標註資料夾內的 .cache 檔案，torch 2.6 導致 cache 導入失效**
    conda activate rontgen
    cd ~/Documents/Rontgen/yolov7
    rm -f ~/Documents/Rontgen/dataset/ARPA-ds-2/*.cache

    nohup python train.py --weights ./yolov7.pt  \
    --device 0 --batch-size 4  \
    --epochs 600  \
    --data data/ARPA_exp3.yaml  \
    --name ARPA_yolov7_exp3-b4r \
    --hyp data/hyp.scratch.p5_2.yaml  \
    --img-size 640 --adam  \
    --exist-ok &> logs\train_exp3.b4.r.txt & \
### ONNX
    python export.py \
    --weights runs/train/ARPA_yolov7_exp3-b4r/weights/best.pt \
    --img-size 640 640 \
    --batch-size 1 \
    --device 0 \
    --dynamic \
    --simplify \
    --end2end \
    --grid \
    --max-wh 640 \
    --topk-all 100 --iou-thres 0.65 --conf-thres 0.3