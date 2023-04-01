import argparse
import start_node
import node
from gevent import monkey
monkey.patch_all()

if __name__ == '__main__':
    # Разбор передаваемых аргументов
    parser = argparse.ArgumentParser()
    parser.add_argument('server_id', nargs='?')
    args = parser.parse_args().server_id

    # Создаем node для текущего сервера
    current_node = node.Node(int(args))

    # Запускаем сервер с определенным параметром, определяющим номер порта
    start_node.start(int(args), current_node)
