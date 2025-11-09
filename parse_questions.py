#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_questions.py

解析題庫 HTML（像使用者所貼的片段），並輸出 CSV（delimiter='|'）

輸出欄位：題目|選項1|選項2|選項3|選項4|答案

使用說明：
  python3 parse_questions.py -i questions.html -o questions_output.csv

若 HTML 中有 <span style="color:red;">正確答案為:X</span> 以此為主；
若沒有，則會從第二個 <td>（通常為答案欄）抓數字作為答案。

需要套件：beautifulsoup4, lxml
"""

from pathlib import Path
import re
import csv
import argparse
try:
    from bs4 import BeautifulSoup
    _HAVE_BS4 = True
except Exception:
    BeautifulSoup = None
    _HAVE_BS4 = False

# ========== 使用者設定 ==========
# 檔案前綴（例如：'1_'、'2_'、'3_'）
FILE_PREFIX = '1_'
# 輸出資料夾名稱
OUTPUT_DIR = 'parsed_questions_csv'
# 預設輸入 HTML 檔案名稱
DEFAULT_INPUT_FILE = 'questions.html'
# 預設輸出格式
DEFAULT_FORMAT = 'csv'
# ================================


def extract_questions_from_html(html_text):
    results = []

    if _HAVE_BS4:
        soup = BeautifulSoup(html_text, 'lxml')
        rows = soup.find_all('tr')
        for tr in rows:
            # skip header rows or rows that are not question rows
            tds = tr.find_all('td', recursive=False)
            if not tds:
                continue

            # skip rows where first td has colspan (headers)
            first_td = tds[0]
            if first_td.has_attr('colspan'):
                continue

            # skip header row if it contains column titles like '題號','答案','題目'
            first_text = tds[0].get_text(strip=True)
            second_text = tds[1].get_text(strip=True) if len(tds) > 1 else ''
            third_text = tds[2].get_text(strip=True) if len(tds) > 2 else ''
            header_keys = {'題號', '答案', '題目'}
            if any(key in (first_text, second_text, third_text) for key in header_keys):
                continue

            # we expect at least 3 tds: 題號 | 答案欄 | 題目(含選項)
            if len(tds) < 3:
                continue

            td_answer_cell = tds[1]
            td_question_cell = tds[2]

            # 先嘗試在題目cell找紅色正確答案標記
            span = td_question_cell.find('span', string=re.compile(r'正確答案為'))
            answer_index = None
            if span:
                m = re.search(r'正確答案為[:：]?\s*([1-4])', span.get_text())
                if m:
                    answer_index = int(m.group(1))

            # 若題目cell無紅色標記，則嘗試從答案欄抓數字
            if answer_index is None:
                txt = td_answer_cell.get_text(strip=True)
                m2 = re.search(r'([1-4])', txt)
                if m2:
                    answer_index = int(m2.group(1))

            # 取得題目與選項的純文字（使用換行分隔）
            q_text = td_question_cell.get_text(separator='\n', strip=True)

            # 移除可能出現的「正確答案為:X」從題目文字中
            q_text = re.sub(r'正確答案為[:：]?\s*[1-4]', '', q_text)

            # 找出所有選項標記 (1) ... (2) ... (3) ... (4)
            option_starts = list(re.finditer(r'\(\s*([1-4])\s*\)', q_text))

            options = ["", "", "", ""]
            if option_starts:
                for i, m in enumerate(option_starts):
                    idx = int(m.group(1)) - 1
                    start = m.end()
                    end = option_starts[i+1].start() if i+1 < len(option_starts) else len(q_text)
                    opt = q_text[start:end].strip()
                    opt = re.sub(r'\s+', ' ', opt).strip()
                    options[idx] = opt

                q_title = q_text[:option_starts[0].start()].strip()
                q_title = re.sub(r'\s+', ' ', q_title)
            else:
                parts = [p.strip() for p in q_text.splitlines() if p.strip()]
                if len(parts) >= 5:
                    q_title = parts[0]
                    for i in range(4):
                        options[i] = parts[i+1]
                else:
                    q_title = q_text

            answer_text = ''
            if answer_index and 1 <= answer_index <= 4:
                answer_text = options[answer_index-1]

            results.append((q_title, options[0], options[1], options[2], options[3], answer_text))

    else:
        # Fallback: 不依賴 BeautifulSoup，使用正則式簡單解析（適用於結構規則的 table）
        trs = re.findall(r'<tr[^>]*>(.*?)</tr>', html_text, flags=re.DOTALL | re.IGNORECASE)
        for tr in trs:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, flags=re.DOTALL | re.IGNORECASE)
            if not tds:
                continue
            # 跳過 header (含 colspan)
            first_td_raw = tds[0]
            if re.search(r'colspan\s*=\s*"?\d+"?', tr, flags=re.IGNORECASE):
                continue
            # 跳過 header row 若為標題列（包含 題號, 答案, 題目）
            # 先去掉 HTML tag，再比對文字
            def strip_tags(s):
                return re.sub(r'<.*?>', '', s).strip()
            first_text = strip_tags(tds[0])
            second_text = strip_tags(tds[1]) if len(tds) > 1 else ''
            third_text = strip_tags(tds[2]) if len(tds) > 2 else ''
            header_keys = {'題號', '答案', '題目'}
            if any(key in (first_text, second_text, third_text) for key in header_keys):
                continue
            if len(tds) < 3:
                continue

            td_answer_html = tds[1]
            td_question_html = tds[2]

            # 把 <br> 轉為換行，移除其他 tag
            td_answer_text = re.sub(r'<br\s*/?>', '\n', td_answer_html, flags=re.IGNORECASE)
            td_answer_text = re.sub(r'<.*?>', '', td_answer_text).strip()

            td_question_text = re.sub(r'<br\s*/?>', '\n', td_question_html, flags=re.IGNORECASE)
            td_question_text = re.sub(r'<.*?>', '', td_question_text).strip()

            # 先找題目內的正確答案標示
            answer_index = None
            m = re.search(r'正確答案為[:：]?\s*([1-4])', td_question_text)
            if m:
                answer_index = int(m.group(1))

            if answer_index is None:
                m2 = re.search(r'([1-4])', td_answer_text)
                if m2:
                    answer_index = int(m2.group(1))

            q_text = re.sub(r'正確答案為[:：]?\s*[1-4]', '', td_question_text).strip()

            option_starts = list(re.finditer(r'\(\s*([1-4])\s*\)', q_text))
            options = ["", "", "", ""]
            if option_starts:
                for i, m in enumerate(option_starts):
                    idx = int(m.group(1)) - 1
                    start = m.end()
                    end = option_starts[i+1].start() if i+1 < len(option_starts) else len(q_text)
                    opt = q_text[start:end].strip()
                    opt = re.sub(r'\s+', ' ', opt).strip()
                    options[idx] = opt
                q_title = q_text[:option_starts[0].start()].strip()
                q_title = re.sub(r'\s+', ' ', q_title)
            else:
                parts = [p.strip() for p in q_text.splitlines() if p.strip()]
                if len(parts) >= 5:
                    q_title = parts[0]
                    for i in range(4):
                        options[i] = parts[i+1]
                else:
                    q_title = q_text

            answer_text = ''
            if answer_index and 1 <= answer_index <= 4:
                answer_text = options[answer_index-1]

            results.append((q_title, options[0], options[1], options[2], options[3], answer_text))

    return results


def get_next_filename(prefix, output_dir, file_format='csv'):
    """
    根據前綴和已有檔案，生成下一個檔案名稱
    
    Args:
        prefix: 檔案前綴（例如 '1_'）
        output_dir: 輸出資料夾路徑
        file_format: 檔案格式（預設 'csv'）
    
    Returns:
        完整的檔案路徑
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 找出所有符合前綴的檔案
    pattern = f"{prefix}*.{file_format}"
    existing_files = list(output_path.glob(pattern))
    
    # 提取編號並找出最大值
    max_num = 0
    for file in existing_files:
        # 從檔案名稱中提取數字（例如：1_1.xlsx -> 1）
        match = re.search(rf'^{re.escape(prefix)}(\d+)\.{file_format}$', file.name)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)
    
    # 生成下一個編號
    next_num = max_num + 1
    filename = f"{prefix}{next_num}.{file_format}"
    return output_path / filename


