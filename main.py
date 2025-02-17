import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        # 初始化游戏窗口
        self.master = master
        self.master.title("贪吃蛇游戏——BySherlock")
        self.master.resizable(False, False)

        # 创建画布用于绘制游戏界面
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        # self.canvas.create_text(200, 50, text="使用方向键控制蛇的移动，吃到食物得分", fill="black", font=("Arial", 12))
        self.canvas.pack()

        self.instructions_label = tk.Label(self.master, text="使用方向键控制蛇的移动，吃到食物得分，空格键暂停/继续游戏", width=50,wraplength=250, font=("simhei", 12))
        self.instructions_label.pack(pady=10)

        # 创建得分标签用于显示当前得分
        self.score_label = tk.Label(self.master, text="得分: 0", width=20, font=("simhei", 16))
        self.score_label.pack()

        # 初始化蛇的身体部分、方向、游戏结束标志和暂停标志
        self.snake = [(100, 100), (100, 150), (100, 200)]
        self.direction = "Up"
        self.game_over = False
        self.paused = True  # 初始状态为暂停
        self.game_started = False  # 游戏是否开始的标志

        # 生成初始食物位置
        self.food = self.generate_food()

        # 绑定键盘事件用于控制蛇的移动方向（但仅在游戏开始时才有效）
        self.bind_keys()

        # 添加“开始游戏”按钮
        self.start_button = tk.Button(self.master, text="开始游戏", command=self.start_game, width=10)
        self.start_button.pack(pady=20)




    def start_game(self):
        # 开始游戏，设置游戏开始标志，并调用游戏循环函数（如果之前未开始）
        if not self.game_started:
            self.game_started = True
            self.paused = False
            self.game_loop()

    def generate_food(self):
        # 生成随机食物位置，确保食物不在蛇的身体上
        while True:
            food = (random.randint(1, 39) * 10, random.randint(1, 39) * 10)
            if food not in self.snake:
                return food

    def game_loop(self):
        # 游戏循环，检查碰撞、更新状态并绘制界面（仅在游戏开始时进行）
        if self.game_started and not self.paused and not self.game_over:
            self.canvas.delete("all")

            # 计算蛇头的新位置
            new_head = (
                self.snake[0][0] + (0 if self.direction in ("Up", "Down") else 10 if self.direction == "Right" else -10),
                self.snake[0][1] + (0 if self.direction in ("Left", "Right") else 10 if self.direction == "Down" else -10),
            )

            # 检查是否碰撞到边界或自身
            if new_head in self.snake or new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400:
                self.game_over = True
                self.show_game_over()
                return

            # 更新蛇的身体部分
            self.snake.insert(0, new_head)

            # 检查是否吃到食物
            if new_head == self.food:
                self.food = self.generate_food()
                self.score_label.config(text=f"得分: {len(self.snake) - 3}")
            else:
                self.snake.pop()

            # 绘制蛇和食物
            for segment in self.snake:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="black")
            self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")

            # 调用after方法实现定时更新
            self.master.after(100, self.game_loop)

    def show_game_over(self):
        # 游戏结束，显示最终得分并弹出对话框供玩家选择
        self.paused = True
        self.game_started = False  # 重置游戏开始标志
        final_score = len(self.snake) - 3

        # 创建一个顶层窗口用于显示游戏结束信息
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("游戏结束")
        game_over_window.geometry("250x200")  # 设置窗口大小
        game_over_window.transient(self.master)  # 使game_over_window成为master的临时窗口
        game_over_window.grab_set()  # 禁止用户访问其他窗口，直到game_over_window被关闭

        # 显示最终得分
        score_label = tk.Label(game_over_window, text=f"最终得分: {final_score}", font=("simhei", 16))
        score_label.pack(pady=20)

        # 定义重新开始游戏的函数
        def restart_game():
            game_over_window.destroy()  # 关闭game_over_window
            self.snake = [(100, 100), (100, 150), (100, 200)]
            self.direction = "Up"
            self.paused = False
            self.game_over = False
            self.score_label.config(text="得分: 0")
            self.food = self.generate_food()
            self.start_game()  # 重新开始游戏

        # 定义退出游戏的函数
        def quit_game():
            self.master.quit()  # 退出游戏

        # 创建重新开始和退出游戏的按钮
        restart_button = tk.Button(game_over_window, text="再玩一次", command=restart_game, width=10)
        restart_button.pack(side="left", padx=20)

        quit_button = tk.Button(game_over_window, text="退出游戏", command=quit_game, width=10)
        quit_button.pack(side="right", padx=20)

    def key_press(self, event):
        # 处理键盘事件，控制蛇的移动方向（但仅在游戏开始时才有效）
        if self.game_started:
            if event.keysym == "Up" and self.direction != "Down":
                self.direction = "Up"
            elif event.keysym == "Down" and self.direction != "Up":
                self.direction = "Down"
            elif event.keysym == "Left" and self.direction != "Right":
                self.direction = "Left"
            elif event.keysym == "Right" and self.direction != "Left":
                self.direction = "Right"
            elif event.keysym == "space":
                # 处理空格键事件，用于暂停/继续游戏
                if self.paused:
                    self.paused = False
                    self.game_loop()  # 恢复游戏循环
                else:
                    self.paused = True  # 暂停游戏

    # 处理空格键事件，用于暂停/继续游戏（与之前相同）
    # ...（省略了处理空格键事件的代码，与之前的示例相同）

    def bind_keys(self):
        # 绑定键盘事件（与之前相同）
        self.master.bind("<KeyPress>", self.key_press)

if __name__ == "__main__":
    # 创建主窗口并启动游戏（与之前相同）
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
