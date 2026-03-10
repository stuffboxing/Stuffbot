from functions.run_python_file import run_python_file

__working_dir = "calculator"

test_cases = [
    ["main.py", ""],
    ["main.py", "3 + 5"],
    ["tests.py", ""],
    ["../main.py", ""],
    ["nonexistent.py", ""],
    ["lorem.txt", ""],
]


def test_base(file, args):
    print(run_python_file(__working_dir, file, args))


def main():
    for file, args in test_cases:
        test_base(file, args)
        print("\n")


if __name__ == "__main__":
    main()
