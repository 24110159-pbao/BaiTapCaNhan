from platform import node
import random
import tkinter as tk
from tkinter import messagebox,ttk
from tkinter.scrolledtext import ScrolledText
import time
import math
from collections import deque
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
search_log = []# lưu các suy nghĩ của thuật toán để hiển thị trên giao diện
MAX_LOG = 200# để giới hạn số lượng log hiển thị trên giao diện, tránh bị quá tải khi thuật toán sinh ra quá nhiều log

def add_log(text):
    if len(search_log) < MAX_LOG:
        search_log.append(text)

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



def CHILD_NODE(problem, parent, action):#cho deeo_first_search, breadth_first_search, depth_limited_search

    next_state = problem.result(parent.state, action)

    next_cost = parent.path_cost + 1

    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child



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
        add_log( f"\nEXPAND: {node.state}" )
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
        add_log( f"\nEXPAND: {node.state}" )
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

# IDS và IDA* 
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
        add_log( f"\nEXPAND: {node.state}" )
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

#cho UCS, Greedy, A*,IDA* để tính số ô sai so với goal_state để làm chi phí di chuyển
def KiemTraSoOSai(initial_state,goal_state):
    count = 0

    for i in range(9):
        if initial_state[i] != goal_state[i]:
            count += 1

    return count

def sort_frontier(frontier, node): #cho UCS, Greedy, A* để sắp xếp frontier theo path_cost

    for i in range(len(frontier)):

        if frontier[i].state == node.state:

            if node.path_cost < frontier[i].path_cost:

                frontier[i] = node

            frontier.sort(key=lambda x: x.path_cost)
            return

    frontier.append(node)

    frontier.sort(key=lambda x: x.path_cost)



def CHILD_NODE_UCS(problem, parent, action):

    next_state = problem.result(parent.state, action)
    so_osai = KiemTraSoOSai(next_state, problem.goal)
    next_cost = parent.path_cost + so_osai

    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child

def UCS(problem):

    # node gốc
    node = Node(problem.initial)


    if problem.goal_test(node.state):

        return node


    frontier = []
    frontier.append(node)

    reached = []


    while len(frontier) > 0:

        

        node = frontier.pop(0)  # pop sẽ trả về giá trị của phần tử được xóa đồng thời dồn các phần tử còn lại qua bên trái
        add_log( f"\nEXPAND: {node.state}" )
        reached.append(node.state)

        # kiểm tra goal trước khi tạo con
        if problem.goal_test(node.state):

            return node


        # sinh node con
        for action in problem.actions(node.state):

            child = CHILD_NODE_UCS(problem, node, action)

            exist = False


            for r in reached:

                if r == child.state:
                    exist = True
                    break


            # nếu chưa tồn tại
            if exist == False:

                sort_frontier(frontier, child)


    return None



def CHILD_NODE_GREEDY(problem, parent, action):

    next_state = problem.result(parent.state, action)
    so_osai = KiemTraSoOSai(next_state, problem.goal)
    next_cost = so_osai

    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child

def GREEDY(problem):

    node = Node(problem.initial)

    if problem.goal_test(node.state):

        return node

    frontier = []
    frontier.append(node)


    reached = []

    while len(frontier) > 0:

        node = frontier.pop(0)
        add_log( f"\nEXPAND: {node.state}" )
        reached.append(node.state)

        if problem.goal_test(node.state):

            return node

        for action in problem.actions(node.state):

            child = CHILD_NODE_GREEDY(problem, node, action)

            exist = False

            for r in reached:

                if r == child.state:

                    exist = True
                    break

            if exist == False:

                sort_frontier(frontier, child)

    return None



def mahatan_distance(state, goal):#cho A* và IDA* 

    distance = 0

    for i in range(1, 9):

        index_state = state.index(i)
        index_goal = goal.index(i)

        row_state = index_state // 3
        col_state = index_state % 3

        row_goal = index_goal // 3
        col_goal = index_goal % 3

        distance += abs(row_state - row_goal) + abs(col_state - col_goal)

    return distance

def CHILD_NODE_A_sao(problem, parent, action):

    next_state = problem.result(parent.state, action)
    so_osai = KiemTraSoOSai(next_state, problem.goal)
    h_cost_parent = mahatan_distance(parent.state, problem.goal)
    h_cost= mahatan_distance(next_state, problem.goal)

    next_cost = parent.path_cost - h_cost_parent + so_osai + h_cost# trừ đi h(node cha) cộng g(node con) cộng h(node con)
    # mục đích để ko cộng dồn h(n)
    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child

