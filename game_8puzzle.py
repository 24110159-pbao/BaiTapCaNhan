import tkinter as tk
from tkinter import messagebox,ttk
from tkinter.scrolledtext import ScrolledText
import time

"""
    https://github.com/24110159-pbao/BaiTapCaNhan.git
    Rule1: nếu vị trí ô trống (0) có row > 0 thì có thể di chuyển lên trên (Up), bằng cách hoán đổi với ô ở index - 3
    Rule2: nếu vị trí ô trống (0) có row < 2 thì có thể di chuyển xuống dưới (Down), bằng cách hoán đổi với ô ở index + 3
    Rule3: nếu vị trí ô trống (0) có col > 0 thì có thể di chuyển sang trái (Left), bằng cách hoán đổi với ô ở index - 1
    Rule4: nếu vị trí ô trống (0) có col < 2 thì có thể di chuyển sang phải (Right), bằng cách hoán đổi với ô ở index + 1
    Rule5: trạng thái kết thúc khi:
            state == goal_state       
    P:
    Bài toán tìm đường đi trong 8-Puzzle từ initial_state đến goal_state bằng thuật toán BFS
    E:
    Không gian trạng thái gồm tất cả hoán vị hợp lệ của 8-Puzzle, mỗi trạng thái là một danh sách 1 chiều 9 phần tử hiển thị trên giao diện 3x3
    A:
    Các hành động hợp lệ được sinh động dựa trên vị trí của ô trống (0): Up, Down, Left, Right (nếu không vượt biên)
    S:
    Trạng thái mới được tạo bằng cách hoán đổi vị trí ô trống (0) với ô lân cận theo action tương ứng, sử dụng hàm result(state, action)
"""

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):

        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

class Problem:

    def __init__(self, initial_state, goal_state):

        self.initial = initial_state
        self.goal = goal_state



    def goal_test(self, state):

        return state == self.goal


    # tìm các hành động hợp lệ
    def actions(self, state):

        actions = []

        blank = state.index(0)

        row = blank // 3
        col = blank % 3

        if col > 0:
            actions.append("Left")

        if col < 2:
            actions.append("Right")

        if row > 0:
            actions.append("Up")


        if row < 2:
            actions.append("Down")

        return actions


    # tạo trạng thái mới
    def result(self, state, action):

        new_state = state.copy()

        blank = state.index(0)

        # xác định vị trí đổi chỗ
        if action == "Up":
            target = blank - 3

        elif action == "Down":
            target = blank + 3

        elif action == "Left":
            target = blank - 1

        elif action == "Right":
            target = blank + 1


        # đổi chỗ
        new_state[blank] = new_state[target]
        new_state[target] = 0

        return new_state



def CHILD_NODE(problem, parent, action):

    next_state = problem.result(parent.state, action)

    next_cost = parent.path_cost + 1

    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )

    return child


def print_solution(node):

    path = []

    while node != None:

        path.append(node)

        node = node.parent


    path.reverse()


    print("====== SOLUTION ======\n")

    for n in path:

        print("Action:", n.action)
        print("Cost:", n.path_cost)

        s = n.state

        print(s[0], s[1], s[2])
        print(s[3], s[4], s[5])
        print(s[6], s[7], s[8])

        print()




def deep_first_search(problem):

    # node gốc
    node = Node(problem.initial)


    if problem.goal_test(node.state):

        return node


    frontier = []
    frontier.append(node)

    explored  = []


    while len(frontier) > 0:


        node = frontier.pop(-1)# pop sẽ trả về giá trị của phần tử cuối cùng được xóa 
        explored.append(node.state)



        # sinh node con
        for action in problem.actions(node.state):

            child = CHILD_NODE(problem, node, action)# đưa node cha, action để tạo node con

            exist = False


            for e in explored:

                if e == child.state:
                    exist = True


            # kiểm tra frontier
            for f in frontier:

                if f.state == child.state:
                    exist = True


            
            if exist == False:
                # nếu chưa tồn tại nhưng đạt mục tiêu thì trả về node con, nếu chưa đạt mục tiêu thì thêm vào frontier để tiếp tục tìm kiếm
                if problem.goal_test(child.state):
                    return child
                else:
                    frontier.append(child)

    return None

