#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑鼠鍵盤自動化腳本

使用說明：
  python3 automate_actions.py
  
  執行預設的自動化操作序列
"""

import time
import platform
import pyperclip
import subprocess
from pathlib import Path
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, Listener as KeyboardListener


class ActionAutomator:
    """滑鼠鍵盤自動化執行器"""
    
    def __init__(self, action_interval=0.5):
        """
        初始化自動化執行器
        
        Args:
            action_interval: 每個操作之間的間隔時間（秒）
        """
        self.action_interval = action_interval
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.is_mac = platform.system() == 'Darwin'
        self.should_stop = False
        self.keyboard_listener = None
        
        # 根據作業系統設定修飾鍵
        if self.is_mac:
            self.modifier_key = Key.cmd  # Mac 使用 Cmd
        else:
            self.modifier_key = Key.ctrl  # Windows 使用 Ctrl
    
    def on_key_press(self, key):
        """監聽鍵盤按鍵，ESC 鍵停止循環"""
        if key == Key.esc:
            print("\n\n偵測到 ESC 鍵，將在當前腳本執行完成後停止循環...")
            self.should_stop = True
            return False  # 停止監聽器
    
    def wait(self, seconds=None):
        """等待指定時間，如果未指定則使用預設間隔"""
        time.sleep(seconds if seconds is not None else self.action_interval)
    
    def click(self, x, y, button=Button.left):
        """
        點擊指定位置
        
        Args:
            x: X 座標
            y: Y 座標
            button: 滑鼠按鍵（預設左鍵）
        """
        self.mouse_controller.position = (x, y)
        self.wait(0.1)  # 移動到位置後稍等一下
        self.mouse_controller.click(button)
        print(f"點擊: ({x}, {y})")
        self.wait()
    
    def press_key_combination(self, modifier, key):
        """
        按下鍵盤組合鍵
        
        Args:
            modifier: 修飾鍵（如 Ctrl 或 Cmd）
            key: 主要按鍵（可以是字符串或 Key 對象）
        """
        with self.keyboard_controller.pressed(modifier):
            self.keyboard_controller.press(key)
            self.keyboard_controller.release(key)
        key_name = key if isinstance(key, str) else str(key).replace('Key.', '')
        modifier_name = 'Cmd' if self.is_mac else 'Ctrl'
        print(f"按下: {modifier_name} + {key_name}")
        self.wait()
    
    def type_text(self, text):
        """
        輸入文字
        
        Args:
            text: 要輸入的文字
        """
        self.keyboard_controller.type(text)
        print(f"輸入: {text}")
        self.wait()
    
    def paste_text(self, text):
        """
        將文字複製到剪貼簿並貼上
        
        Args:
            text: 要貼上的文字
        """
        pyperclip.copy(text)
        self.press_key_combination(self.modifier_key, 'v')
        print(f"貼上文字（長度: {len(text)} 字元）")
    
    def press_key(self, key):
        """
        按下單一按鍵
        
        Args:
            key: 按鍵（可以是字符串或 Key 對象）
        """
        self.keyboard_controller.press(key)
        self.keyboard_controller.release(key)
        key_name = key if isinstance(key, str) else str(key).replace('Key.', '')
        print(f"按下: {key_name}")
        self.wait()
    
    def save_clipboard_to_file(self, filepath):
        """
        將剪貼簿內容儲存到檔案
        
        Args:
            filepath: 檔案路徑
        """
        try:
            clipboard_content = pyperclip.paste()
            file_path = Path(filepath)
            file_path.write_text(clipboard_content, encoding='utf-8')
            print(f"✓ 已將剪貼簿內容儲存到: {file_path.absolute()}")
            self.wait(0.3)  # 稍等一下確保檔案寫入完成
        except Exception as e:
            print(f"✗ 儲存檔案時發生錯誤: {e}")
            raise
    
    def run_script(self, script_path):
        """
        執行 Python 腳本
        
        Args:
            script_path: 腳本路徑
        """
        try:
            script_path = Path(script_path)
            if not script_path.exists():
                print(f"✗ 找不到腳本: {script_path}")
                return
            
            print(f"執行腳本: {script_path}")
            result = subprocess.run(
                ['python3', str(script_path)],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            if result.returncode == 0:
                print(f"✓ 腳本執行成功")
            else:
                print(f"✗ 腳本執行失敗，返回碼: {result.returncode}")
            
            self.wait(0.5)
        except Exception as e:
            print(f"✗ 執行腳本時發生錯誤: {e}")
            raise
    
    def run_automation(self):
        """執行自動化操作序列"""
        print("=" * 60)
        print("開始執行自動化操作...")
        print(f"作業系統: {platform.system()}")
        print(f"操作間隔: {self.action_interval} 秒")
        print("=" * 60)
        
        # 點擊位置 1
        # TODO: 請填入座標 (x, y)
        self.click(100, 175)
        
        # 點擊位置 2
        # TODO: 請填入座標 (x, y)
        self.click(300, 750)
        
        # 點擊位置 3
        # TODO: 請填入座標 (x, y)
        self.click(800, 800)
        
        # 點擊位置 4
        # TODO: 請填入座標 (x, y)
        self.click(1010, 20)
        
        # 點擊位置 5
        # TODO: 請填入座標 (x, y)
        self.click(1240, 200)
        
        # 按 Ctrl+V (Mac: Cmd+V) 貼上
        paste_content = """const yourAnswers = [
    1, 3, 2, 4, 1, 3, 2, 4, 1, 3, // 第 1 到 10 題
    2, 4, 1, 3, 2, 4, 1, 3, 2, 4, // 第 11 到 20 題
    1, 3, 2, 4, 1, 3, 2, 4, 1, 3, // 第 21 到 30 題
    2, 4, 1, 3, 2, 4, 1, 3, 2, 4, // 第 31 到 40 題
    1, 3, 2, 4, 1, 3, 2, 4, 1, 3, // 第 41 到 50 題
    2, 4, 1, 3, 2, 4, 1, 3,        // 第 51 到 58 題
    2, 4, 1, 3, 2, 4             // 第 59 到 64 題
];