def A_sao(problem):

    # node gốc
    node = Node(problem.initial)
    node.path_cost = mahatan_distance(node.state, problem.goal) 
    if problem.goal_test(node.state):

        return node


    frontier = []
    frontier.append(node)

    reached = []


    while len(frontier) > 0:

        

        node = frontier.pop(0)  # pop sẽ trả về giá trị của phần tử được xóa đồng thời dồn các phần tử còn lại qua bên trái
        add_log( f"\nEXPAND: {node.state}" )
        reached.append(node.state)

        # kiểm tra goal trước khi tạo con
        if problem.goal_test(node.state):

            return node


        # sinh node con
        for action in problem.actions(node.state):

            child = CHILD_NODE_A_sao(problem, node, action)

            exist = False


            for r in reached:

                if r == child.state:
                    exist = True
                    break


            # nếu chưa tồn tại
            if exist == False:

                sort_frontier(frontier, child)


    return None

def CHILD_NODE_IDA_sao(problem, parent, action):

    next_state = problem.result(parent.state, action)
    so_osai = KiemTraSoOSai(next_state, problem.goal)
    h_cost_parent = mahatan_distance(parent.state, problem.goal)
    h_cost= mahatan_distance(next_state, problem.goal)

    next_cost = parent.path_cost - h_cost_parent + so_osai + h_cost# trừ đi h(node cha) cộng g(node con) cộng h(node con)
    # mục đích để ko cộng dồn h(n)
    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child

def depth_limited_IDA(problem, limit):

    root = Node(problem.initial)
    
    root.path_cost = mahatan_distance(
        root.state,
        problem.goal
    )

    frontier = [root]

    next_limit = float('inf')

    while len(frontier) > 0:

        node = frontier.pop(-1)

        add_log(
            f"\nEXPAND: {node.state}"
        )

        # goal test
        if problem.goal_test(node.state):
            return node, next_limit

        # nếu vượt ngưỡng
        if node.path_cost > limit:

            next_limit = min(next_limit,node.path_cost)

            continue

        actions = list(
            problem.actions(node.state)
        )

        actions.reverse()

        for action in actions:

            child = CHILD_NODE_IDA_sao(
                problem,
                node,
                action
            )

            # chống cycle
            if not is_cycle(node, child.state):
                frontier.append(child)

    return None, next_limit


def IDA_sao(problem):

    # limit ban đầu = h(root)
    limit = mahatan_distance(
        problem.initial,
        problem.goal
    )

    while True:

        result, new_limit = depth_limited_IDA(
            problem,
            limit
        )

        if result is not None:
            return result

        # không còn node nào
        if new_limit == float('inf'):
            return None

        # tăng ngưỡng
        limit = new_limit


def Child_Node_Simple_Hill_Climbing(problem, parent, action):
    next_state = problem.result(parent.state, action)
    mahatan = mahatan_distance(next_state, problem.goal)
    next_cost = mahatan 

    child = Node(
        next_state,
        parent,
        action,
        next_cost
    )
    add_log( f"Generate {action} -> {child.state}" )
    return child

def Simple_Hill_Climbing(problem):
    node  = Node(problem.initial)
    node.path_cost = mahatan_distance(node.state, problem.goal)

    while True:
        add_log( f"\nEXPAND: {node.state}" )
        check_neighbor = False
        for action in problem.actions(node.state):
            child = Child_Node_Simple_Hill_Climbing(problem, node, action)
            if child.path_cost < node.path_cost:
                node = child
                check_neighbor = True
                break
        if check_neighbor == False:
            break

    return node           


def Best_Simple_Hill_Climbing(problem):
    node  = Node(problem.initial)
    node.path_cost = mahatan_distance(node.state, problem.goal)

    while True:
        add_log( f"\nEXPAND: {node.state}" )
        neighbors  = []
        for action in problem.actions(node.state):
            child = Child_Node_Simple_Hill_Climbing(problem, node, action)
            if child.path_cost < node.path_cost:
                neighbors .append(child)

        #sẽ sắp xếp tăng dần theo path_cost
        neighbors .sort(key=lambda x: x.path_cost)

        if len(neighbors ) > 0:
            node = neighbors [0]           
        else:
            break
    return node

