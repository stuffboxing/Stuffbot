from functions.get_file_content import get_file_content

__working_dir = "calculator"

test_cases = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]


def lorem_test(file_path):
    content = get_file_content(__working_dir, file_path)
    is_truncted = "truncated" in content
    print(f"Result lorem: truncated={is_truncted}, char_length={len(content)}")


def base_test(file_path):
    print(get_file_content(__working_dir, file_path))


def main():
    lorem_test("lorem.txt")
    print("\n")
    for test in test_cases:
        base_test(test)
        print("\n")


if __name__ == "__main__":
    main()
