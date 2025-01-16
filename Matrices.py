class Matrix:
    def __init__(self, r, c, value = None):
        self.row = r
        self.column = c
        if value is None:
            self.value = self.zero_matrix()
        else:
            self.value = value

    # Returns nested list with no elements inside
    def empty_matrix(self):
        result = []
        for i in range(self.row):
            result.append([])
        return result

    # Returns a list similar to self but with all elements zero
    def zero_matrix(self):
        result = []
        for i in range(self.row):
            row = [0.0 for j in range(self.column)]
            result.append(row)
        return result

    # Returns a list with the values given by user
    def set_matrix(self):
        print(f"The matrix requested is a {self.row}x{self.column} matrix. ")
        print("Write each row in a new line and each element in a row separated by one space. ")
        result = []
        for i in range(self.row):
            row_str = input(f"Row {i}: ").split()
            if len(row_str) == self.column:
                row = [float(ele) for ele in row_str]
                result.append(row)
            else:
                result = self.zero_matrix()
                print("Not enough or too many elements given. Please try again.")
                break
        return result

    def show(self):
        print("[")
        for i in range(self.row):
            for j in range(self.column):
                print(self.value[i][j], end=", ")
            print()
        print("]")

    def transpose(self):
        result = []
        for ele_num in range(self.column):
            element = []
            for row_num in range(self.row):
                element.append(self.value[row_num][ele_num])
            result.append(element)
        return result

    def find_element(self, element):
        for row in self.value:
            if element in row:
                return self.value.index(row), row.index(element)

    def get(self, num, column = False):
        if column:
            return self.transpose()[num]
        return self.value[num]

    def get_zeroes(self, column = False):
        row_nums = []
        max_index = self.row if not column else self.column
        for num in range(max_index):
            if self.is_zero(num, column = column):
                row_nums.append(num)
        return row_nums

    def is_zero(self, num, column = False):
        element = self.get(num, column = column)
        for i in element:
            if i != 0:
                return False
        return True

    def swap_rows(self, row1, row2):
        result = self.value.copy()
        result[row1], result[row2] = result[row2], result[row1]
        return result

    def lin_comb(self, row1, row2, scalar):
        result = self.value.copy()
        scaled_row2 = [scalar * ele for ele in result[row2]]
        result[row1] = [ele1 + ele2 for ele1, ele2 in zip(result[row1], scaled_row2)]
        return result

    def scale_row(self, row, scalar):
        result = self.value.copy()
        result[row] = [scalar * ele for ele in result[row]]
        return result

    def zero_rows_bottom(self):
        result = Matrix(self.row, self.column, self.value.copy())
        zero_rows = result.get_zeroes()
        row_num = result.row - 1
        for i in range(len(zero_rows)):
            if zero_rows[-1 - i] == row_num:
                row_num -= 1
                continue
            result.value = result.swap_rows(zero_rows[-1 - i], row_num)
            row_num -= 1
        return result.value

    def conv_piv_col(self, col_num):
        result = Matrix(self.row, self.column, self.value.copy())
        # (1) Find the row of largest element in that column
        pivotal_column = result.get(col_num, column=True)
        pivot = max(pivotal_column)
        pivotal_row_index, _ = result.find_element(pivot)
        result.value = result.swap_rows(0, pivotal_row_index)
        # (2) Reduce all elements below the pivot equal to zero
        for row_num in range(1,result.row):
            try:
                result.value = result.lin_comb(row_num, 0, (-1) * result.value[row_num][col_num] / pivot)
            except ZeroDivisionError:
                pass

        return result.value

    def get_ref(self):
        result = Matrix(self.row, self.column, self.value.copy())
        # Step 1 - Send all zero rows to bottom
        result.value = result.zero_rows_bottom()
        # Step 2 - Yet to write
        row_index = 0
        for col_index in range(result.column):
            if result.is_zero(col_index, column = True):
                continue
            subm_result = Matrix(result.row - row_index, result.column, result.value[row_index:])
            result.value[row_index:] = subm_result.conv_piv_col(col_index)
            row_index +=1

        return result.value

    # This comment marks the end of the class Matrix


if __name__ == "__main__":
    print("This program right now will print the Row Echelon Form of your matrix")
    row = int(input("Enter number of rows of your matrix: "))
    column = int(input("Enter number of columns of your matrix: "))
    print()
    a = Matrix(row,column)
    a.value = a.set_matrix()
    a.show()
    b = Matrix(row, column, a.get_ref())
    b.show()




