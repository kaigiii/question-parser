# Question Parser

一個用於解析 HTML 題庫並轉換為 CSV 格式的工具，同時提供滑鼠和鍵盤操作記錄功能。

## 功能特性

### 核心功能
- **HTML 題庫解析** (`parse_questions.py`)
  - 自動解析 HTML 表格中的題目、選項和答案
  - 支援多種答案標記格式（紅色標記、答案欄位）
  - 自動提取題目、四個選項和正確答案
  - 輸出為 CSV 格式（使用標準逗號 `,` 分隔符）
  - 自動檔案編號功能，避免覆蓋現有檔案

### 輔助功能
- **操作記錄** (`record_mouse_keyboard.py`)
  - 記錄滑鼠點擊位置
  - 記錄鍵盤按鍵操作
  - 自動保存為 JSON 格式

- **自動化腳本** (`automate_actions.py`)
  - 自動執行滑鼠點擊和鍵盤操作序列
  - 支援 Mac 和 Windows 平台
  - 自動將剪貼簿內容保存為 HTML 檔案
  - 自動執行解析腳本
  - 支援循環執行，按 ESC 鍵停止

## 安裝說明

### 系統需求
- Python 3.6 或更高版本

### 安裝依賴

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install beautifulsoup4 lxml pynput pyperclip
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

CSV 檔案包含以下欄位（使用標準逗號 `,` 分隔）：

```
題目,選項1,選項2,選項3,選項4,答案
```

### 記錄滑鼠和鍵盤操作

```bash
python3 record_mouse_keyboard.py
```

使用說明：
1. 執行後開始記錄所有滑鼠點擊和鍵盤按鍵
2. 按 `ESC` 鍵停止記錄
3. 記錄會自動保存到 `actions.json`

### 自動化腳本

```bash
python3 automate_actions.py
```

使用說明：

1. **首次使用前必須調整座標位置**：
   - 打開 `automate_actions.py` 檔案
   - 找到所有標記為 `# TODO: 請填入座標 (x, y)` 的位置
   - 根據您的螢幕和應用程式視窗，填入實際的滑鼠點擊座標
   - **重要**：不同電腦、不同螢幕解析度、不同視窗大小，座標位置都會不同

2. **執行流程**：
   - 腳本會自動執行一系列滑鼠點擊和鍵盤操作
   - 自動將剪貼簿內容保存為 `questions.html`
   - 自動執行 `parse_questions.py` 解析腳本
   - 完成後等待 2 秒，自動開始下一次循環
   - 按 `ESC` 鍵可停止循環執行

3. **自訂設定**：
   - 可調整 `action_interval` 參數來改變操作間隔時間（預設 0.5 秒）
   - 可修改 `run_loop()` 方法中的等待時間（預設 2 秒）

#### 座標位置調整方法

由於不同電腦的螢幕解析度、視窗大小、應用程式佈局都可能不同，**必須根據實際情況調整座標位置**：

1. **使用記錄工具**：
   ```bash
   python3 record_mouse_keyboard.py
   ```
   執行後點擊目標位置，記錄會顯示座標，例如：`點擊: (100, 175)`

2. **手動測試**：
   - 在 `automate_actions.py` 中臨時添加 `print()` 語句
   - 使用 Python 的 `pynput` 庫獲取當前滑鼠位置

3. **注意事項**：
   - Mac 和 Windows 的座標系統相同，但視窗位置可能不同
   - 如果視窗大小改變，座標也需要重新調整
   - 建議在固定視窗大小和位置下使用

## 專案結構

```
.
├── parse_questions.py          # 核心功能：HTML 題庫解析器
├── record_mouse_keyboard.py    # 輔助功能：操作記錄工具
├── automate_actions.py         # 自動化腳本：執行滑鼠鍵盤操作序列
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
- **pyperclip** (>=1.8.2): 剪貼簿操作

## 答案識別規則

解析器會依以下順序識別正確答案：

1. **優先**：HTML 中的紅色標記（`<span style="color:red;">正確答案為:X</span>`）
2. **備選**：答案欄位（第二個 `<td>`）中的數字（1-4）

## 注意事項

### 解析器注意事項
- 確保 HTML 檔案使用 UTF-8 編碼
- 題目格式應為表格（`<table>`）結構
- 每個題目應包含題號、答案欄和題目內容欄位
- 選項格式支援 `(1)`, `(2)`, `(3)`, `(4)` 標記或換行分隔

### 自動化腳本注意事項
- **重要**：不同電腦的螢幕解析度、視窗大小、應用程式佈局都不同，**必須根據實際情況調整座標位置**
- 首次使用前，請先使用 `record_mouse_keyboard.py` 記錄實際的座標位置
- 建議在固定視窗大小和位置下使用自動化腳本
- 執行前請確保目標應用程式已開啟並準備好
- 腳本會自動循環執行，按 `ESC` 鍵可停止

## 授權

本專案為開源專案，可自由使用和修改。