def Stochastic_Hill_Climbing(problem):
    node  = Node(problem.initial)
    node.path_cost = mahatan_distance(node.state, problem.goal)
    
    while True:
        add_log( f"\nEXPAND: {node.state}" )
        if problem.goal_test(node.state):
            return node
        neighbors  = []
        for action in problem.actions(node.state):
            child = Child_Node_Simple_Hill_Climbing(problem, node, action)
            if child.path_cost < node.path_cost:
                neighbors .append(child)

        if len(neighbors ) > 0:
            node = random.choice(neighbors )    
        else:
            print("No more neighbors to explore.")
            break
    return node

def Random_Restart_Hill_Climbing(problem):
    for i in range(100):
        node  = Node(problem.initial)
        node.path_cost = mahatan_distance(node.state, problem.goal)
        while True:
            add_log( f"\nEXPAND: {node.state}" )
            if problem.goal_test(node.state):
                return node
            neighbors  = []
            for action in problem.actions(node.state):
                child = Child_Node_Simple_Hill_Climbing(problem, node, action)
                if child.path_cost < node.path_cost:
                    neighbors .append(child)

            if len(neighbors ) > 0:
                node = random.choice(neighbors )    
            else:
                print("No more neighbors to explore.")
                break
    return None

def Local_Beem_Search(problem, k=3):

    current_states = [Node(problem.initial)]

    current_states[0].path_cost = mahatan_distance(
        current_states[0].state,
        problem.goal
    )

    while True:

        neighbor_states = []

        for node in current_states:

            add_log(
                f"\nEXPAND: {node.state}"
            )

            if problem.goal_test(node.state):
                return node

            for action in problem.actions(node.state):

                child = Child_Node_Simple_Hill_Climbing(
                    problem,
                    node,
                    action
                )

                neighbor_states.append(child)

        if len(neighbor_states) == 0:

            current_states.sort(
                key=lambda x: x.path_cost
            )

            return current_states[0]

        # kiểm tra goal
        for node in neighbor_states:

            if problem.goal_test(node.state):
                return node

        # lấy k trạng thái tốt nhất
        neighbor_states.sort(
            key=lambda x: x.path_cost
        )

        current_states = neighbor_states[:k]


def CHILD_NODE_SA(problem, parent, action):

    next_state = problem.result(parent.state, action)

    child = Node(
        next_state,
        parent,
        action,
        parent.path_cost + 1
    )

    add_log(
        f"Generate {action} -> {child.state}"
    )

    return child    

def Simulated_Annealing(problem,T0=100,Tmin=0,alpha=0.96):
        
    current = Node(problem.initial)

    T = T0

    while T > Tmin:

        add_log(
            f"\nEXPAND: {current.state} | T={T}"
        )

        if problem.goal_test(current.state):
            return current

        actions = problem.actions(current.state)

        if len(actions) == 0:
            break

        # chọn ngẫu nhiên 1 hàng xóm
        action = random.choice(actions)

        next_node = CHILD_NODE_SA(
            problem,
            current,
            action
        )

        current_h = mahatan_distance(
            current.state,
            problem.goal
        )

        next_h = mahatan_distance(
            next_node.state,
            problem.goal
        )

        delta = next_h - current_h

        # tốt hơn => nhận luôn
        if delta < 0:

            current = next_node

            add_log(
                f"Accept better state h={next_h}"
            )

        else:

            p = math.exp(-delta / T)

            r = random.random()

            add_log(
                f"Worse state: p={p:.4f}, r={r:.4f}"
            )

            if r < p:

                current = next_node

                add_log(
                    "Accepted worse state"
                )

        T = int(alpha * T)

    return current



def random_state_from_goal(goal, moves=15):

    state = goal.copy()

    temp_problem = Problem(state, goal)

    for _ in range(moves):

        actions = temp_problem.actions(state)

        action = random.choice(actions)

        state = temp_problem.result(
            state,
            action
        )

    return state

def belief_goal_test(problem, states):

    return (
        problem.goal_test(states[0])
        and
        problem.goal_test(states[1])
    )


