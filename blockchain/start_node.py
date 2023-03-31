from gevent import monkey
from flask import Flask, request
import time
import threading
import logging
import node
import grequests
import block
import json

monkey.patch_all()


def start(server_id):
    # Создадим сервер
    current_server = Flask(__name__)

    # Создаем текущую node
    current_node = node.Node(server_id)

    # Обозначаем порты и хоста
    if server_id == 1:
        current_port = 5000
        port2 = 5001
        port3 = 5002
    elif server_id == 2:
        current_port = 5001
        port2 = 5000
        port3 = 5002
    else:
        current_port = 5002
        port2 = 5000
        port3 = 5001

    # Убираем сообщения из Log
    logging.getLogger('werkzeug').disabled = True

    host = 'localhost'

    servers_urls = [f'http://{host}:{current_port}/', f'http://{host}:{port2}/', f'http://{host}:{port3}/']

    # Создаем текущую node
    current_node = node.Node(server_id)

    # Функция генерации нового блока текущим сервером
    def new_blocks_generator():
        while True:
            if len(current_node.blocks_array) != 0:
                # Получим текущий последний блок и значение его поля Hash
                last_block = json.loads(current_node.blocks_array[-1])
                prev_hash = last_block['hash']

                # На основе последнего блока сгенерируем новый блок
                new_block = block.create_new_block(current_node.block_index + 1, prev_hash, current_node.server_id,
                                                   server_id)

                # Если сгенерированный нами new_block.index не присутствует еще -> значит мы первые
                if new_block.index > current_node.block_index:
                    # Отправим Асинхронно запрос двум другим серверам с сообщением, содержащим new_block
                    rst = (grequests.post(u, json=new_block.block_to_json()) for u in servers_urls)
                    grequests.map(rst)

            time.sleep(0.2)

    # Сервер будет откликаться на запрос POST к нему
    @current_server.route("/", methods=['POST'])
    def server_handler():
        # Принимаем данные
        received_block = request.get_json()

        # Передаем эти данные Node обработчик
        block_handler_flag = current_node.block_handler(received_block)

        # Мы ничего не получили (такого быть не может) -> выходим
        if not block_handler_flag:
            return "block_handler_flag Error"

        return "We received new Block"

    # Запустим сервер в отдельном потоке
    threading.Thread(target=current_server.run, args=(host, current_port)).start()
    threading.Thread(target=new_blocks_generator).start()
    time.sleep(1)

    # Создадим Генезис, если это первый сервер
    if server_id == 1:
        genesis_block = node.create_genesis()

        # Отправим Асинхронно запрос всем серверам с сообщением, содержащим genesis_block
        rs = (grequests.post(u, json=genesis_block) for u in servers_urls)
        grequests.map(rs)