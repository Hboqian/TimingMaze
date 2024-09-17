class TimingMazeState:
    def __init__(self, maze_state, is_end_visible, end_x, end_y, start_x, start_y):
        """
            Args:
                maze_state (List[List[int]]): 2D list of integers representing the maze state
                is_end_visible (bool): Boolean representing if the end is visible
                end_x (int): x-coordinate of the end cell
                end_y (int): y-coordinate of the end cell
        """
        self.maze_state = maze_state
        self.start_x = start_x
        self.start_y = start_y
        self.is_end_visible = is_end_visible
        if is_end_visible:
            self.end_x = end_x
            self.end_y = end_y
    
    def __str__(self):
        return f"Is End Visibile: {self.is_end_visible}\nStart: [{self.start_x},{self.start_y}]\n"