def write_output(rows, output_path):
    output_path = Path(output_path)
    cols = ['題目', '選項1', '選項2', '選項3', '選項4', '答案']
    # 使用 '|' 分隔的 csv
    with output_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(cols)
        for r in rows:
            writer.writerow(r)
    print(f"✓ 輸出 {len(rows)} 筆到 {output_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(description='解析題庫 HTML 並輸出 CSV')
    parser.add_argument('-i', '--input', help=f'輸入 HTML 檔案（預設: {DEFAULT_INPUT_FILE}）', default=DEFAULT_INPUT_FILE)
    parser.add_argument('-o', '--output', help='輸出檔案（預設: 自動編號）', default=None)
    args = parser.parse_args()

    html_path = Path(args.input)
    if not html_path.exists():
        print(f"✗ 找不到檔案: {html_path}")
        return
    html_text = html_path.read_text(encoding='utf-8')

    rows = extract_questions_from_html(html_text)
    if not rows:
        print('✗ 未解析到任何題目，請確認輸入格式是否正確')
        return

    # 如果沒有指定輸出檔案，使用自動編號
    if args.output is None:
        output_path = get_next_filename(FILE_PREFIX, OUTPUT_DIR, DEFAULT_FORMAT)
    else:
        output_path = Path(args.output)

    write_output(rows, output_path)


if __name__ == '__main__':
    main()
