from tkinter import Tk, END, messagebox, filedialog, Scale, Label
from ttkbootstrap import Button, Text, Scrollbar, Treeview
from warnings import filterwarnings
from datetime import datetime
from pygame.mixer import init
from pygame.mixer import music#导入库
from PIL import Image, ImageTk
#——————————————————————————————————————————————————————————————————————
filterwarnings('ignore')#取消警告


class StartApp:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('551x395')
        self.window.attributes('-topmost', True)
        self.window.title('待办')
        self.window.resizable(False, False)
        self.window.overrideredirect(True)
        self.center_window(551, 395)

        # 加载背景图片
        try:
            self.bg_image = Image.open('PNG.png')
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = Label(self.window, image=self.bg_photo)
        except:
            # 如果图片加载失败，使用纯色背景
            self.bg_label = Label(self.window, bg="#ffffff")

        self.label = Label(self.window, text="正在加载中………………", bg='white',font=("Arial", 36, "bold"))
        self.build()

        # 设置3秒后自动关闭启动画面并打开主程序
        self.window.after(1000, self.transition_to_main)

    def build(self):
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.place(x=10, y=200)

    def center_window(self, width, height):
        """将窗口居中显示"""
        # 获取屏幕尺寸
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # 计算窗口位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置窗口大小和位置
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def transition_to_main(self):
        """过渡到主程序"""
        self.window.destroy()  # 销毁启动窗口
        # 直接在主线程中启动主程序
        self.start_main_app()

    def start_main_app(self):
        """启动主程序"""
        app = Application()
        app.run()