const allQuestionContainers = document.querySelectorAll('.body');

if (allQuestionContainers.length < yourAnswers.length) {
    console.error(`❌ 錯誤：答案數量 (${yourAnswers.length}) 多於頁面上的題目數量 (${allQuestionContainers.length})。`);
}

yourAnswers.forEach((answerValue, index) => {
    const questionIndex = index + 1; // 題目從 1 開始
    const container = allQuestionContainers[index];

    if (!container) {
        console.warn(`⚠️ 警告：找不到第 ${questionIndex} 題的容器。`);
        return;
    }

    const targetRadio = container.querySelector(`input[type="radio"][value="${answerValue}"]`);

    if (targetRadio) {
        targetRadio.checked = true;
        console.log(`✅ 第 ${questionIndex} 題成功選取選項 (${answerValue})。`);
    } else {
        console.warn(`⚠️ 警告：第 ${questionIndex} 題找不到對應選項 (${answerValue})。`);
    }
});"""
        self.paste_text(paste_content)
        
        # 按下 Enter
        self.press_key(Key.enter)

        # 點擊位置 6
        # TODO: 請填入座標 (x, y)
        self.click(980, 650)
        
        # 點擊位置 7
        # TODO: 請填入座標 (x, y)
        self.click(1170, 200)
        
        # 點擊位置 8
        # TODO: 請填入座標 (x, y)
        self.click(1100, 400)

        # 按 Ctrl+F (Mac: Cmd+F) 搜尋
        self.press_key_combination(self.modifier_key, 'f')

        # 按 Ctrl+V (Mac: Cmd+V) 貼上 "tbody"
        self.paste_text("tbody")

        # 點擊位置 8
        # TODO: 請填入座標 (x, y)
        self.click(1300, 445)
        
        # 按 Ctrl+C (Mac: Cmd+C) 複製
        self.press_key_combination(self.modifier_key, 'c')
        
        # 等待一下確保複製完成
        self.wait(0.3)
        
        # 將剪貼簿內容儲存為 questions.html
        print("\n[步驟] 將剪貼簿內容儲存為 questions.html")
        self.save_clipboard_to_file('questions.html')
        
        # 執行 parse_questions.py
        print("\n[步驟] 執行 parse_questions.py")
        self.run_script('parse_questions.py')
        
        # 按 Ctrl+F (Mac: Cmd+F) 搜尋
        self.press_key_combination(self.modifier_key, 'f')

        # 按 Ctrl+V (Mac: Cmd+V) 貼上 "active"
        self.paste_text("active")

        print("\n" + "=" * 60)
        print("✓ 自動化操作執行完成！")
        print("=" * 60)
    
    def run_loop(self):
        """循環執行自動化操作，直到按下 ESC 鍵"""
        print("\n" + "=" * 60)
        print("開始循環執行自動化操作...")
        print("按 ESC 鍵可停止循環")
        print("=" * 60)
        
        # 啟動 ESC 鍵監聽器
        self.should_stop = False
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        loop_count = 0
        while not self.should_stop:
            loop_count += 1
            print(f"\n{'=' * 60}")
            print(f"開始第 {loop_count} 次循環")
            print(f"{'=' * 60}")
            
            # 執行完整的自動化流程
            self.run_automation()
            
            # 檢查是否收到停止信號
            if self.should_stop:
                print("\n收到停止信號，退出循環")
                break
            
            # 等待 2 秒後再次執行
            print(f"\n等待 2 秒後開始第 {loop_count + 1} 次循環...")
            print("（按 ESC 鍵可停止）")
            for i in range(20):  # 2秒 = 20 * 0.1秒，每0.1秒檢查一次
                if self.should_stop:
                    break
                time.sleep(0.1)
        
        # 停止鍵盤監聽器
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        print("\n" + "=" * 60)
        print(f"✓ 循環執行完成！共執行 {loop_count} 次")
        print("=" * 60)


if __name__ == '__main__':
    # 建立自動化執行器，設定操作間隔為 0.5 秒
    # 可以調整 action_interval 參數來改變操作間隔
    automator = ActionAutomator(action_interval=0.5)
    
    try:
        # 給使用者 3 秒準備時間
        print("\n將在 3 秒後開始執行...")
        print("請確保目標應用程式已開啟並準備好")
        print("腳本將循環執行，按 ESC 鍵可停止")
        time.sleep(3)
        
        # 循環執行自動化操作
        automator.run_loop()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        if automator.keyboard_listener:
            automator.keyboard_listener.stop()
    except Exception as e:
        print(f"\n\n發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        if automator.keyboard_listener:
            automator.keyboard_listener.stop()

