
import sys

DIRECTIONS = {"u", "d", "r", "l", "w", "x", "y", "z"}
NUMBER_VALUES_ILLEGAL = "You didn't put in 4 items. That is the request."
WORD_FILE_NOT_EXIST = "The word file doesn't exist."
MATRIX_FILE_NOT_EXIST = "The matrix file doesn't exist."
ILLEGAL_DIRECTIONS = "Some of the directions are illegal."


def make_directions_set(directions):
    """Gets a string and changes if into a set"""
    directions_set = set()
    for i in range(len(directions)):
        directions_set.add(directions[i])
    return directions_set


def make_dictionary_list(word_appearance):
    """Gets a dictionary and returns a list of tuples with it's values,
    only the values that are different from 0"""
    appearance_lst = list()
    for word, times in word_appearance.items():
        if times != 0:
            appearance_lst.append((word, times))
    return appearance_lst


def check_input_args(args):
    """Checks each parameter got if legal. If one of them isn't, it returns
    a massage that says this. If all are legal, returns None
    so the program will continue to run."""
    if len(args) != 5:  # including the file's name
        return NUMBER_VALUES_ILLEGAL
    word_file = args[1]
    try:
        with open(word_file) as wf:
            wf.read()
    except OSError:
        return WORD_FILE_NOT_EXIST
    matrix_file = args[2]
    try:
        with open(matrix_file) as mf:
            mf.read()
    except OSError:
        return MATRIX_FILE_NOT_EXIST
    directions = args[4]
    directions = make_directions_set(directions)
    if not directions.issubset(DIRECTIONS):
        return ILLEGAL_DIRECTIONS
    return None


def read_wordlist_file(filename):
    """Gets the place of the word list and returns a list of the words in it"""
    with open(filename, 'r') as my_open_file:
        word_list = my_open_file.readlines()
    word_list = [x.rstrip() for x in word_list]
    return word_list


def read_matrix_file(filename):
    """Gets the place of the matrix file, returns if as list of lists
    of every line."""
    with open(filename, 'r') as my_open_file:
        matrix = my_open_file.readlines()
    matrix = [x.rstrip() for x in matrix]
    matrix = [matrix[i].split(",") for i in range(len(matrix))]
    return matrix


def build_a_new_matrix(rows, columns):
    """Get the number of rows and the number of columns and return a
    matrix at those sizes. The matrix is built from a list with strings
    within a list."""
    new_matrix = []
    for i in range(rows):
        new_matrix.append(list())
        for j in range(columns):
            new_matrix[i].append("")
    return new_matrix


def reorder_dz(matrix):
    """Gets a matrix and reorders it, so the down arrow will become as a
    left to right arrow. Or so the down left going arrow will become
    as a right down going diagonal arrow."""
    num_columns = len(matrix)
    num_rows = len(matrix[0])
    new_matrix = build_a_new_matrix(num_rows, num_columns)
    for row in range(num_rows):
        for column in range(num_columns):
            new_matrix[num_rows - row - 1][column] = matrix[column][row]
    return new_matrix


def reorder_l(matrix):
    """Gets a matrix and reorders it, so the right to left arrow will become
    as a left to right arrow."""
    num_columns = len(matrix[0])
    num_rows = len(matrix)
    new_matrix = build_a_new_matrix(num_rows, num_columns)
    for column in range(num_columns):
        for row in range(num_rows):
            new_matrix[row][num_columns - column - 1] = matrix[row][column]
    return new_matrix


def reorder_uw(matrix):
    """Gets a matrix and reorders it, so the up arrow will become
    as a left to right arrow. Or so the up right going arrow will become
    as a right down going diagonal arrow."""
    num_columns = len(matrix)
    num_rows = len(matrix[0])
    new_matrix = build_a_new_matrix(num_rows, num_columns)
    for row in range(num_rows):
        for column in range(num_columns):
            new_matrix[row][num_columns - column - 1] = matrix[column][row]
    return new_matrix


def reorder_x(matrix):
    """Gets a matrix and reorders it, so the up left going arrow will become
    as a right down going diagonal arrow."""
    num_columns = len(matrix)
    num_rows = len(matrix[0])
    new_matrix = build_a_new_matrix(num_rows, num_columns)
    for row in range(num_rows):
        for column in range(num_columns):
            new_matrix[num_rows - row - 1][num_columns - column - 1] = matrix[column][row]
    return new_matrix


