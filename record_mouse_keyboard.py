#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記錄滑鼠點擊位置和鍵盤按鍵

使用說明：
  python3 record_mouse_keyboard.py
  
  按 ESC 鍵停止記錄，會自動保存到 actions.json
"""

import json
import time
from datetime import datetime
from pathlib import Path

from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener


class ActionRecorder:
    """記錄滑鼠點擊位置和鍵盤按鍵"""
    
    def __init__(self):
        self.actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.recording = False
    
    def on_click(self, x, y, button, pressed):
        """記錄滑鼠點擊位置"""
        if self.recording and pressed:  # 只記錄按下，不記錄釋放
            elapsed = time.time() - self.start_time
            button_name = str(button).replace('Button.', '').replace('left', '左鍵').replace('right', '右鍵').replace('middle', '中鍵')
            self.actions.append({
                'type': 'click',
                'x': x,
                'y': y,
                'button': str(button),
                'time': elapsed
            })
            print(f"[{elapsed:.3f}s] 點擊: ({x}, {y}) - {button_name}")
    
    def on_press(self, key):
        """記錄鍵盤按鍵"""
        if self.recording:
            elapsed = time.time() - self.start_time
            try:
                key_str = key.char
                key_display = key_str
            except AttributeError:
                key_str = str(key)
                # 美化特殊按鍵顯示
                key_display = key_str.replace('Key.', '').replace('space', '空白').replace('enter', 'Enter').replace('tab', 'Tab')
                key_display = key_display.replace('backspace', 'Backspace').replace('delete', 'Delete')
                key_display = key_display.replace('esc', 'ESC').replace('shift', 'Shift').replace('ctrl', 'Ctrl')
                key_display = key_display.replace('alt', 'Alt').replace('cmd', 'Cmd')
            
            self.actions.append({
                'type': 'key',
                'key': key_str,
                'time': elapsed
            })
            
            print(f"[{elapsed:.3f}s] 按鍵: {key_display}")
            
            # ESC 鍵停止記錄
            if key == Key.esc:
                print("\n✓ 停止記錄（按了 ESC 鍵）")
                return False
    
    def start_recording(self):
        """開始記錄"""
        print("=" * 60)
        print("開始記錄滑鼠點擊位置和鍵盤按鍵...")
        print("按 ESC 鍵停止記錄")
        print("=" * 60)
        
        self.actions = []
        self.start_time = time.time()
        self.recording = True
        
        # 記錄開始時間戳
        self.actions.append({
            'type': 'recording_start',
            'timestamp': datetime.now().isoformat(),
            'time': 0.0
        })
        
        # 啟動監聽器
        self.mouse_listener = MouseListener(on_click=self.on_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        # 等待 ESC 鍵停止
        try:
            self.keyboard_listener.join()
        except KeyboardInterrupt:
            pass
        
        self.stop_recording()
    
    def stop_recording(self):
        """停止記錄"""
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.actions.append({
            'type': 'recording_end',
            'time': elapsed
        })
        
        # 計算實際操作數量（排除開始和結束標記）
        action_count = len([a for a in self.actions if a['type'] in ('click', 'key')])
        print(f"\n✓ 記錄完成！共記錄 {action_count} 個操作，總時長 {elapsed:.2f} 秒")
    
    def save_to_file(self, filepath='actions.json'):
        """保存記錄到檔案"""
        output_path = Path(filepath)
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(self.actions, f, indent=2, ensure_ascii=False)
        print(f"✓ 已保存到：{output_path.absolute()}")


if __name__ == '__main__':
    recorder = ActionRecorder()
    try:
        recorder.start_recording()
    except KeyboardInterrupt:
        recorder.stop_recording()
    
    recorder.save_to_file()
