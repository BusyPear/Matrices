class Matrix:
    def __init__(self, r, c, value = None):
        # self.value = None
        self.row = r
        self.column = c
        if value is None:
            self.value = self.zero_matrix()
        else:
            self.value = value

    def empty_matrix(self):
        result = []
        for i in range(self.row):
            result.append([])
        return result

    def zero_matrix(self):
        result = []
        for i in range(self.row):
            row = [0.0 for j in range(self.column)]
            result.append(row)
        return result

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

    def get_row(self, row):
        return self.value[row]

    def get_column(self, column):
        return self.transpose()[column]

    def check_zero_row(self):
        row_nums = []
        for num in range(len(self.value)):
            for ele in self.value[num]:
                if ele != 0:
                    break
                    pass
            else:
                row_nums.append(num)
        return row_nums

    def check_zero_column(self):
        self_t = Matrix(self.column, self.row, self.transpose())
        column_nums = self_t.check_zero_row()
        return column_nums

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

    # Probably GEM algorithm next, make the function return a matrix object in REF form
    def REF(self):
        result = Matrix(self.row, self.column, self.value.copy())
        # (Complete)Step 1 - Send all zero rows to bottom
        zero_rows = self.check_zero_row()
        row_num = self.row - 1
        # (edit below line for new row/column convention)
        # non_zero_rows = [row_num for row_num in range(1, self.row+1) if row_num not in zero_rows]
        for i in range(len(zero_rows)):
            if zero_rows[-1-i] == row_num:
                row_num -= 1
                continue
            result.value = result.swap_rows(zero_rows[-1-i], row_num)
            row_num -= 1

        # Step 2 - Identify first non-zero column, apply partial pivot(optional) and interchange that row with first row
        zero_columns = result.check_zero_column()
        print(zero_columns)
        # subm_self = submatrix of original
        # (1) Find first nonzero column
        non_zero_column = 0
        for i in range(result.column):
            if i not in zero_columns:
                non_zero_column = i
                break
        else:
            # Add something if matrix is zero matrix???
            pass
        # (2) Find the row of largest element in that column
        non_zero_columns = result.get_column(non_zero_column)
        print(non_zero_columns)
        pivot = max(non_zero_columns)
        print(pivot)
        pivot_column = non_zero_column
        print(pivot_column)
        pivot_row, _ = result.find_element(pivot)
        print(pivot_row)
        result.value = result.swap_rows(0, pivot_row)

        # Step 3 - Make all elements below this pivot equal zero
        for row_num in range(1,self.row):
            result.value = result.lin_comb(row_num, 0, (-1) * result.value[row_num][pivot_column]/pivot)

        # Step 4 - Repeat steps 2 & 3 for submatrices of result

        return result.value

    # This comment marks the end of the class Matrix


if __name__ == "__main__":
    a = Matrix(4,3, [[0.0,8.0,0.0], [0.0,0.0,7.0], [0.0,7.0,6.0], [0.0,5.0,0.0]])
    # a.value = a.set_matrix()
    b = Matrix(4, 3, a.REF())
    b.show()
    # print(b)



