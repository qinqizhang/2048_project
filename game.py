import tkinter as tk
import random
class NoChangeException(Exception):
    '''
    The exception handling handles all invalid inputs.
    Parameters:
        Exception
    Returns:
        it will pass some function if the function raises NoChangeException.
    '''
    pass
class Game(tk.Frame):
    def __init__(self):
        '''
        The constructrue of the class, and it defines main grid.GUI,the keyboard key.
        '''
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(self, bg='lightgrey', bd=3, width=400,height=400)
        self.main_grid.grid(pady=(100,0))
        self.make_GUI()
        self.start_game()
        self.master.bind("a", self.left)
        self.master.bind("d", self.right)
        self.master.bind("w", self.up)
        self.master.bind("s", self.down)
        self.mainloop()
    def make_GUI(self):
        '''
        Design the UI and set the original frame. There are cell frame and score frame.
        '''        
        self.cells=[]
        for i in range(4):
            row=[]
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg='white',
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i,column=j,padx=5,pady=5)
                cell_number = tk.Label(self.main_grid,bg='white')
                cell_number.grid(row=i,column=j)
                cell_data = {"frame":cell_frame,"number":cell_number}
                row.append(cell_data)
            self.cells.append(row)
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5,y=45,anchor="center")
        tk.Label(
            score_frame,
            text="Score"
        ).grid(row=0)
        self.score_label = tk.Label(score_frame,text = "0")
        self.score_label.grid(row=1)

    def start_game(self):
        '''
        Start game with the matrix and cells. Initially there would be 2 random cells with a number 2 in it.
        '''  
        self.matrix = []
        for i in range(4):
            self.matrix.append([0]*4)
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg='orange')
        self.cells[row][col]["number"].configure(
            bg='orange',
            fg="white",
            font=("Helvetica", 55, "bold"),
            text="2"
        )
        while(self.matrix[row][col]!=0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg='orange')
        self.cells[row][col]["number"].configure(
            bg='orange',
            fg="white",
            font=("Helvetica", 55, "bold"),
            text="2"
        )
        self.score=0
    def stack(self):
        '''
        function to compress the grid after every step before and after merging cells.
        '''
        new_matrix = []
        for i in range(4):
            new_matrix.append([0]*4)
        
        for i in range(4):
            position = 0
            for j in range(4):
                if self.matrix[i][j]!= 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position+=1
        self.matrix = new_matrix
    
    def combine(self):
        '''
        function to merge the cells in matrix after compressing
        '''
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j]!= 0 and self.matrix[i][j]==self.matrix[i][j+1]:
                    self.matrix[i][j]=self.matrix[i][j]*2
                    self.matrix[i][j+1] =0
                    self.score +=self.matrix[i][j]
    def reverse(self):
        '''
        function to reverse the matrix means reversing the content of each row (reversing the sequence)
        '''
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix

    def transpose(self):
        '''
        function to get the transpose of matrix means interchanging rows and column
        '''
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[j][i])
        self.matrix = new_matrix
    def add_new(self):
        '''
        function to add a new 2 in grid at any random empty cell
        '''
        if any(0 in row for row in self.matrix):
            row = random.randint(0,3)
            col = random.randint(0,3)
            while(self.matrix[row][col]!=0):
                row = random.randint(0,3)
                col = random.randint(0,3)
            self.matrix[row][col] = 2 
        
    def update_GUI(self):
        '''
        function to update the UI with the new matrix
        '''
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value==0:
                    self.cells[i][j]["frame"].configure(bg='white')
                    self.cells[i][j]["number"].configure(bg='white',text="")
                else:
                    self.cells[i][j]["frame"].configure(bg='orange')
                    self.cells[i][j]["number"].configure(
                        bg='orange',
                        fg="white",
                        font=("Helvetica", 55, "bold"),
                        text=str(cell_value))
        self.score_label.configure(text = self.score)
        self.update_idletasks()

    def left(self,event):
        '''
        function to move left and check if the input is valid, and update the UI with the new matrix
        '''
        try:
        # Save the current state of the matrix
            matrix_before = [row[:] for row in self.matrix]
            # Perform the stack operation
            self.stack()
            self.combine()
            self.stack()
            # Check if the matrix has changed after those operations
            if self.matrix == matrix_before:
                raise NoChangeException

            # Continue with the rest of the operations if there is a change
            self.add_new()
            self.update_GUI()
            self.game_over()
        except NoChangeException:
            # Handle the case when there is no change in the matrix
            print("invalid input")


    def right(self,event):
        '''
        function to move right and check if the input is valid, and update the UI with the new matrix
        '''
        try:
        # Save the current state of the matrix
            matrix_before = [row[:] for row in self.matrix]
            # Perform the stack operation
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            # Check if the matrix has changed after those operations
            if self.matrix == matrix_before:
                raise NoChangeException
            # Continue with the rest of the operations if there is a change
            
            self.add_new()
            self.update_GUI()
            self.game_over()
        except NoChangeException:
            # Handle the case when there is no change in the matrix
            print("invalid input")
    
    def up(self,event):
        '''
        function to move up and check if the input is valid, and update the UI with the new matrix
        '''
        try:
        # Save the current state of the matrix
            matrix_before = [row[:] for row in self.matrix]
            # Perform the stack operation
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
            # Check if the matrix has changed after those operations
            if self.matrix == matrix_before:
                raise NoChangeException
            # Continue with the rest of the operations if there is a change
            
            self.add_new()
            self.update_GUI()
            self.game_over()
        except NoChangeException:
            # Handle the case when there is no change in the matrix
            print("invalid input")
    
    def down(self,event):
        '''
        function to move down and check if the input is valid, and update the UI with the new matrix
        '''
        try:
        # Save the current state of the matrix
            matrix_before = [row[:] for row in self.matrix]
            # Perform the stack operation
            self.transpose()
            self.reverse()        
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()
            # Check if the matrix has changed after those operations
            if self.matrix == matrix_before:
                raise NoChangeException
            # Continue with the rest of the operations if there is a change
            
            self.add_new()
            self.update_GUI()
            self.game_over()
        except NoChangeException:
            # Handle the case when there is no change in the matrix
            print("invalid input")

    def horizontal_move_exists(self):
        '''
        function to check if there is any possible move in horizontal area.
        '''
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exists(self):
        '''
        function to check if there is any possible move in vertical area.
        '''
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
    def game_over(self):
        '''
        function to check if the status of grid to decide if the game is over.
        '''
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text="You Win",
                bg="green",
                fg="white",
                font=("Helvetica", 55, "bold")
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(
                game_over_frame,
                text="Game Over",
                bg="Red",
                fg="white",
                font=("Helvetica", 55, "bold")
            ).pack()


        
        