class Application:
    PRIORITY_INFO = {
        '高等级': {'color': '#ffcccc', 'order': 3},  # 浅红色，最高优先级
        '中等级': {'color': '#ffffcc', 'order': 2},  # 浅黄色，中等优先级
        '低等级': {'color': '#ccffcc', 'order': 1},  # 浅绿色，最低优先级
    }
    def __init__(self):
        self.value = ''
        self.status = True
        self.isplay = False
        self.ispaused = False
        init()#初始化变量
        self.window = Tk()
        self.window.geometry('450x320')
        self.window.attributes('-topmost', True)
        self.window.title('待办')
        self.window.resizable(False, False)
        self.center_window(450, 320)
        self.music_load = ""
        try:
            self.window.iconbitmap('favicon.ico')
        except:
            pass#创建窗口
        columns = ('任务', '优先级')
        self.treeview = Treeview(self.window, columns=columns, show='headings', height=9, selectmode='extended')

        # 设置列标题
        self.treeview.heading('任务', text='任务内容')
        self.treeview.heading('优先级', text='优先级')

        # 设置列宽度
        self.treeview.column('任务', width=250, anchor='w')
        self.treeview.column('优先级', width=80, anchor='center')

        # 创建滚动条
        self.scrollbar = Scrollbar(self.window, bootstyle="round")

        # 配置滚动条与Treeview的关联
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.treeview.yview)

        # 创建其他控件
        self.task_high = Button(self.window, text='高等级', padding=(10, 5), command=self.high)
        self.task_mid = Button(self.window, text='中等级', padding=(10, 5), command=self.mid)
        self.task_low = Button(self.window, text='低等级', padding=(10, 5), command=self.low)
        self.open_ = Button(self.window, text='打开', padding=(11, 5), command=self.open_file, bootstyle='info')
        self.save_ = Button(self.window, text='保存', padding=(11, 5), command=self.save_file, bootstyle='info')
        self.task_create = Text(self.window, width=25, height=1)
        self.task_created = Button(self.window, text='创建', padding=(15, 5), command=self.selected,
                                   bootstyle='success')
        self.delete = Button(self.window, text='删除', padding=(15, 5), command=self.delete_selected,
                             bootstyle='danger')
        self.start = Button(self.window, text='开始', padding=(10, 2), command=self.play_)
        self.pause = Button(self.window, text='暂停', padding=(10, 2), command=self.pause_)
        self.stop = Button(self.window, text='停止', padding=(10, 2), command=self.stop_)
        self.music_load_btn = Button(self.window, text='导入音乐', padding=(10, 2), command=self.open_music)
        self.volume_scale = Scale(self.window, from_=0, to=100, orient='vertical', length=180, bg="#f0f0f0",
                                  command=self.volume)
        self.volume_scale.set(30)  # 默认音量
        self.attributes = Button(self.window, text='取消置顶', padding=(10, 2), command=self.attribute,
                                 bootstyle='warning')
        self.l1 = Label(self.window, text='0%')
        self.l2 = Label(self.window, text='100%')

        # 添加排序按钮
        self.sort_priority_btn = Button(self.window, text='按优先级排序', padding=(10, 2),
                                        command=self.sort_by_priority, bootstyle='warning')
        self.sort_task_btn = Button(self.window, text='按名称排序', padding=(10, 2), command=self.sort_by_task,
                                    bootstyle='warning')
        self.build()

    #——————————————————————————————————————————————————————————————————————
    # 定义优先级颜色
    def center_window(self, width, height):
        """将窗口居中显示"""
        # 获取屏幕尺寸
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # 计算窗口位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置窗口大小和位置
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    def open_file(self):
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[
                ("文本文件", "*.txt")
            ]
        )

        if file_path:  # 用户选择了文件
            try:
                tasks = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for line in content.splitlines():
                        if line.strip():  # 过滤空行
                            # 解析行内容，格式应为"任务内容------优先级"
                            if '------' in line:
                                task_text, priority = line.split('------', 1)
                                tasks.append((task_text.strip(), priority.strip()))
                            else:
                                # 如果没有优先级信息，默认设为低等级
                                tasks.append((line.strip(), '低等级'))

                # 清空现有任务
                for item in self.treeview.get_children():
                    self.treeview.delete(item)

                # 按优先级排序后添加
                sorted_tasks = self.sort_tasks_by_priority(tasks)
                for task_text, priority in sorted_tasks:
                    self.add_task_to_treeview(task_text, priority)

            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    #打开待办
    def open_music(self):
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            title="选择音乐",
            filetypes=[
                ("mp3文件", "*.mp3")
            ]
        )

        if file_path:  # 用户选择了文件
            try:
                self.music_load = file_path
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    #打开音乐
    def save_file(self):
        # 打开保存文件对话框
        default_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            title="保存文件",
            defaultextension=".txt",  # 默认扩展名
            filetypes=[
                ("文本文件", "*.txt")
            ]
        )

        if file_path:  # 用户选择了保存位置
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    # 按优先级排序后保存
                    tasks = []
                    for item in self.treeview.get_children():
                        task_text = self.treeview.item(item, 'values')[0]
                        priority = self.treeview.item(item, 'values')[1]
                        tasks.append((task_text, priority))

                    sorted_tasks = self.sort_tasks_by_priority(tasks)
                    for task_text, priority in sorted_tasks:
                        file.write(f"{task_text}------{priority}\n")

                messagebox.showinfo("成功", "文件保存成功！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{str(e)}")
    #保存待办
    def play_(self):
        if self.ispaused:
            music.unpause()
            self.ispaused = False
            self.isplay = True
        else:
            try:
                music.load(self.music_load)
                music.play(loops=-1)
                self.ispaused = False
                self.isplay = True
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    #播放音乐
    def stop_(self):
        music.stop()
        self.ispaused = False
        self.isplay = False
    #停止播放音乐
    def pause_(self):
        if self.isplay and not self.ispaused:
            music.pause()
            self.ispaused = True
            self.isplay = False
    #暂停音乐
    def high(self):
        self.value = '高等级'

    def mid(self):
        self.value = '中等级'

    def low(self):
        self.value = '低等级'
    #定义优先级
    def delete_selected(self):
        selected_items = self.treeview.selection()

        if not selected_items:
            messagebox.showinfo("提示", "请先选择项目")
            return

        # 询问确认
        if messagebox.askyesno("确认", f"确定要删除选中的 {len(selected_items)} 个项目吗？"):
            for item in selected_items:
                self.treeview.delete(item)
    #删除项
    def sort_tasks_by_priority(self,tasks):
        """按优先级排序任务列表"""
        return sorted(tasks, key=lambda x: self.PRIORITY_INFO.get(x[1], {'order': 0})['order'], reverse=True)
    #排序任务列表
    def add_task_to_treeview(self,task_text, priority):
        """向Treeview中添加任务并设置颜色"""
        item_id = self.treeview.insert('', 'end', values=(task_text, priority))

        # 根据优先级设置行颜色
        color_info = self.PRIORITY_INFO.get(priority, {'color': '#ffffff'})
        color = color_info['color']
        self.treeview.tag_configure(priority, background=color)
        self.treeview.item(item_id, tags=(priority,))
    #添加任务1
    def selected(self):
        task_text = self.task_create.get('1.0', END).strip()

        if not task_text:
            messagebox.showinfo("提示", "请先输入内容")
            return

        if self.value == '':
            self.value = '低等级'

        # 添加到Treeview
        self.add_task_to_treeview(task_text, self.value)
        self.task_create.delete('1.0', END)

        # 重新按优先级排序所有任务
        self.resort_tasks()
    #添加任务2
    def resort_tasks(self):
        """重新按优先级排序Treeview中的所有任务"""
        # 获取所有任务
        tasks = []
        for item in self.treeview.get_children():
            task_text = self.treeview.item(item, 'values')[0]
            priority = self.treeview.item(item, 'values')[1]
            tasks.append((task_text, priority))

        # 清空Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # 按优先级排序后重新添加
        sorted_tasks = self.sort_tasks_by_priority(tasks)
        for task_text, priority in sorted_tasks:
            self.add_task_to_treeview(task_text, priority)
    #重新按优先级排序

    def sort_by_priority(self):
        """按优先级排序按钮"""
        self.resort_tasks()
        messagebox.showinfo("提示", "已按优先级排序")
    #按优先级排序（调用）


    def sort_by_task(self):
        """按任务名称排序按钮"""
        # 获取所有任务
        tasks = []
        for item in self.treeview.get_children():
            task_text = self.treeview.item(item, 'values')[0]
            priority = self.treeview.item(item, 'values')[1]
            tasks.append((task_text, priority))

        # 按任务名称排序
        sorted_tasks = sorted(tasks, key=lambda x: x[0])

        # 清空Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # 重新添加
        for task_text, priority in sorted_tasks:
            self.add_task_to_treeview(task_text, priority)

        messagebox.showinfo("提示", "已按任务名称排序")
    #按任务名称排序
    def attribute(self):
        if not self.status:
            self.window.attributes('-topmost', True)
            self.attributes['text'] = '取消置顶'
        elif self.status:
            self.window.attributes('-topmost', False)
            self.attributes['text'] = '置顶'
        self.status = not self.status
    #置顶功能
    def volume(self,val):
        volume_ = float(val) / 100
        music.set_volume(volume_)
    #调节音量
    #——————————————————————————————————————————————————————————————————————
    # 创建Treeview（两列列表）
    def build(self):
        self.music_load_btn.place(x=370, y=285)
        self.volume_scale.place(x=370, y=10)
        self.scrollbar.place(x=350, y=100, width=15, height=190)
        self.treeview.place(x=10, y=100)
        self.task_high.place(x=10, y=10)
        self.task_mid.place(x=80, y=10)
        self.task_low.place(x=150, y=10)
        self.task_create.place(x=10, y=60)
        self.task_created.place(x=220, y=60)
        self.delete.place(x=220, y=10)
        self.open_.place(x=290, y=10)
        self.save_.place(x=290, y=60)
        self.start.place(x=370, y=195)
        self.pause.place(x=370, y=225)
        self.stop.place(x=370, y=255)
        self.l1.place(x=390, y=5)
        self.l2.place(x=390, y=160)
        self.sort_priority_btn.place(x=10, y=290)
        self.sort_task_btn.place(x=120, y=290)
        self.attributes.place(x=220, y=290)
    def run(self):
        self.window.mainloop()#主循环
if __name__ == "__main__":
    start_app = StartApp()
    start_app.window.mainloop()