def reorder_matrix(matrix, direction):
    """Sends the matrix to be reordered the matrix by the direction to be
    as right to left arrow or as right down going diagonal arrow."""
    if direction == "r" or direction == "y":
        return matrix
    if direction == "d" or direction == "z":
        return reorder_dz(matrix)
    if direction == "u" or direction == "w":
        return reorder_uw(matrix)
    if direction == "l":
        return reorder_l(matrix)
    if direction == "x":
        return reorder_x(matrix)


def do_if_straight(word, matrix, direction):
    """Sends the matrix to be reordered by the direction, so we will check only
    for the right arrow. Checks how many times a word is in that matrix."""
    new_matrix = reorder_matrix(matrix, direction)
    appearance_times = 0
    num_rows = len(new_matrix)
    num_columns = len(new_matrix[0])
    word_length = len(word)
    if num_columns < word_length:
        return appearance_times
    for row in range(num_rows):
        for column in range(num_columns - word_length + 1):
            if new_matrix[row][column] == word[0]:
                this_column = column
                count_length = 1
                for letter in word:
                    if new_matrix[row][this_column] != letter:
                        break
                    if letter == word[-1:] and count_length == word_length:
                        appearance_times += 1
                        break
                    this_column += 1
                    count_length += 1
    return appearance_times


def do_if_diagonal(word, matrix, direction):
    """Sends the matrix to be reordered by the direction, so we will check only
    for the right right down going diagonal arrow. Checks how many times a
    word is in that matrix."""
    new_matrix = reorder_matrix(matrix, direction)
    appearance_times = 0
    num_rows = len(new_matrix)
    num_columns = len(new_matrix[0])
    word_length = len(word)
    if num_rows < word_length:
        return appearance_times
    for row in range(num_rows - word_length + 1):
        for column in range(num_columns - word_length + 1):
            if new_matrix[row][column] == word[0]:
                this_row = row
                this_column = column
                count_length = 1
                for letter in word:
                    if new_matrix[this_row][this_column] != letter:
                        break
                    if letter == word[-1:] and count_length == word_length:
                        appearance_times += 1
                        break
                    this_column += 1
                    this_row += 1
                    count_length += 1
    return appearance_times


def go_by_direction(word, matrix, direction):
    """Checks if the direction is one of the staight ones or one of the diagonal,
    and sends to another function according to that. Returns the number of times
    it appears in the matrix by that direction."""
    appearance_times = 0
    if direction in "udrl":
        appearance_times = do_if_straight(word, matrix, direction)
    if direction in "wxyz":
        appearance_times = do_if_diagonal(word, matrix, direction)
    return appearance_times


def find_word_appearance(word, matrix, directions):
    """Gets a word, a matrix and directions and checks how many times
    the word appears in the matrix, by the directions got."""
    num_appearance = 0
    for direction in directions:
        num_appearance += go_by_direction(word, matrix, direction)
    return num_appearance


def find_words_in_matrix(word_list, matrix, directions):
    """Gets words list and checks how many times each word is in
    the matrix by the directions got."""
    if word_list == [] or matrix == []:
        return []
    word_appearance = dict()
    directions = make_directions_set(directions)
    for word in word_list:
        word_appearance[word] = find_word_appearance(word, matrix, directions)
    word_appearance = make_dictionary_list(word_appearance)
    return word_appearance


def write_output_file(results, output_filename):
    """Gets the results as tuples and write them to a file named as got.
    If the file already exists, it rewrite it. If it doesn't, it opens such."""
    output_file = open(output_filename, 'w')
    for n in range(len(results)):
        results[n] = results[n][0] + "," + str(results[n][1])
        if n != (len(results) - 1):
            results[n] = results[n] + "\n"
    for r in range(len(results)):
        output_file.write(results[r])
    output_file.close()


def start_checking():
    """Gets the input from the command line as the user wrote. Checks
    if the input is legal. Stops the program if not, else checks how many
    times each word is in the matrix by the directions got , and returns
    the values."""
    args = sys.argv
    check = check_input_args(args)
    if check is not None:
        print(check)
        return
    word_file = args[1]
    matrix_file = args[2]
    output_file = args[3]
    directions = args[4]
    word_list = read_wordlist_file(word_file)
    matrix = read_matrix_file(matrix_file)
    results = find_words_in_matrix(word_list, matrix, directions)
    write_output_file(results, output_file)


if __name__ == "__main__":
    start_checking()
