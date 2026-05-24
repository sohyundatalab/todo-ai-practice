import json
from datetime import datetime

# Constants
FILE_PATH = "todos.json"

def print_menu():
    print("\n할 일 관리 프로그램")
    print("1. 할 일 추가")
    print("2. 할 일 완료")
    print("3. 할 일 삭제")
    print("4. 할 일 목록 보기")
    print("5. 종료")

def load_todos():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Validate and correct data format if necessary
            cleaned_data = []
            for item in data:
                if isinstance(item, dict) and "task" in item:
                    cleaned_data.append({
                        "task": item["task"],
                        "progress": item.get("progress", "미완료"),
                        "created_at": item.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            return cleaned_data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return []

def save_todos(data):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_todo():
    task = input("할 일을 입력하세요: ")
    if task.strip():  # Validate empty input
        todos = load_todos()
        todos.append({
            "task": task,
            "progress": "미완료",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_todos(todos)
        print("추가되었습니다.")
    else:
        print("빈 할 일은 추가할 수 없습니다.")

def complete_todo():
    index = get_todo_number("완료할 할 일 인덱스를 입력하세요: ")
    if index is not None:
        todos = load_todos()
        todos[index]["progress"] = "완료"
        save_todos(todos)
        print("완료 처리되었습니다.")

def delete_todo():
    index = get_todo_number("삭제할 할 일 인덱스를 입력하세요: ")
    if index is not None:
        todos = load_todos()
        del todos[index]
        save_todos(todos)
        print("삭제되었습니다.")

def show_todos():
    todos = load_todos()
    if not todos:
        print("등록된 할 일이 없습니다.")
        return

    for idx, todo in enumerate(todos):
        status = "완료" if todo["progress"] == "완료" else "미완료"
        created_at = todo["created_at"]
        print(f"{idx + 1}. {todo['task']} ({status}) - 생성일: {created_at}")

def get_todo_number(prompt):
    try:
        number = int(input(prompt)) - 1
        todos = load_todos()
        if 0 <= number < len(todos):
            return number
        else:
            print("존재하지 않는 인덱스입니다.")
            return None
    except ValueError:
        print("숫자를 입력해야 합니다.")
        return None

def main_menu():
    while True:
        print_menu()

        choice = input("선택하세요 (1-5): ")

        if choice == "1":
            add_todo()

        elif choice == "2":
            complete_todo()

        elif choice == "3":
            delete_todo()

        elif choice == "4":
            show_todos()

        elif choice == "5":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main_menu()