import os

def check_structure():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current dir: {current_dir}")
    
    # Перевіряємо всі файли
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(current_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

if __name__ == "__main__":
    check_structure()
