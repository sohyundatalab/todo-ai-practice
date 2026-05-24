import json
from datetime import datetime

# Constants
FILE_PATH = "todos.json"


def load_data():
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
                        "created_at": item.get(
                            "created_at",
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                    })

            return cleaned_data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        # Remove the corrupted file and start with an empty list
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return []


def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_todo(todo):
    data = load_data()

    data.append({
        "task": todo["task"],
        "progress": "미완료",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    print("추가되었습니다.")


def complete_todo(index):
    data = load_data()

    if 0 <= index < len(data):
        data[index]["progress"] = "완료"
        save_data(data)
        print("완료 처리되었습니다.")
    else:
        print("잘못된 인덱스입니다.")


def delete_todo(index):
    data = load_data()

    if 0 <= index < len(data):
        del data[index]
        save_data(data)
        print("삭제되었습니다.")
    else:
        print("잘못된 인덱스입니다.")


def print_todos():
    data = load_data()

    if not data:
        print("등록된 할 일이 없습니다.")
        return

    for idx, todo in enumerate(data):
        status = "완료" if todo["progress"] == "완료" else "미완료"
        created_at = todo["created_at"]
        print(f"{idx + 1}. {todo['task']} ({status}) - 생성일: {created_at}")


def main_menu():
    while True:
        print("\n할 일 관리 프로그램")
        print("1. 할 일 추가")
        print("2. 할 일 완료")
        print("3. 할 일 삭제")
        print("4. 할 일 목록 보기")
        print("5. 종료")

        choice = input("선택하세요 (1-5): ")

        if choice == "1":
            task = input("할 일을 입력하세요: ")
            add_todo({"task": task})

        elif choice == "2":
            index = int(input("완료할 할 일 인덱스를 입력하세요: ")) - 1
            complete_todo(index)

        elif choice == "3":
            index = int(input("삭제할 할 일 인덱스를 입력하세요: ")) - 1
            delete_todo(index)

        elif choice == "4":
            print_todos()

        elif choice == "5":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main_menu()