def breadth_first_search(problem):

    # node gốc
    node = Node(problem.initial)


    if problem.goal_test(node.state):

        return node


    frontier = []
    frontier.append(node)

    explored  = []


    while len(frontier) > 0:


        node = frontier.pop(0)# pop sẽ trả về giá trị của phần tử được xóa đồng thời dồn các phần tử còn lại qua bên trái

        explored.append(node.state)



        # sinh node con
        for action in problem.actions(node.state):

            child = CHILD_NODE(problem, node, action)# đưa node cha, action để tạo node con

            exist = False


            for e in explored:

                if e == child.state:
                    exist = True


            # kiểm tra frontier
            for f in frontier:

                if f.state == child.state:
                    exist = True


            
            if exist == False:
                # nếu chưa tồn tại nhưng đạt mục tiêu thì trả về node con, nếu chưa đạt mục tiêu thì thêm vào frontier để tiếp tục tìm kiếm
                if problem.goal_test(child.state):
                    return child
                else:
                    frontier.append(child)
    return None

def is_cycle(node, state):

    while node is not None:

        if node.state == state:
            return True

        node = node.parent

    return False

def depth_limited_search(problem, limit):

    root = Node(problem.initial)

    frontier = [root]

    while len(frontier) > 0:

        node = frontier.pop(-1)

        # goal test
        if problem.goal_test(node.state):
            return node

        # chỉ expand nếu chưa vượt limit
        if node.path_cost < limit:

            actions = problem.actions(
                node.state
            )

            # vì để lấy như kiểu stack thì cần phải đảo ngược thì for action in actions mới thực thi như stack
            actions.reverse()

            for action in actions:

                child = CHILD_NODE(
                    problem,
                    node,
                    action
                )

                # chống cycle trên path
                if not is_cycle(node,child.state):
                    frontier.append(child)

    return None


def iterative_deepening_search(problem, max_depth=27):

    for limit in range(max_depth + 1):

        result = depth_limited_search(problem, limit)

        if result != None:
            return result

    return None