def BELIEF_CHILD_NODE(
        problem,
        parent,
        action):

    new_states = []

    for state in parent.state:

        # nếu đã goal thì giữ nguyên
        if problem.goal_test(state):

            next_state = state.copy()

        # nếu action hợp lệ
        elif action in problem.actions(state):

            next_state = problem.result(
                state,
                action
            )

        # nếu action không hợp lệ
        else:

            next_state = state.copy()

        new_states.append(next_state)

    child = Node(
        new_states,
        parent,
        action,
        parent.path_cost + 1
    )

    add_log(
        f"Generate {action}"
    )

    add_log(
        f"S1={new_states[0]}"
    )

    add_log(
        f"S2={new_states[1]}"
    )

    return child

def Belief_State_BFS(
        problem,
        state1,
        state2):

    root = Node(
        [state1, state2]
    )

    frontier = deque([root])

    explored = set()

    while frontier:

        node = frontier.popleft()

        key = tuple(    
            sorted([
                tuple(node.state[0]),
                tuple(node.state[1])
            ])
        )

        if key in explored:
            continue

        explored.add(key)

        add_log(
            "\nEXPAND:"
        )

        add_log(
            f"S1={node.state[0]}"
        )

        add_log(
            f"S2={node.state[1]}"
        )

        if belief_goal_test(
            problem,
            node.state
        ):
            return node

        for action in [
            "Up",
            "Down",
            "Left",
            "Right"
        ]:

            child = BELIEF_CHILD_NODE(
                problem,
                node,
                action
            )

            child_key = tuple(    
                sorted([
                    tuple(child.state[0]),
                    tuple(child.state[1])
                ])
            )

            if child_key not in explored:

                frontier.append(child)

    return None

def random_goal_pair():

    goal1 = random_state_from_goal(
        goal_state,
        5
    )

    goal2 = random_state_from_goal(
        goal_state,
        10
    )

    while goal1 == goal2:

        goal2 = random_state_from_goal(
            goal_state,
            10
        )

    return goal1, goal2

def belief_multi_goal_test(
        states,
        goal1,
        goal2):

    s1 = states[0]
    s2 = states[1]

    return (

        s1 == s2

        and

        (
            s1 == goal1
            or
            s1 == goal2
        )

    )

MAX_DEPTH = 20
def Belief_State_BFS_MultiGoal(
        problem,
        state1,
        state2,
        goal1,
        goal2):

    root = Node(
        [state1, state2]
    )

    frontier = deque([root])

    explored = set()

    while frontier:
        

        node = frontier.popleft()

        if node.path_cost >= MAX_DEPTH:
            continue

        s1 = tuple(node.state[0])
        s2 = tuple(node.state[1])

        if s1 < s2:
            key = (s1,s2)
        else:
            key = (s2,s1)

        if key in explored:
            continue

        explored.add(key)

        add_log(
            "\nEXPAND:"
        )

        add_log(
            f"S1={node.state[0]}"
        )

        add_log(
            f"S2={node.state[1]}"
        )

        # GOAL TEST MỚI
        if belief_multi_goal_test(
                node.state,
                goal1,
                goal2):

            return node

        for action in [
            "Up",
            "Down",
            "Left",
            "Right"
        ]:

            child = BELIEF_CHILD_NODE(
                problem,
                node,
                action
            )

            child_key = (
                tuple(child.state[0]),
                tuple(child.state[1])
            )

            if child_key not in explored:

                frontier.append(child)

    return None

def random_state_with_fixed_7(goal,moves=20):

    while True:

        state = random_state_from_goal(
            goal,
            moves
        )

        if state[6] == 7:
            return state
#thuật toán mới 1 bảng, bằng backtracking
def constraint_test(index):
    goal = [
        1,2,3,
        4,5,6,
        7,8,0
    ]
    return goal[index]

def Backtracking(state, index=0, used=None):


    if used is None:
        used = set()

    if index == 9:

        add_log(f"GOAL FOUND {state}")
        return state.copy()

    candidates = [x for x in range(9) if x not in used]

    random.shuffle(candidates)

    for value in candidates:

        add_log(
            f"Try coordinate=({index//3}, {index%3}) value={value}"
        )

        if value != constraint_test(index):

            add_log(
                f"Reject value={value}"
            )

            continue

        state[index] = value
        used.add(value)

        add_log(
            f"Accept -> {state.copy()}"
        )

        result = Backtracking(
            state,
            index + 1,
            used
        )

        if result is not None:
            return result

        state[index] = 0
        used.remove(value)

    return None
