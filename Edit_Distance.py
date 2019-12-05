# finds min number of operations to convert str1 to str2
def edit_distance(str1, str2, str1_len, str2_len):

    # base case 1:
    # checks if 1st string is empty
    if str1_len == 0:
        return str2_len

    # base case 2:
    # checks if 2nd string is empty
    if str2_len == 0:
        return str1_len

    # checks last char of strings
    # if similar, edit count is not updated and check edits for remaining characters
    if str1[str1_len - 1] == str2[str2_len - 1]:
        return edit_distance(str1, str2, str1_len - 1, str2_len - 1)

    # else last char of strings differ
    # performs all 3 possible options and gets edit count : 1) insert, 2) remove, 3) replace
    # return the min edit count of the three plus 1
    return 1 + min(edit_distance(str1, str2, str1_len, str2_len - 1),  # Insert
                   edit_distance(str1, str2, str1_len - 1, str2_len),  # Remove
                   edit_distance(str1, str2, str1_len - 1, str2_len - 1)  # Replace
                   )

def main():
    # asks user for 2 words to compare
    str1 = input("Enter first word: ")
    str2 = input("Enter second word: ")

    # prints number of edits needed for conversion
    print("The minimum number of operations needed to convert word one into word two is: ", end="", flush=True)
    print(edit_distance(str1.lower(), str2.lower(), len(str1), len(str2)))

main()
