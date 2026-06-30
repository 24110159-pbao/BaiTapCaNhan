# 8 Puzzle AI Visualizer

## 1. Giới thiệu

8 Puzzle AI Visualizer là chương trình giải bài toán 8-Puzzle bằng các
thuật toán tìm kiếm trong lĩnh vực Trí tuệ nhân tạo (AI).

Chương trình sử dụng Python và Tkinter để xây dựng giao diện trực quan,
giúp quan sát quá trình tìm kiếm, đường đi kết quả và thời gian chạy của
từng thuật toán.

## 2. Các thuật toán hỗ trợ

Chương trình hỗ trợ:

-   BFS
-   DFS
-   IDS
-   UCS
-   Greedy Best First Search
-   A\*
-   IDA\*
-   Simple Hill Climbing
-   Best Simple Hill Climbing
-   Stochastic Hill Climbing
-   Random Restart Hill Climbing
-   Local Beam Search
-   Simulated Annealing
-   Belief State BFS
-   Multi Goal Belief State BFS
-   Backtracking
-   AND-OR Search
-   AC-3
-   Min-Conflicts

## 3. Yêu cầu

-   Python \>= 3.8

Thư viện:

-   tkinter
-   random
-   time
-   math
-   collections

## 4. Cách chạy chương trình

Clone project:

``` bash
git clone https://github.com/24110159-pbao/BaiTapCaNhan.git
```

Di chuyển vào thư mục:

``` bash
cd BaiTapCaNhan
```

Chạy:

``` bash
python game_8puzzle.py
```

## 5. Hướng dẫn sử dụng

### Bước 1: Chọn thuật toán

Tại mục Algorithm chọn thuật toán muốn chạy.

Ví dụ:

-   BFS
-   A\*
-   Simulated Annealing

### Bước 2: Chạy thuật toán

Nhấn nút:

Solve

Chương trình sẽ thực hiện tìm kiếm từ trạng thái ban đầu đến trạng thái
đích.

### Bước 3: Xem kết quả

Khu vực Board:

Hiển thị trạng thái hiện tại của puzzle.

Khu vực Final Path:

Hiển thị toàn bộ đường đi tìm được.

Khu vực Search Process:

Hiển thị quá trình mở rộng node của thuật toán.

## 6. Các nút điều khiển

### Next Step

Hiển thị từng bước giải.

### Auto Run

Tự động chạy từng bước cho đến trạng thái đích.

### Reload

Quay lại trạng thái ban đầu.

## 7. Thay đổi trạng thái ban đầu

Mở file:

game_8puzzle.py

Tìm:

``` python
initial_state = [
    1,2,3,
    4,0,6,
    7,5,8
]
```

Có thể thay đổi thành trạng thái khác.

Ví dụ:

``` python
initial_state = [
    1,2,3,
    4,5,6,
    0,7,8
]
```

## 8. Quy tắc di chuyển

Ô trống được ký hiệu là 0.

Có 4 phép di chuyển:

Up:

index - 3

Down:

index + 3

Left:

index - 1

Right:

index + 1

## 9. Heuristic

Greedy sử dụng số ô sai vị trí:

h(n)

A\* và IDA\* sử dụng Manhattan Distance:

\|row1-row2\| + \|col1-col2\|

## 10. Kết quả

Chương trình hiển thị:

-   Đường đi từ đầu đến đích
-   Số bước
-   Chi phí
-   Thời gian chạy
-   Quá trình tìm kiếm

## 11. Cấu trúc file

    BaiTapCaNhan

    ├── game_8puzzle.py

    └── README.md

## 12. Lưu ý

-   BFS, UCS, A\* thường cho kết quả ổn định.
-   DFS và các thuật toán Local Search có thể không tìm được đường tối
    ưu.
-   Các thuật toán ngẫu nhiên có thể cho kết quả khác nhau mỗi lần chạy.

## 13. Repository

https://github.com/24110159-pbao/BaiTapCaNhan.git
