import json
from datetime import datetime

# Constants
FILE_PATH = 'todos.json'

def load_data():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return validate_data(data)
    except (FileNotFoundError, json.JSONDecodeError):
        # Corrupted file will be removed and an empty list returned
        if not handle_corrupted_file():
            print("파일 처리 중 오류 발생.")
        return []

def handle_corrupted_file():
    try:
        open(FILE_PATH, 'w', encoding='utf-8').close()
        return True
    except Exception as e:
        print(f"파일 초기화 중 오류 발생: {e}")
        return False

def validate_data(data):
    cleaned_data = []
    for item in data:
        if isinstance(item, dict) and 'task' in item and 'progress' in item:
            cleaned_data.append({
                "task": item["task"],
                "progress": item.get("progress", "미완료"),
                "created_at": item.get("created_at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            })
    return cleaned_data

def save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_todo(todo):
    data = load_data()
    todo['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.append({"task": todo["task"], "progress": "미완료"})
    save_data(data)
    print("추가되었습니다.")

def complete_todo(index):
    data = load_data()
    if validate_index(index, data):
        data[index]["progress"] = "완료"
        save_data(data)
        print("완료 처리되었습니다.")

def delete_todo(index):
    data = load_data()
    if validate_index(index, data):
        del data[index]
        save_data(data)
        print("삭제되었습니다.")

def validate_index(index, data):
    if 0 <= index < len(data):
        return True
    print("잘못된 인덱스입니다.")
    return False

def print_todos():
    data = load_data()
    for idx, todo in enumerate(data):
        status = '완료' if todo["progress"] == "완료" else '미완료'
        print(f"{idx + 1}. {todo['task']} ({status}) - 생성일: {todo['created_at']}")

def main_menu():
    while True:
        print("\n할 일 관리 프로그램")
        print("1. 할 일 추가")
        print("2. 할 일 완료")
        print("3. 할 일 삭제")
        print("4. 할 일 목록 보기")
        print("5. 종료")
        choice = input("선택하세요 (1-5): ")

        if choice == '1':
            task = input("할 일을 입력하세요: ")
            add_todo({"task": task})
        elif choice == '2':
            index = get_index_from_user("완료할 할 일 인덱스를 입력하세요: ")
            complete_todo(index)
        elif choice == '3':
            index = get_index_from_user("삭제할 할 일 인덱스를 입력하세요: ")
            delete_todo(index)
        elif choice == '4':
            print_todos()
        elif choice == '5':
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

def get_index_from_user(prompt):
    while True:
        try:
            index = int(input(prompt)) - 1
            return index
        except ValueError:
            print("유효한 숫자를 입력하세요.")

if __name__ == "__main__":
    main_menu()