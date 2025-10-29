# ARPA-ds-2

    ``` < Raw Names >
    0    RADAR-Detect
    1    RADAR-Targeted
    2    AIS-Detect
    3    AIS-Targeted
    4    Association
    5    Red
    6    Other-Red
    ```

## ARPA-RULE

    ## RULE-1
        標註三類，正樣本三類

        ### RULE-1A
            訓練標註正樣本三類
            ``` < Rule-1A Names >
            0    RADAR-Detect
            1    RADAR-Targeted
            2(4)    Association
            ```
        ### RULE-1B
            訓練標註正樣本合併一類
            ``` < Rule-1A Names >
            0 (0,1,4)   RADAR-Detect

            ```
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

## ARPA-ds-2.1

`追加資料`製作 @ W11-NB

### label format converter @ Anaconda PowerShell

    C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
    d:/dataset_utils/label_format_converter.py xml txt `
    C:\Users\Rontgen-W11-NB\AppData\Roaming\PotPlayerMini64\Capture `
    d:\labelImg-windows_v1.8.1\data\predefined_classes.txt `

### data augmentation

    cd C:\Users\Rontgen-W11-NB\AppData\Roaming\PotPlayerMini64\Capture

    C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
    d:/dataset_utils/data_augmentation.py `
    d:\yolov7\data\ARPA_hyp2.yaml `
    C:\Users\Rontgen-W11-NB\AppData\Roaming\PotPlayerMini64\Capture --new-image 3 --no-background 

### 複製 `追加資料` 至 RAW

### 製作 RULE-1A

    1. 複製 RAW 至 RULE-1A
    2. 重製為 RULE-1A

        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/myTool/yolo_label_editor.py `
        -f D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\image-arpa-rule-1A `
        -c 2 
        -c 3
        -c 5 
        -c 6
        -c 4 -t 2

    3. 移除 孤兒標註 -> 空白標註 -> 無標註影像
            C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe d:/dataset_utils/myTool/yolo_stats.py -r D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\image-arpa-rule-1A

### 製作 RULE-1B

    4. 重製為 RULE-1A

        C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe `
        d:/dataset_utils/myTool/yolo_label_editor.py `
        -f D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\image-arpa-rule-1B `
        -c 1 -t 0
        -c 4 -t 0
        -c 2 
        -c 3
        -c 5 
        -c 6
    5. 移除 孤兒標註 / 空白標註
            C:/Users/Rontgen-W11-NB/.conda/envs/augment-venv/python.exe d:/dataset_utils/myTool/yolo_stats.py -r D:\wan-hai\wan-hai-radar-label\ARPA-ds-2\image-arpa-rule-1B

### 製作 RED


    
