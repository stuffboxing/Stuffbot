from functions.write_file import write_file

__working_dir = "calculator"

test_cases = [
    ["lorem.txt", "wait, this isn't lorem ipsum"],
    ["pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
    ["/tmp/temp.txt", "this should not be allowed"],
]


def base_test(file, content):
    print(write_file(__working_dir, file, content))


def main():
    for file, content in test_cases:
        base_test(file, content)
        print("\n")


if __name__ == "__main__":
    main()
