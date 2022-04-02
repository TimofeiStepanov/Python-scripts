#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
simple sandbox escape example.
"""


def main():
    text = input('>>> ')
    for keyword in ['eval', 'exec', 'import', 'open', 'os', 'read', 'system', 'write', 'subprocess']:
        if keyword in text:
            print('No!!!')
            print(f'{keyword} is banned!')
            return
    else:
        exec(text, {"__builtins__": {}}, {})
        return


GREEN = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[91m'
ENDC = '\033[0m'
if __name__ == '__main__':
    print(
        f'{WARNING}Привет! Жестокие люди из HackerU посадили тебя в песочницу с питоном\nтебя выпустят из песочницы, если ты сдашь флаг!\nтебе еще повезло: вот код программы:{ENDC}')
    print('-' * 200)
    print(open(__file__).read(500))
    print('-' * 200)
    print('вводи свои догадки:')
    while 1:
        try:
            main()
        except Exception as e:
            print(f"Ой! что-то сломалось!\n{ERROR}{e}{ENDC}")
