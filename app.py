from os import system
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def clear_screen():
    system("cls")


def wait_and_return():
    input("\nPress ENTER to return to the menu...")
    return True


def get_option(text="Select an option: ", min_value=1, max_value=6):
    try:
        value = int(input(text))
        if value < min_value or value > max_value:
            print(
                f"Invalid input. Please enter a number between {min_value} and {max_value}.")
            return 0
        return value
    except ValueError:
        print(
            f"Invalid input. Please enter a number between {min_value} and {max_value}.")
        return 0


def list_items(items: list[str]):
    for index, item in enumerate(items):
        print(f"[{index + 1}] - {item}")
    return items


def select_from_list(items: list[str], prompt: str):
    list_items(items)
    while True:
        option = get_option(prompt, 1, len(items))
        if option:
            return items[option - 1]


def count_recipes():
    return list(BASE_PATH.glob("**/*.txt"))


def list_categories():
    return [f.name for f in BASE_PATH.iterdir() if f.is_dir() and not f.name.startswith(".")]


def list_files(path):
    return [f.stem for f in Path(path).glob("*.txt")]


def read_file(path):
    try:
        with path.open(encoding="utf-8") as file:
            print("=== RECIPE CONTENT ===")
            print(file.read())
    except FileNotFoundError:
        print("❌ The recipe does not exist.")


def create_file(path):
    try:
        with path.open("x", encoding="utf-8") as file:
            file.write(input("Enter the content of the new recipe: "))
            print("Recipe created successfully.")
    except FileNotFoundError:
        print("❌ Directory does not exist")
    except FileExistsError:
        print("❌ File already exists")
    except PermissionError:
        print("❌ Permission denied")
    except OSError as e:
        print(f"❌ OS error: {e}")


def read_recipe():
    category = select_from_list(list_categories(), "Select a category: ")
    files = list_files(BASE_PATH / category)
    recipe = select_from_list(files, "Select a recipe: ")
    return BASE_PATH / category / f"{recipe}.txt"


def create_recipe():
    category = select_from_list(list_categories(), "Select a category: ")
    recipe_name = input("Enter the name of the new recipe: ").strip()
    create_file(BASE_PATH / category / f"{recipe_name}.txt")


def create_category():
    new_category = input("Enter the name of the new category: ").strip()
    category_path = BASE_PATH / new_category
    try:
        category_path.mkdir()
        print("Category created successfully.")
    except FileExistsError:
        print("❌ Category already exists.")


def delete_recipe():
    path_file = read_recipe()
    try:
        path_file.unlink()
        print("✅ File deleted successfully")
    except FileNotFoundError:
        print("❌ File does not exist")
    except PermissionError:
        print("❌ Permission denied")
    except IsADirectoryError:
        print("❌ This is a directory, not a file")
    except OSError as e:
        print(f"❌ OS error: {e}")


def delete_category():
    category = select_from_list(
        list_categories(), "Select a category to delete: ")
    path_category = BASE_PATH / category
    try:
        path_category.rmdir()
        print(f"✅ Folder '{path_category.name}' deleted successfully")
    except FileNotFoundError:
        print("❌ Folder does not exist")
    except OSError:
        print("❌ Folder is not empty or cannot be deleted")


def show_menu():
    print("       WELCOME TO THE RECIPE MANAGER       ")
    print(f"Folder path: {BASE_PATH}")
    print(f"Total recipes: {len(count_recipes())}")
    print("[1] - Read recipe")
    print("[2] - Create recipe")
    print("[3] - Create category")
    print("[4] - Delete recipe")
    print("[5] - Delete category")
    print("[6] - Exit program")
    print("==========================================")


return_to_menu = True

while True:
    if return_to_menu:
        clear_screen()
        show_menu()

    option = get_option()

    if option == 6:
        print("Program finished...")
        break

    match option:
        case 1:
            print("=== READ RECIPE ===")
            read_file(read_recipe())
            return_to_menu = wait_and_return()
        case 2:
            print("=== CREATE RECIPE ===")
            create_recipe()
            return_to_menu = wait_and_return()
        case 3:
            print("=== CREATE CATEGORY ===")
            create_category()
            return_to_menu = wait_and_return()
        case 4:
            print("=== DELETE RECIPE ===")
            delete_recipe()
            return_to_menu = wait_and_return()
        case 5:
            print("=== DELETE CATEGORY ===")
            delete_category()
            return_to_menu = wait_and_return()
        case _:
            print("You must select a valid input.")
            return_to_menu = wait_and_return()