#thuật toán and or search 
MAX_ANDOR_DEPTH =4
def nondeterministic_results(problem, state, action):

    results = []

    main_state = problem.result(state, action)
    results.append(main_state)

    actions = problem.actions(main_state)

    count = 0

    for a in actions:

        if count >= 2:
            break

        s = problem.result(main_state, a)

        if s not in results:
            results.append(s)
            count += 1

    return results

def OR_SEARCH(problem,
              state,
              parent,
              path,
              depth):

    add_log(
        f"\nOR depth={depth}: {state}"
    )

    if problem.goal_test(state):

        add_log(
            "SUCCESS (goal)"
        )

        return Node(
            state,
            parent
        )

    if depth >= MAX_ANDOR_DEPTH:

        add_log(
            "FAILURE (depth)"
        )

        return None

    if state in path:

        add_log(
            "FAILURE (cycle)"
        )

        return None
    actions = problem.actions(state)

    priority = [
        "Down",
        "Right",
        "Left",
        "Up"
    ]

    actions.sort(
        key=lambda x: priority.index(x)
    )
    for action in actions:

        add_log(
            f"Try Action {action}"
        )

        result_states = nondeterministic_results(
            problem,
            state,
            action
        )

        plan = AND_SEARCH(
            problem,
            result_states,
            Node(state,parent,action),
            path + [state],
            depth + 1
        )

        if plan is not None:

            add_log(
                f"Action {action} ACCEPTED"
            )

            return plan

        add_log(
            f"Action {action} REJECTED"
        )

    return None

def AND_SEARCH(problem,
               states,
               parent,
               path,
               depth):

    add_log(
        f"AND depth={depth}"
    )

    success_node = None

    for i, s in enumerate(states):

        add_log(
            f"Check S{i+1}: {s}"
        )

        result = OR_SEARCH(
            problem,
            s,
            parent,
            path,
            depth
        )

        if result is None:

            add_log(
                f"S{i+1} -> FAILURE"
            )

            return None

        add_log(
            f"S{i+1} -> SUCCESS"
        )

        success_node = result

    return success_node

def AND_OR_GRAPH_SEARCH(problem):

    search_log.clear()
    
    add_log(
        
        "===== AND OR SEARCH ====="
    )

    root = Node(
        problem.initial
    )

    result = OR_SEARCH(
        problem,
        problem.initial,
        None,
        [],
        0
    )

    return result

#thuật toán ac-3
from collections import deque

def AC3():

    add_log(
        "\n===== AC3 START ====="
    )

    goal = [
        1,2,3,
        4,5,6,
        7,8,0
    ]

    # DOMAIN BAN ĐẦU
    domains = {}

    for i in range(9):

        domains[i] = list(range(9))

        add_log(
            f"D(X{i}) = {domains[i]}"
        )

    add_log("")

    # ÁP RÀNG BUỘC Xi = goal[i]
    for fixed_var in range(9):

        add_log(
            f"\nPROCESS X{fixed_var}"
        )

        add_log(
            f"Constraint: X{fixed_var} = {goal[fixed_var]}"
        )

        domains[fixed_var] = [goal[fixed_var]]

        add_log(
            f"D(X{fixed_var}) = {domains[fixed_var]}"
        )

        fixed_value = goal[fixed_var]

        for other in range(9):

            if other == fixed_var:
                continue

            add_log(
                f"\nREVISE(X{other}, X{fixed_var})"
            )

            if fixed_value in domains[other]:

                domains[other].remove(
                    fixed_value
                )

                add_log(
                    f"Remove {fixed_value} from X{other}"
                )

                add_log(
                    f"D(X{other}) = {domains[other]}"
                )

                if len(domains[other]) == 0:

                    add_log(
                        "FAILURE: Empty Domain"
                    )

                    return None
    add_log(
        "\n===== FINAL DOMAINS ====="
    )

    result = []

    for i in range(9):

        add_log(
            f"X{i} -> {domains[i]}"
        )

        result.append(
            domains[i][0]
        )

    add_log(
        f"\nAC3 RESULT = {result}"
    )

    return result
