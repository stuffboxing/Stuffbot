from functions.get_files_info import get_files_info

test_folders = [".", "pkg", "/bin", "../"]

__main_folder = "calculator"


def base_test(target_dir, sub_dir):
    actual_dir_name = "current"
    if sub_dir != ".":
        actual_dir_name = f"'{sub_dir}'"
    items = get_files_info(target_dir, sub_dir)

    print(f"Result for {actual_dir_name} directory:")
    for line in items.split("\n"):
        if "Error:" in line:
            print(f"    {line}")
        else:
            print(f"  {line}")


def main():
    for folder in test_folders:
        base_test(__main_folder, folder)
        print("\n")


if __name__ == "__main__":
    main()
