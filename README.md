# 8-Puzzle Solver - BFS, DFS, IDS

## Giới thiệu

Project mô phỏng bài toán **8-Puzzle** bằng Python và Tkinter.

Chương trình cho phép:

* Giải bài toán 8-puzzle
* Minh họa từng bước di chuyển
* So sánh các thuật toán tìm kiếm:

  * BFS (Breadth First Search)
  * DFS (Depth First Search)
  * IDS (Iterative Deepening Search)

---

# Mô tả bài toán

8-Puzzle gồm:

* 8 ô số từ 1 → 8
* 1 ô trống (0)

Mục tiêu:

Biến đổi từ trạng thái ban đầu (`initial_state`) sang trạng thái đích (`goal_state`) bằng cách di chuyển ô trống.

Ví dụ:

Initial State:

```text
1 2 3
4 0 6
7 5 8
```

Goal State:

```text
1 2 3
4 5 6
7 8 0
```

---

# Luật di chuyển

Ô trống (0) có thể:

* Up
* Down
* Left
* Right

nếu không vượt biên của bảng 3x3.

---

# Cấu trúc chương trình

## Class Node

Lưu thông tin của mỗi node:

* state
* parent
* action
* path_cost

---

## Class Problem

Định nghĩa:

* trạng thái đầu
* trạng thái đích
* actions(state)
* result(state, action)
* goal_test(state)

---

# Các thuật toán tìm kiếm

## 1. Breadth First Search (BFS)

### Ý tưởng

BFS mở rộng node theo từng mức độ sâu.

Node được đưa vào queue theo cơ chế FIFO.

### Đặc điểm

* Tìm được đường đi ngắn nhất
* Đầy đủ (complete)
* Optimal với cost bằng nhau

### Ưu điểm

* Đảm bảo lời giải tối ưu
* Phù hợp khi lời giải nằm gần root

### Nhược điểm

* Tốn nhiều bộ nhớ
* Frontier tăng rất nhanh

### Độ phức tạp

```text
Time  : O(b^d)
Space : O(b^d)
```

---

## 2. Depth First Search (DFS)

### Ý tưởng

DFS đi sâu nhất có thể trước rồi mới quay lui.

Sử dụng stack (LIFO).

### Đặc điểm

* Không đảm bảo tối ưu
* Có thể đi sâu vô ích

### Ưu điểm

* Bộ nhớ nhỏ
* Thường chạy nhanh hơn BFS

### Nhược điểm

* Có thể không tìm ra đường ngắn nhất
* Có thể bị lặp vô hạn nếu không chống cycle

### Độ phức tạp

```text
Time  : O(b^m)
Space : O(bm)
```

---

## 3. Iterative Deepening Search (IDS)

### Ý tưởng

IDS kết hợp:

* DFS
* Depth Limited Search (DLS)

Thuật toán sẽ:

* tìm với depth = 0
* depth = 1
* depth = 2
* ...

cho đến khi tìm được lời giải.

### Đặc điểm

* Optimal như BFS
* Memory nhỏ như DFS

### Ưu điểm

* Ít tốn RAM
* Đảm bảo tìm lời giải ngắn nhất
* Không cần biết trước độ sâu lời giải

### Nhược điểm

* Phải tìm lại nhiều node
* Chậm hơn DFS/BFS trong bài toán nhỏ

### Độ phức tạp

```text
Time  : O(b^d)
Space : O(bd)
```

---

# Giao diện (UI)

Giao diện được xây dựng bằng Tkinter gồm:

* Hiển thị bảng 3x3
* Chọn thuật toán
* Hiển thị runtime
* Next Step
* Auto Run
* Reload

Ngoài ra chương trình còn hiển thị:

* action
* cost
* đường đi lời giải