#min-conflicts
def count_conflicts(state, goal):

    conflicts = 0

    # Constraint 1:
    # Xi phải bằng goal[i]

    for i in range(9):

        if state[i] != goal[i]:

            conflicts += 1

    # Constraint 2:
    # AllDifferent

    for i in range(9):

        for j in range(i + 1, 9):

            if state[i] == state[j]:

                conflicts += 1

    return conflicts
def conflicted_variables(state, goal):

    vars = []

    for i in range(9):

        conflict = False

        # sai goal
        if state[i] != goal[i]:

            conflict = True

        # trùng giá trị
        for j in range(9):

            if i != j and state[i] == state[j]:

                conflict = True

        if conflict:

            vars.append(i)

    return vars
def Min_Conflicts(problem, max_steps=200):

    add_log(
        "\n===== MIN CONFLICTS ====="
    )

    # ----------------------
    # Random Initial State
    # ----------------------

    current = [random.randint(0,8)
               for _ in range(9)]

    add_log(
        f"\nInitial State:"
    )

    add_log(
        str(current)
    )

    for step in range(max_steps):

        add_log(
            f"\n===== STEP {step+1} ====="
        )

        current_conflicts = count_conflicts(
            current,
            problem.goal
        )

        add_log(
            f"Total Conflicts = {current_conflicts}"
        )

        # GOAL
        if current_conflicts == 0:

            add_log(
                "\nGOAL FOUND"
            )

            return Node(current)

        # ----------------------
        # Chọn biến lỗi ngẫu nhiên
        # ----------------------

        conflict_vars = conflicted_variables(
            current,
            problem.goal
        )

        var = random.choice(
            conflict_vars
        )

        add_log(
            f"Choose Variable X{var}"
        )

        best_values = []

        best_conflict = float('inf')

        # ----------------------
        # Thử mọi giá trị
        # ----------------------

        for value in range(9):
            if value == current[var]:
                continue


            temp = current.copy()

            temp[var] = value

            c = count_conflicts(
                temp,
                problem.goal
            )

            add_log(
                f"Try X{var}={value} -> conflicts={c}"
            )

            if c < best_conflict:

                best_conflict = c

                best_values = [value]

            elif c == best_conflict:

                best_values.append(
                    value
                )

        chosen_value = random.choice(
            best_values
        )

        add_log(
            f"Best Conflict = {best_conflict}"
        )

        add_log(
            f"Assign X{var}={chosen_value}"
        )

        current[var] = chosen_value

        add_log(
            f"State = {current}"
        )

    add_log(
        "\nFAILURE"
    )

    return None