class PuzzleGUI:

    def __init__(self, root, solution_node, runtime):

        self.root = root
        self.root.title("8 Puzzle Visualizer")


        # MÀU SẮC
        self.BG_MAIN = "#1e1e2e"
        self.BG_BOARD = "#252538"

        self.BG_CELL = "#585b70"
        self.BG_CELL_ACTIVE = "#7027c9"

        self.TEXT_CELL = "#ffffff"

        self.BG_EMPTY = "#181825"

        self.BG_BTN = "#11111b"
        self.BG_BTN_HOVER = "#a6e3a1"

        self.TEXT_BTN = "#cdd6f4"


        # WINDOW
        self.root.configure(bg=self.BG_MAIN)
        self.root.resizable(False, False)


        # PATH
        self.path = self.get_solution_path(solution_node)

        self.current_index = 0


        # TOP FRAME
        self.top_frame = tk.Frame(
            root,
            bg=self.BG_MAIN
        )

        self.top_frame.pack(pady=10)

        algo_label = tk.Label(
            self.top_frame,
            text="Algorithm:",
            font=("Segoe UI", 11, "bold"),
            bg=self.BG_MAIN,
            fg="white"
        )

        algo_label.pack(
            side=tk.LEFT,
            padx=5
        )

        self.algo_combo = ttk.Combobox(
            self.top_frame,
            values=["BFS", "DFS", "IDS"],
            state="readonly",
            width=10,
            font=("Segoe UI", 11)
        )

        self.algo_combo.current(0)

        self.algo_combo.pack(
            side=tk.LEFT,
            padx=5
        )

        self.solve_button = tk.Button(
            self.top_frame,
            text="Solve",
            command=self.solve_selected_algorithm,
            font=("Segoe UI", 10, "bold"),
            bg="#89b4fa",
            fg="black",
            relief="flat",
            padx=10
        )

        self.solve_button.pack(
            side=tk.LEFT,
            padx=10
        )


        # INFO FRAME
        self.info_frame = tk.Frame(
            root,
            bg=self.BG_MAIN
        )

        self.info_frame.pack(pady=10)

        self.action_label = tk.Label(
            self.info_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            bg=self.BG_MAIN,
            fg="#f5e0dc"
        )

        self.action_label.pack(
            side=tk.LEFT,
            padx=15
        )

        self.cost_label = tk.Label(
            self.info_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            bg=self.BG_MAIN,
            fg="#f5e0dc"
        )

        self.cost_label.pack(
            side=tk.LEFT,
            padx=15
        )

        self.time_label = tk.Label(
            self.info_frame,
            text=f"Runtime: {runtime:.6f} s",
            font=("Segoe UI", 13, "bold"),
            bg=self.BG_MAIN,
            fg="#89dceb"
        )

        self.time_label.pack(
            side=tk.LEFT,
            padx=15
        )

        # =========================
        # MAIN CONTENT
        # =========================
        self.main_frame = tk.Frame(
            root,
            bg=self.BG_MAIN
        )

        self.main_frame.pack(pady=10)

        # =========================
        # BOARD FRAME
        # =========================
        self.board_frame = tk.Frame(
            self.main_frame,
            bg=self.BG_BOARD,
            padx=10,
            pady=10
        )

        self.board_frame.pack(
            side=tk.LEFT,
            padx=15
        )

        self.cells = []

        for i in range(3):

            row = []

            for j in range(3):

                label = tk.Label(
                    self.board_frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Segoe UI", 26, "bold"),
                    fg=self.TEXT_CELL,
                    borderwidth=0,
                    relief="flat"
                )

                label.grid(
                    row=i,
                    column=j,
                    padx=6,
                    pady=6
                )

                row.append(label)

            self.cells.append(row)

        # LOG FRAME
        self.log_frame = tk.Frame(
            self.main_frame,
            bg=self.BG_MAIN
        )

        self.log_frame.pack(
            side=tk.LEFT,
            padx=10
        )

        self.log_text = ScrolledText(
            self.log_frame,
            width=35,
            height=18,
            font=("Consolas", 11),
            bg="#11111b",
            fg="#a6e3a1",
            insertbackground="white"
        )

        self.log_text.pack()

        # BUTTON FRAME
        self.control_frame = tk.Frame(
            root,
            bg=self.BG_MAIN
        )

        self.control_frame.pack(pady=20)

        btn_config = {

            "font": ("Segoe UI", 11, "bold"),

            "fg": self.TEXT_BTN,

            "bg": self.BG_BTN,

            "activebackground": self.BG_BOARD,

            "activeforeground": "#ffffff",

            "relief": "flat",

            "width": 11,

            "bd": 0,

            "cursor": "hand2",

            "pady": 6
        }

        self.reload_button = tk.Button(
            self.control_frame,
            text="Reload",
            command=self.reload,
            **btn_config
        )

        self.reload_button.pack(
            side=tk.LEFT,
            padx=8
        )

        self.next_button = tk.Button(
            self.control_frame,
            text="Next Step",
            command=self.next_step,
            **btn_config
        )

        self.next_button.pack(
            side=tk.LEFT,
            padx=8
        )

        self.auto_button = tk.Button(
            self.control_frame,
            text="Auto Run",
            command=self.auto_run,
            **btn_config
        )

        self.auto_button.pack(
            side=tk.LEFT,
            padx=8
        )


        # HOVER BUTTON
        for btn in [

            self.reload_button,
            self.next_button,
            self.auto_button

        ]:

            btn.bind(

                "<Enter>",

                lambda e, b=btn:
                b.config(
                    bg=self.BG_BOARD,
                    fg=self.BG_BTN_HOVER
                )
            )

            btn.bind(

                "<Leave>",

                lambda e, b=btn:
                b.config(
                    bg=self.BG_BTN,
                    fg=self.TEXT_BTN
                )
            )


        # SHOW INITIAL
        self.show_state()
        self.show_log()


    # LẤY ĐƯỜNG ĐI
    def get_solution_path(self, node):

        path = []

        while node is not None:

            path.append(node)

            node = node.parent

        path.reverse()

        return path


    # HIỂN THỊ STATE
    def show_state(self):

        node = self.path[self.current_index]

        state = node.state

        for i in range(9):

            row = i // 3
            col = i % 3

            value = state[i]

            if value == 0:

                self.cells[row][col].config(

                    text="",

                    bg=self.BG_EMPTY
                )

            else:

                self.cells[row][col].config(

                    text=str(value),

                    bg=self.BG_CELL_ACTIVE
                    if value % 2 == 0
                    else self.BG_CELL
                )

        action_text = node.action if node.action else "Start"

        self.action_label.config(
            text=f"Action: {action_text}"
        )

        self.cost_label.config(
            text=f"Cost: {node.path_cost}"
        )


    # HIỂN THỊ LOG
    def show_log(self):

        self.log_text.delete(1.0, tk.END)

        self.log_text.insert(
            tk.END,
            "====== SOLUTION ======\n\n"
        )

        for node in self.path:

            self.log_text.insert(
                tk.END,
                f"Action: {node.action}\n"
            )

            self.log_text.insert(
                tk.END,
                f"Cost: {node.path_cost}\n"
            )

            s = node.state

            self.log_text.insert(
                tk.END,
                f"{s[0]} {s[1]} {s[2]}\n"
            )

            self.log_text.insert(
                tk.END,
                f"{s[3]} {s[4]} {s[5]}\n"
            )

            self.log_text.insert(
                tk.END,
                f"{s[6]} {s[7]} {s[8]}\n"
            )

            self.log_text.insert(
                tk.END,
                "\n"
            )

    # CHỌN THUẬT TOÁN
    def solve_selected_algorithm(self):

        selected = self.algo_combo.get()

        problem = Problem(
            initial_state,
            goal_state
        )

        start_time = time.time()

        if selected == "BFS":

            result = breadth_first_search(problem)

        elif selected == "DFS":

            result = deep_first_search(problem)

        elif selected == "IDS":

            result = iterative_deepening_search(problem)

        end_time = time.time()

        runtime = end_time - start_time

        self.time_label.config(
            text=f"Runtime: {runtime:.6f} s"
        )

        if result:

            self.path = self.get_solution_path(result)

            self.current_index = 0

            self.show_state()

            self.show_log()

    # NEXT STEP
    def next_step(self):

        if self.current_index < len(self.path) - 1:

            self.current_index += 1

            self.show_state()

        else:

            messagebox.showinfo(
                "Finished",
                "Đã tới trạng thái đích!"
            )


    # AUTO RUN
    def auto_run(self):

        if self.current_index < len(self.path) - 1:

            self.current_index += 1

            self.show_state()

            self.root.after(
                800,
                self.auto_run
            )


    # RELOAD
    def reload(self):

        self.current_index = 0

        self.show_state()



# MAIN
initial_state = [
    1, 2, 3,
    4, 0, 6,
    7, 5, 8
]

goal_state = [
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
]

problem = Problem(
    initial_state,
    goal_state
)

# đo thời gian chạy DFS
start_time = time.time()

result = deep_first_search(problem)

end_time = time.time()

runtime = end_time - start_time

if result != None:

    print_solution(result)

    root = tk.Tk()

    gui = PuzzleGUI(
        root,
        result,
        runtime
    )

    root.mainloop()

else:

    print("No solution")