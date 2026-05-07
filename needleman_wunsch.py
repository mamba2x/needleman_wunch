def chiso_needleman_wunsch(sequence_one, sequence_two, match_score=1, mismatch_score=-1, gap_penalty=-2):
    chiso_rows = len(sequence_one) + 1
    chiso_cols = len(sequence_two) + 1

    chiso_score_grid = [[0 for _ in range(chiso_cols)] for _ in range(chiso_rows)]
    chiso_direction_grid = [["" for _ in range(chiso_cols)] for _ in range(chiso_rows)]

    for chiso_row in range(1, chiso_rows):
        chiso_score_grid[chiso_row][0] = chiso_row * gap_penalty
        chiso_direction_grid[chiso_row][0] = "up"

    for chiso_col in range(1, chiso_cols):
        chiso_score_grid[0][chiso_col] = chiso_col * gap_penalty
        chiso_direction_grid[0][chiso_col] = "left"

    for chiso_row in range(1, chiso_rows):
        for chiso_col in range(1, chiso_cols):
            if sequence_one[chiso_row - 1] == sequence_two[chiso_col - 1]:
                chiso_diagonal_score = chiso_score_grid[chiso_row - 1][chiso_col - 1] + match_score
            else:
                chiso_diagonal_score = chiso_score_grid[chiso_row - 1][chiso_col - 1] + mismatch_score

            chiso_up_score = chiso_score_grid[chiso_row - 1][chiso_col] + gap_penalty
            chiso_left_score = chiso_score_grid[chiso_row][chiso_col - 1] + gap_penalty

            chiso_best_score = max(chiso_diagonal_score, chiso_up_score, chiso_left_score)
            chiso_score_grid[chiso_row][chiso_col] = chiso_best_score

            if chiso_best_score == chiso_diagonal_score:
                chiso_direction_grid[chiso_row][chiso_col] = "diagonal"
            elif chiso_best_score == chiso_up_score:
                chiso_direction_grid[chiso_row][chiso_col] = "up"
            else:
                chiso_direction_grid[chiso_row][chiso_col] = "left"

    chiso_aligned_one = ""
    chiso_aligned_two = ""
    chiso_row = len(sequence_one)
    chiso_col = len(sequence_two)

    while chiso_row > 0 or chiso_col > 0:
        chiso_move = chiso_direction_grid[chiso_row][chiso_col]

        if chiso_move == "diagonal":
            chiso_aligned_one = sequence_one[chiso_row - 1] + chiso_aligned_one
            chiso_aligned_two = sequence_two[chiso_col - 1] + chiso_aligned_two
            chiso_row -= 1
            chiso_col -= 1
        elif chiso_move == "up":
            chiso_aligned_one = sequence_one[chiso_row - 1] + chiso_aligned_one
            chiso_aligned_two = "-" + chiso_aligned_two
            chiso_row -= 1
        else:
            chiso_aligned_one = "-" + chiso_aligned_one
            chiso_aligned_two = sequence_two[chiso_col - 1] + chiso_aligned_two
            chiso_col -= 1

    return chiso_aligned_one, chiso_aligned_two, chiso_score_grid[-1][-1], chiso_score_grid


def chiso_print_score_grid(chiso_score_grid, sequence_one, sequence_two):
    chiso_header = "      " + "  ".join(sequence_two)
    print(chiso_header)

    for chiso_index, chiso_row in enumerate(chiso_score_grid):
        if chiso_index == 0:
            chiso_label = " "
        else:
            chiso_label = sequence_one[chiso_index - 1]

        chiso_values = "  ".join(f"{chiso_cell:2}" for chiso_cell in chiso_row)
        print(f"{chiso_label}  {chiso_values}")


if __name__ == "__main__":
    chiso_first_dna = input("Enter first DNA sequence: ").upper().strip()
    chiso_second_dna = input("Enter second DNA sequence: ").upper().strip()

    chiso_result_one, chiso_result_two, chiso_final_score, chiso_matrix = chiso_needleman_wunsch(
        chiso_first_dna,
        chiso_second_dna,
    )

    print("\nScore matrix:")
    chiso_print_score_grid(chiso_matrix, chiso_first_dna, chiso_second_dna)

    print("\nBest global alignment:")
    print(chiso_result_one)
    print(chiso_result_two)
    print(f"\nAlignment score: {chiso_final_score}")
