import argparse
import start_node

if __name__ == '__main__':
    # Разбор передаваемых аргументов
    parser = argparse.ArgumentParser()
    parser.add_argument('server_id', nargs='?')
    args = parser.parse_args().server_id

    # Запускаем сервер с определенным параметром, определяющим номер порта
    start_node.start(int(args))