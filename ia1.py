import random
from queue import Queue

class Room:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.clean = 0  # 1 represents clean, 0 represents dirty

    def is_dirty(self):
        return self.clean == 0

    def has_agent(self):
        return self.row == agent.row and self.col == agent.col

    def __str__(self):
        return "\U0001F916" if self.has_agent() else (
            "\U0001F4A9" if self.is_dirty() else "\u2728"
        )

class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.rooms = [[Room(i, j) for j in range(cols)] for i in range(rows)]

    def randomize_dirt(self):
        for row in self.rooms:
            for room in row:
                room.clean = random.randint(0, 1)

    def is_clean(self):
        for row in self.rooms:
            for room in row:
                if room.is_dirty():
                    return False
        return True

    def performance_measure(self):
        clean = 0
        dirty = 0
        for row in self.rooms:
            for room in row:
                if room.is_dirty():
                    dirty += 1
                else:
                    clean += 1
        print(f"There are {dirty} dirty out of {clean + dirty} rooms")

    def __str__(self):
        return "\n".join([" ".join([str(room) for room in row]) for row in self.rooms])

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.row = random.randint(0, self.environment.rows - 1)
        self.col = random.randint(0, self.environment.cols - 1)
        self.cost = 0

    def move_up(self):
        if self.row > 0:
            self.row -= 1
            self.cost += 1

    def move_down(self):
        if self.row < self.environment.rows - 1:
            self.row += 1
            self.cost += 1

    def move_left(self):
        if self.col > 0:
            self.col -= 1
            self.cost += 1

    def move_right(self):
        if self.col < self.environment.cols - 1:
            self.col += 1
            self.cost += 1

    def move_to_closest_dirty_room(self):
        def bfs(start_row, start_col):
            visited = [[False for _ in range(self.environment.cols)] for _ in range(self.environment.rows)]
            q = Queue()
            q.put((start_row, start_col, 0))
            while not q.empty():
                row, col, distance = q.get()
                if self.environment.rooms[row][col].is_dirty():
                    return row, col
                visited[row][col] = True
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    r, c = row + dr, col + dc
                    if 0 <= r < self.environment.rows and 0 <= c < self.environment.cols and not visited[r][c]:
                        q.put((r, c, distance + 1))
            return None

        closest_dirty_room = bfs(self.row, self.col)
        if closest_dirty_room is not None:
            target_row, target_col = closest_dirty_room
            if target_row < self.row:
                self.move_up()
            elif target_row > self.row:
                self.move_down()
            elif target_col < self.col:
                self.move_left()
            else:
                self.move_right()

    def clean_current_room(self):
        current_room = self.environment.rooms[self.row][self.col]
        if current_room.is_dirty():
            current_room.clean = 1
        else:
            print("Room already clean")

if __name__ == "__main__":
    environment = Environment(10, 10)
    environment.randomize_dirt()
    agent = Agent(environment)
    stages = 0
    while not environment.is_clean():
        print(environment)
        environment.performance_measure()
        agent.clean_current_room()
        agent.move_to_closest_dirty_room()
        stages += 1
        print()

    print("Cleaning complete!")
    print(f"{stages} stages needed")
    print(f"Total cost: {agent.cost}")
