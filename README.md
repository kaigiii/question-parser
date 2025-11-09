# Question Parser

一個用於解析 HTML 題庫並轉換為 CSV 格式的工具，同時提供滑鼠和鍵盤操作記錄功能。

## 功能特性

### 核心功能
- **HTML 題庫解析** (`parse_questions.py`)
  - 自動解析 HTML 表格中的題目、選項和答案
  - 支援多種答案標記格式（紅色標記、答案欄位）
  - 自動提取題目、四個選項和正確答案
  - 輸出為 CSV 格式（使用 `|` 分隔符）
  - 自動檔案編號功能，避免覆蓋現有檔案

### 輔助功能
- **操作記錄** (`record_mouse_keyboard.py`)
  - 記錄滑鼠點擊位置
  - 記錄鍵盤按鍵操作
  - 自動保存為 JSON 格式

## 安裝說明

### 系統需求
- Python 3.6 或更高版本

### 安裝依賴

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install beautifulsoup4 lxml pynput
```

## 使用方法

### 解析題庫 HTML

基本用法：

```bash
python3 parse_questions.py -i questions.html -o output.csv
```

使用預設設定（自動編號）：

```bash
python3 parse_questions.py
```

這會自動：
- 讀取 `questions.html`
- 輸出到 `parsed_questions_csv/` 資料夾
- 自動生成檔案名稱（例如：`1_1.csv`, `1_2.csv`）

#### 參數說明

- `-i, --input`: 輸入 HTML 檔案路徑（預設：`questions.html`）
- `-o, --output`: 輸出 CSV 檔案路徑（預設：自動編號）

#### 輸出格式

CSV 檔案包含以下欄位（使用 `|` 分隔）：

```
題目|選項1|選項2|選項3|選項4|答案
```

### 記錄滑鼠和鍵盤操作

```bash
python3 record_mouse_keyboard.py
```

使用說明：
1. 執行後開始記錄所有滑鼠點擊和鍵盤按鍵
2. 按 `ESC` 鍵停止記錄
3. 記錄會自動保存到 `actions.json`

## 專案結構

```
.
├── parse_questions.py          # 核心功能：HTML 題庫解析器
├── record_mouse_keyboard.py    # 輔助功能：操作記錄工具
├── requirements.txt            # Python 依賴套件
├── questions.html              # 範例輸入檔案
├── actions.json                # 操作記錄輸出檔案
└── parsed_questions_csv/       # 解析結果輸出資料夾
    ├── 1_1.csv
    ├── 1_2.csv
    └── ...
```

## 依賴套件

- **beautifulsoup4** (>=4.12.0): HTML 解析
- **lxml** (>=4.9.0): BeautifulSoup 的解析器
- **pynput** (>=1.7.6): 滑鼠和鍵盤監聽

## 答案識別規則

解析器會依以下順序識別正確答案：

1. **優先**：HTML 中的紅色標記（`<span style="color:red;">正確答案為:X</span>`）
2. **備選**：答案欄位（第二個 `<td>`）中的數字（1-4）

## 注意事項

- 確保 HTML 檔案使用 UTF-8 編碼
- 題目格式應為表格（`<table>`）結構
- 每個題目應包含題號、答案欄和題目內容欄位
- 選項格式支援 `(1)`, `(2)`, `(3)`, `(4)` 標記或換行分隔

## 授權

本專案為開源專案，可自由使用和修改。

