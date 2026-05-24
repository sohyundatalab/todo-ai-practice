import json
from datetime import datetime

# Constants
FILE_PATH = 'todos.json'


def load_todos():
    """Load todos from the JSON file and normalize items."""
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cleaned = []
            for item in data:
                if isinstance(item, dict) and 'task' in item and 'progress' in item:
                    cleaned.append({
                        'task': item['task'],
                        'progress': item.get('progress', '미완료'),
                        'created_at': item.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    })
            return cleaned
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # If the file is corrupted, reset it and start empty
        open(FILE_PATH, 'w', encoding='utf-8').close()
        return []


def save_todos(data):
    """Save todos to the JSON file (single shared function)."""
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def display_menu():
    print('\n할 일 관리 프로그램')
    print('1. 할 일 추가')
    print('2. 할 일 완료')
    print('3. 할 일 삭제')
    print('4. 할 일 목록 보기')
    print('5. 종료')


def get_int_input(prompt, min_value=None, max_value=None):
    """Safely get an integer from user. Returns None on invalid input."""
    val = input(prompt)
    try:
        iv = int(val)
    except ValueError:
        return None
    if (min_value is not None and iv < min_value) or (max_value is not None and iv > max_value):
        return None
    return iv


def add_todo():
    task = input('할 일을 입력하세요: ').strip()
    if not task:
        print('입력이 없습니다. 취소합니다.')
        return
    data = load_todos()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.append({'task': task, 'progress': '미완료', 'created_at': created_at})
    save_todos(data)
    print('추가되었습니다.')


def list_todos():
    data = load_todos()
    if not data:
        print('등록된 할 일이 없습니다.')
        return
    for idx, todo in enumerate(data, start=1):
        status = '완료' if todo.get('progress') == '완료' else '미완료'
        created_at = todo.get('created_at', '')
        print(f"{idx}. {todo.get('task')} ({status}) - 생성일: {created_at}")


def complete_todo():
    data = load_todos()
    if not data:
        print('할 일이 없습니다.')
        return
    list_todos()
    choice = get_int_input(f'완료할 할 일 번호를 입력하세요 (1-{len(data)}): ', 1, len(data))
    if choice is None:
        print('잘못된 입력입니다. 숫자 범위를 확인하세요.')
        return
    index = choice - 1
    data[index]['progress'] = '완료'
    save_todos(data)
    print('완료 처리되었습니다.')


def delete_todo():
    data = load_todos()
    if not data:
        print('할 일이 없습니다.')
        return
    list_todos()
    choice = get_int_input(f'삭제할 할 일 번호를 입력하세요 (1-{len(data)}): ', 1, len(data))
    if choice is None:
        print('잘못된 입력입니다. 숫자 범위를 확인하세요.')
        return
    index = choice - 1
    del data[index]
    save_todos(data)
    print('삭제되었습니다.')


def main():
    while True:
        display_menu()
        choice = get_int_input('선택하세요 (1-5): ', 1, 5)
        if choice is None:
            print('잘못된 선택입니다. 다시 시도해주세요.')
            continue
        if choice == 1:
            add_todo()
        elif choice == 2:
            complete_todo()
        elif choice == 3:
            delete_todo()
        elif choice == 4:
            list_todos()
        elif choice == 5:
            print('프로그램을 종료합니다.')
            break


if __name__ == '__main__':
    main()


# 개선된 점 요약 표
# | 개선점 | 설명 |
# |---|---|
# |함수 분리|메뉴 출력, 파일 불러오기, 파일 저장, 추가, 목록 보기, 완료, 삭제를 각각 함수로 분리하여 가독성 향상|
# |중복 저장 제거|모든 저장 동작을 `save_todos()`로 통합하여 중복 코드 제거|
# |입력 검증 강화|숫자 입력에서 예외를 처리하여 잘못된 입력으로 프로그램이 종료되지 않도록 처리|
# |초급자 친화적 코드|복잡한 문법을 피해 직관적인 함수와 간단한 흐름으로 구성|
# |데이터 정규화|파일 로드 시 항목을 검증하고 생성일을 보장함|
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