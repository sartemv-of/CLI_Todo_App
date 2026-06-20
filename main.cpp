import sys
from manager import TaskManager
from models import TaskPriority, TaskStatus

def print_menu() -> None:
    print("\n" + "="*30)
    print(" CLI TODO ADVANCED")
    print("="*30)
    print("1. Показать все задачи")
    print("2. Добавить новую задачу")
    print("3. Начать выполнение (В процессе)")
    print("4. Завершить задачу (Выполнено)")
    print("5. Удалить задачу")
    print("0. Выход из приложения")
    print("="*30)

def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Выберите действие (0-5): ").strip()

        match choice:
            case "1":
                tasks = manager.get_all_tasks()
                if not tasks:
                    print("\nСписок задач пока пуст.")
                else:
                    print("\nВАШИ ЗАДАЧИ:")
                    for task in tasks:
                        print(task)

            case "2":
                print("\nСОЗДАНИЕ ЗАДАЧИ")
                title = input("Введите название задачи: ").strip()
                description = input("Введите описание (опционально): ").strip()

                print("Приоритеты: 1 - Низкий, 2 - Средний, 3 - Высокий")
                p_choice = input("Выберите приоритет (по умолчанию Средний): ").strip()
                priority = TaskPriority.MEDIUM
                if p_choice == "1": priority = TaskPriority.LOW
                elif p_choice == "3": priority = TaskPriority.HIGH

                try:
                    new_task = manager.add_task(title, description, priority)
                    print(f"\n✅ Задача успешно добавлена! ID: {new_task.id}")
                except ValueError as e:
                    print(f"\n❌ Ошибка: {e}")

            case "3" | "4":
                action = "start" if choice == "3" else "complete"
                print(f"\n🔄 ИЗМЕНЕНИЕ СТАТУСА")

                try:
                    task_id = int(input("Введите ID задачи: ").strip())

                    target_task = None
                    for t in manager.get_all_tasks():
                        if t.id == task_id:
                            target_task = t
                            break

                    if target_task:
                        if action == "start":
                            target_task.in_progress()
                            print(f"\n🟡 Задача [{task_id}] переведена в статус 'В процессе'.")
                        else:
                            target_task.complete()
                            print(f"\n🟢 Задача [{task_id}] успешно выполнена!")
                            manager.save_tasks()
                    else:
                        print(f"\n❌ Задача с ID {task_id} не найдена.")
                except ValueError:
                    print("\n❌ Ошибка: ID должен быть целым числом.")

            case "5":
                print("\n❌ УДАЛЕНИЕ ЗАДАЧИ")
                try:
                    task_id = int(input("Введите ID задачи для удаления: ").strip())
                    if manager.remove_task(task_id):
                        print(f"\n🗑️ Задача [{task_id}] успешно удалена.")
                    else:
                        print(f"\n❌ Задача с ID {task_id} не найдена.")
                except ValueError:
                    print("\n❌ Ошибка: ID должен быть целым числом.")

            case "0":
                print("\n👋 До свидания! Программа завершена. Все данные сохранены.")
                sys.exit()

            case _:
                print("\n⚠️ Некорректный ввод. Пожалуйста, введите число от 0 to 5.")

if __name__ == "__main__":
    main()