class PuzzleGUI:

    def __init__(self, root, solution_node, runtime, goal1=None, goal2=None):

        self.goal1 = goal1
        self.goal2 = goal2

        self.is_belief = False
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
            values=["BFS", 
                    "DFS", 
                    "IDS", 
                    "UCS",
                    "GREEDY",
                    "A*",
                    "IDA*",
                    "Simple Hill Climbing",
                    "Best Simple Hill Climbing",
                    "Stochastic Hill Climbing",
                    "Random Restart Hill Climbing",
                    "Local Beam Search",
                    "Simulated Annealing",
                    "Belief State BFS",
                    "Multi-Goal Belief State BFS",
                    "7 Multi-Goal Belief State BFS",
                    "Backtracking",
                    "AND-OR Search",
                    "AC-3",
                    "Min-Conflicts"
                    ],
                    
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
        self.board_frame2 = tk.Frame(
            self.main_frame,
            bg=self.BG_BOARD,
            padx=10,
            pady=10
        )

        self.cells2 = []

        for i in range(3):

            row = []

            for j in range(3):

                label = tk.Label(
                    self.board_frame2,
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

            self.cells2.append(row)

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


        # =========================
        # SEARCH PROCESS FRAME
        # =========================
        # FINAL PATH FRAME


        self.path_frame = tk.Frame(
            self.main_frame,
            bg=self.BG_MAIN
        )

        self.path_frame.pack(
            side=tk.LEFT,
            padx=10
        )

        self.path_title = tk.Label(
            self.path_frame,
            text="Final Path",
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_MAIN,
            fg="#94e2d5"
        )

        self.path_title.pack(pady=5)

        self.path_text = ScrolledText(
            self.path_frame,
            width=35,
            height=20,
            font=("Consolas", 10),
            bg="#11111b",
            fg="#f38ba8"
        )

        self.path_text.pack()

        self.log_frame = tk.Frame(
            self.main_frame,
            bg=self.BG_MAIN
        )

        self.log_frame.pack(
            side=tk.LEFT,
            padx=10
        )

        self.log_title = tk.Label(
            self.log_frame,
            text="Search Process",
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_MAIN,
            fg="#f9e2af"
        )

        self.log_title.pack(pady=5)

        self.log_text = ScrolledText(
            self.log_frame,
            width=45,
            height=20,
            font=("Consolas", 10),
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
        self.show_final_path()


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
  
        # ======================
        # NORMAL MODE (1 BOARD)
        # ======================
        if not self.is_belief:

            state = node.state

            for i in range(9):
                r, c = divmod(i, 3)
                val = state[i]

                if val == 0:
                    self.cells[r][c].config(text="", bg=self.BG_EMPTY)
                else:
                    self.cells[r][c].config(
                        text=str(val),
                        bg=self.BG_CELL_ACTIVE if val % 2 == 0 else self.BG_CELL
                    )

            self.board_frame2.pack_forget()

        # ======================
        # BELIEF MODE (2 BOARDS)
        # ======================
        else:

            state1, state2 = node.state

            if not self.board_frame2.winfo_ismapped():

                self.board_frame2.pack(
                    side=tk.LEFT,
                    padx=15
                )

            # BOARD 1
            for i in range(9):
                r, c = divmod(i, 3)
                val = state1[i]

                if val == 0:
                    self.cells[r][c].config(text="", bg=self.BG_EMPTY)
                else:
                    self.cells[r][c].config(
                        text=str(val),
                        bg=self.BG_CELL_ACTIVE if val % 2 == 0 else self.BG_CELL
                    )

            # BOARD 2
            for i in range(9):
                r, c = divmod(i, 3)
                val = state2[i]

                if val == 0:
                    self.cells2[r][c].config(text="", bg=self.BG_EMPTY)
                else:
                    self.cells2[r][c].config(
                        text=str(val),
                        bg=self.BG_CELL
                    )

        # ======================
        # INFO UPDATE
        # ======================
        self.action_label.config(
            text=f"Action: {node.action if node.action else 'Start'}"
        )

        self.cost_label.config(
            text=f"Cost: {node.path_cost}"
        )

    # HIỂN THỊ LOG

    def show_log(self):
        

        global search_log
        

        self.log_text.delete(
            1.0,
            tk.END
        )

        self.log_text.insert(
            tk.END,
            "====== SEARCH PROCESS ======\n\n"
        )

        for log in search_log:

            self.log_text.insert(
                tk.END,
                log + "\n"
            )

        self.log_text.see(tk.END)



    # CHỌN THUẬT TOÁN
    def solve_selected_algorithm(self):

        global search_log

        search_log.clear()

        selected = self.algo_combo.get()

        if selected in [
            "Belief State BFS",
            "Multi-Goal Belief State BFS",
            "7 Multi-Goal Belief State BFS"
        ]:
            self.is_belief = True
            self.board_frame2.pack(
                    side=tk.LEFT,
                    padx=15
                )
        else:
            self.is_belief = False
            self.board_frame2.pack_forget()

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

        elif selected == "UCS":

            result = UCS(problem)

        elif selected == "GREEDY":

            result = GREEDY(problem)

        elif selected == "A*":

            result = A_sao(problem)

        elif selected == "IDA*":

            result = IDA_sao(problem)

        elif selected == "Simple Hill Climbing":

            result = Simple_Hill_Climbing(problem)

        elif selected == "Best Simple Hill Climbing":

            result = Best_Simple_Hill_Climbing(problem)

        elif selected == "Stochastic Hill Climbing":

            result = Stochastic_Hill_Climbing(problem)

        elif selected == "Random Restart Hill Climbing":

            result = Random_Restart_Hill_Climbing(problem)

        elif selected == "Local Beam Search":

            result = Local_Beem_Search(problem)

        elif selected == "Simulated Annealing":

            result = Simulated_Annealing(problem)

        elif selected == "Belief State BFS":

            state1 = random_state_from_goal(
                goal_state,
                10
            )

            state2 = random_state_from_goal(
                goal_state,
                15
            )

            result = Belief_State_BFS(
                problem,
                state1,
                state2
            )
        elif selected == "Multi-Goal Belief State BFS":
            
            state1 = random_state_from_goal(
                goal_state,
                10
            )

            state2 = random_state_from_goal(
                goal_state,
                15
            )

            goal1, goal2 = random_goal_pair()
            
            add_log(
                "\n========== GOALS =========="
            )

            add_log(
                f"Goal1={goal1}"
            )

            add_log(
                f"Goal2={goal2}"
            )

            result = Belief_State_BFS_MultiGoal(
                problem,
                state1,
                state2,
                goal1,
                goal2
            )
        elif selected == "7 Multi-Goal Belief State BFS":
            
            state1 = random_state_with_fixed_7(
                goal_state,
                20
            )

            state2 = random_state_with_fixed_7(
                goal_state,
                30
            )

            while state1 == state2:
                state2 = random_state_with_fixed_7(
                    goal_state,
                    30
                )

            goal1, goal2 = random_goal_pair()
            
            add_log(
                "\n========== GOALS =========="
            )

            add_log(
                f"Goal1={goal1}"
            )

            add_log(
                f"Goal2={goal2}"
            )

            result = Belief_State_BFS_MultiGoal(
                problem,
                state1,
                state2,
                goal1,
                goal2
            )
        elif selected == "Backtracking":

            init_state = [0] * 9

            final_state = Backtracking(init_state)

            if final_state:
                result = Node(final_state)
            else:
                result = None
        elif selected == "AND-OR Search":

            result = AND_OR_GRAPH_SEARCH(problem)
            self.show_log()

        elif selected == "AC-3":

            final_state = AC3()

            if final_state:

                result = Node(
                    final_state
                )

            else:

                result = None
        elif selected == "Min-Conflicts":

            result = Min_Conflicts(problem)
        else:

            result = None

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

            self.show_final_path()

    # NEXT STEP
    def next_step(self):

        if self.current_index < len(self.path) - 1:

            self.current_index += 1

            self.show_state()

            self.show_final_path()

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

        selected = self.algo_combo.get()

        self.is_belief = (
            selected == "Belief State BFS"
            or 
            selected == "Multi-Goal Belief State BFS"
            or
            selected == "7 Multi-Goal Belief State BFS"
        )

        if not self.is_belief:
            self.board_frame2.pack_forget()

        self.show_state()
    
    def show_final_path(self):
        self.path_text.insert(
            tk.END,
            "\n===== GOALS =====\n"
        )

        self.path_text.insert(
            tk.END,
            f"Goal1 = {self.goal1}\n"
        )

        self.path_text.insert(
            tk.END,
            f"Goal2 = {self.goal2}\n\n"
        )

        self.path_text.delete(
            1.0,
            tk.END
        )

        self.path_text.insert(
            tk.END,
            "====== FINAL PATH ======\n\n"
        )

        for i, node in enumerate(self.path):

            action = (
                node.action
                if node.action
                else "Start"
            )

            self.path_text.insert(
                tk.END,
                f"Step {i}: {action}\n"
            )

            # BELIEF MODE
            if self.is_belief:

                state1, state2 = node.state

                self.path_text.insert(
                    tk.END,
                    "State 1\n"
                )

                for r in range(3):

                    row = state1[
                        r*3:(r+1)*3
                    ]

                    self.path_text.insert(
                        tk.END,
                        f"{row}\n"
                    )

                self.path_text.insert(
                    tk.END,
                    "\nState 2\n"
                )

                for r in range(3):

                    row = state2[
                        r*3:(r+1)*3
                    ]

                    self.path_text.insert(
                        tk.END,
                        f"{row}\n"
                    )

            # NORMAL MODE
            else:

                state = node.state

                for r in range(3):

                    row = state[
                        r*3:(r+1)*3
                    ]

                    self.path_text.insert(
                        tk.END,
                        f"{row}\n"
                    )

            self.path_text.insert(
                tk.END,
                "\n"
            )


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

# đo thời gian chạy BFs
start_time = time.time()

result = breadth_first_search(problem)

end_time = time.time()

runtime = end_time - start_time

if result != None:

    root = tk.Tk()

    gui = PuzzleGUI(
        root,
        result,
        runtime
    )

    root.mainloop()

else:

    print("No solution")