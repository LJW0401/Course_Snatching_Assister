import cv2
from PIL import ImageGrab
import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
import pyautogui
import sys,os
import base64
import datetime
import time

import pic

def AppPath():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)            #没打包前的py目录




class Get_Click_Pos():
    def __init__(self) -> None:
        self.click_pos = (0,0)
    
    
    def CreateWindow(self):
        self.window = tk.Tk()
        # 获取屏幕的宽度和高度
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # 设置窗口大小为全屏
        self.window.geometry(f"{screen_width}x{screen_height}")
        # 设置窗口为全屏和无边框
        self.window.attributes('-fullscreen', True)
        self.window.overrideredirect(True)
        # 设置窗口透明度（0表示完全透明，1表示不透明）
        self.window.attributes('-alpha', 0.5)
        # 设置窗口背景颜色为纯色（这里使用白色作为示例）
        self.window.configure(bg='green')
        # 添加鼠标点击事件监听器
        self.window.bind("<Button-1>", self.CloseWindow)
    
    
    def Run(self):
        # 进入主循环
        self.window.mainloop()
    
    
    def CloseWindow(self, event):
        # print(event.x, event.y)
        self.click_pos = (event.x, event.y)
        self.window.destroy()
        self.window.quit()



class Click_Perform():
    def __init__(self) -> None:
        self.click_pos_1 = (0,0)
        self.click_pos_2 = (0,0)
        self.template_list = []
    
    
    def GetScreenShot(self):
        screenshot = ImageGrab.grab()# 截取整个屏幕
        screenshot_np = np.array(screenshot)# 将Pillow图像转换为NumPy数组
        screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)# 将NumPy数组转换为OpenCV格式的图像
        # screenshot.show()# 显示截图
        
        return screenshot_cv2
    
    
    def MatchTemplate(self,template):
        result = cv2.matchTemplate(self.GetScreenShot(), template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 这是相似度的阈值，可以根据需要调整
        loc = np.where(result >= threshold)# 设置阈值来筛选匹配结果
        return loc[0].shape[0] #返回匹配到的template数量
    
    
    def ClickButton(self):
        n = 0
        n += self.MatchTemplate(template=self.template_list[0])
        n += self.MatchTemplate(template=self.template_list[1])
        
        if n == 0:
            pyautogui.moveTo(# 移动鼠标到按钮1位置，duration是移动的时间（秒）
                self.click_pos_1[0],
                self.click_pos_1[1],
                duration=0.01
                )
            time.sleep(0.003)
            pyautogui.click()  # 执行鼠标左键单击操作
            
            pyautogui.moveTo(# 移动鼠标到按钮2位置，duration是移动的时间（秒）
                self.click_pos_2[0], 
                self.click_pos_2[1],
                duration=0.01
                )
            time.sleep(0.003)
            pyautogui.click()  # 执行鼠标左键单击操作



class Course_Snatching_Assister():
    def __init__(self):
        self.__version__ = '1.0.0'
        
        self.window = tk.Tk()
        self.window.title('Course Snatching Assister')
        self.window.geometry('500x300')
        # self.window.resizable(0,0)
        
        self.format_str = '%Y-%m-%d %H:%M:%S'
        self.StartTimeStr = tk.StringVar()
        self.StartTimeStr.set(datetime.datetime.now().strftime(self.format_str))
        self.FinishTimeStr = tk.StringVar()
        self.FinishTimeStr.set(
            (datetime.datetime.now()+datetime.timedelta(seconds=15)).strftime(self.format_str)
            )
        # self.StartTimeStr.set('2021-09-01 00:00:00')
        
        self.CreateWidgets()
        self.get_click_pos = Get_Click_Pos()
        self.got_click_pos_1 = False
        self.got_click_pos_2 = False
        self.click_perform = Click_Perform()
        
        self.service_is_running = False


    def CreateWidgets(self):
        self.Frame_ButtonPos = tk.LabelFrame(
            self.window, 
            text='标定点击位置',
            relief='groove',bd=2
        )
        self.Frame_ButtonPos.place(x=10,y=10,width=250, height=120)
        self.CreateWidgets_Frame_ButtonPos()
        
        self.Frame_SetExecutionParameters = tk.LabelFrame(
            self.window, 
            text='执行参数',
            relief='groove',bd=2
        )
        self.Frame_SetExecutionParameters.place(x=10,y=130,width=250, height=160)
        self.CreateWidgets_Frame_SetExecutionParameters()
        
        self.Frame_ClickTest = tk.LabelFrame(
            self.window, 
            text='测试区',
            relief='groove',bd=2
        )
        self.Frame_ClickTest.place(x=260,y=10,width=150, height=280)
        self.CreateWidgets_Frame_Frame_ClickTest()
    
    
    def CreateWidgets_Frame_Frame_ClickTest(self):
        self.Button_ClickTest_1 = tk.Button(
            self.Frame_ClickTest,
            text='按钮1',
            command=lambda : print('已点击按钮1')
        )
        self.Button_ClickTest_1.place(x=20,y=10,width=100, height=30)
        
        self.Button_ClickTest_2 = tk.Button(
            self.Frame_ClickTest,
            text='按钮2',
            command=lambda : print('已点击按钮2')
        )
        self.Button_ClickTest_2.place(x=20,y=160,width=100, height=30)
        
    
    def CreateWidgets_Frame_SetExecutionParameters(self):
        self.Label_SetStartTime = tk.Label(
            self.Frame_SetExecutionParameters,
            text='开始时间：'
        )
        self.Label_SetStartTime.place(x=0,y=10,width=80, height=30)
        
        self.Entry_StartTime = tk.Entry(
            self.Frame_SetExecutionParameters,
            textvariable=self.StartTimeStr,
            width=20
        )
        self.Entry_StartTime.place(x=70,y=10,width=170, height=30)

        self.Label_SetStartTime = tk.Label(
            self.Frame_SetExecutionParameters,
            text='结束时间：'
        )
        self.Label_SetStartTime.place(x=0,y=50,width=80, height=30)
        
        self.Entry_StartTime = tk.Entry(
            self.Frame_SetExecutionParameters,
            textvariable=self.FinishTimeStr,
            width=20
        )
        self.Entry_StartTime.place(x=70,y=50,width=170, height=30)
        
        self.Button_StartService = tk.Button(
            self.Frame_SetExecutionParameters,
            text='开始服务',
            command=self.Button_StartService_Click
        )
        self.Button_StartService.place(x=30,y=90,width=100, height=30)
    
    
    def Button_StartService_Click(self):
        if self.got_click_pos_1 and self.got_click_pos_2:
            self.service_is_running = not self.service_is_running
            if self.service_is_running:
                self.Button_StartService.configure(text='停止服务')
                self.Serve()
            else:
                self.Button_StartService.configure(text='开始服务')
        else:
            messagebox.showinfo('提示','请先标定按钮位置')


    def Serve(self):
        if self.service_is_running:
            if datetime.datetime.now() < datetime.datetime.strptime(self.FinishTimeStr.get(),self.format_str):
                # 还没到达停止时间，持续点击选择的位置
                self.click_perform.ClickButton()
            else:
                # 到达停止时间，点击停止服务
                self.Button_StartService_Click()
            self.window.after(1, self.Serve)
        
        
    def CreateWidgets_Frame_ButtonPos(self):
        x = 10; height = 30
        y1 = 10
        self.Label_Button_1_Signal = tk.Label(
            self.Frame_ButtonPos,
            bg='red',
        )
        self.Label_Button_1_Signal.place(x=x,y=y1,width=height, height=height)

        self.Button_FixButton_1_Pos = tk.Button(
            self.Frame_ButtonPos,
            text='标定选择按钮的位置',
            command=self.Button_FixButton_1_Pos_Click
        )
        self.Button_FixButton_1_Pos.place(x=x+30,y=y1,width=150, height=height)
        
        y2 = 50
        self.Label_Button_2_Signal = tk.Label(
            self.Frame_ButtonPos,
            bg='red',
        )
        self.Label_Button_2_Signal.place(x=x,y=y2,width=height, height=height)
        
        self.Button_FixButton_2_Pos = tk.Button(
            self.Frame_ButtonPos,
            text='标定确定按钮的位置',
            command=self.Button_FixButton_2_Pos_Click
        )
        self.Button_FixButton_2_Pos.place(x=x+30,y=y2,width=150, height=height)
        
    
    
    def Button_FixButton_1_Pos_Click(self):
        self.get_click_pos.CreateWindow()
        self.get_click_pos.Run()
        self.click_perform.click_pos_1 = self.get_click_pos.click_pos
        self.Label_Button_1_Signal.configure(bg='green')
        self.got_click_pos_1 = True
        print(self.click_perform.click_pos_1)
        
    
    def Button_FixButton_2_Pos_Click(self):
        self.get_click_pos.CreateWindow()
        self.get_click_pos.Run()
        self.click_perform.click_pos_2 = self.get_click_pos.click_pos
        self.Label_Button_2_Signal.configure(bg='green')
        self.got_click_pos_2 = True
        print(self.click_perform.click_pos_2)
    
    
    def BlankFunc(self):
        print('BlankFunc')
    
    
    def Run(self):
        self.window.mainloop()
        
if __name__ == '__main__':
    # 将图像数据转换为NumPy数组
    pic_stop_1 = np.frombuffer(base64.b64decode(pic.stop_1), np.uint8)
    pic_stop_1 = cv2.imdecode(pic_stop_1, cv2.IMREAD_COLOR)
    pic_stop_2 = np.frombuffer(base64.b64decode(pic.stop_2), np.uint8)
    pic_stop_2 = cv2.imdecode(pic_stop_2, cv2.IMREAD_COLOR)
    pic_do = np.frombuffer(base64.b64decode(pic.do), np.uint8)
    pic_do = cv2.imdecode(pic_do, cv2.IMREAD_COLOR)

    # 使用OpenCV显示图像
    # cv2.imshow('Decoded Image', pic_stop_1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    
    course_snatching_assister = Course_Snatching_Assister()
    course_snatching_assister.click_perform.template_list.append(pic_stop_1)
    course_snatching_assister.click_perform.template_list.append(pic_stop_2)
    course_snatching_assister.click_perform.template_list.append(pic_do)
    course_snatching_assister.Run()
    
    