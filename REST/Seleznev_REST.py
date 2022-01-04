# -*- coding: cp1251 -*-
from msg import *
from utils import *
import threading
import time
from api import *
import sys

server_api = Api();


def listenServer():
    while True:
        m = server_api.Get();
        if m['result'] != None:
            safe_print(f'��������� �� {m["result"]["id"]}:\n{m["result"]["message"]}');
        time.sleep(2);


def connect():
    server_api.Init();
    safe_print(f'������ ���������');
    safe_print(f'ID: {server_api.ClientID}');
    messages_thread = threading.Thread(target=listenServer, daemon=True);
    messages_thread.start();


def process():
    connect();
    while (True):
        safe_print('[1] ��������� ���������\n[2] �������� ��� ���������\n[3] �����\n');
        answer = int(input());

        if answer == 1:
            safe_print('[1] ������ ��� ������ �������\n[2] ��� ���� ��������\n');

            answer_2 = int(input());

            if answer_2 == 1:
                safe_print('\n������� ID �������\n ');
                c_id = int(input());
                
                safe_print('\n������� ���������\n ')
                message = input();
                
                server_api.Post(c_id, message);
                safe_print('\n�������\n');

                continue

            if answer_2 == 2:
                safe_print('\n������� ���������\n')
                message = input();
                
                server_api.Post(int(Addresses.BROADCAST), message);
                safe_print('\n�������\n');

                continue
            continue
        if answer == 2:
            print('������� ���������')
            messages = server_api.GetAll()['result'];
            for m in messages:
                if (m[1] != (int)(MessageTypes.CONFIRM) and m[1] != (int)(MessageTypes.NODATA)):
                    if(int(m[0])!=server_api.ClientID):
                        safe_print(f'��������� �� ������� {m[0]}:\n{m[2]}');
                    else:  
                        safe_print(f'��������� ��� ������� {m[1]}:\n{m[2]}');
            continue
        if answer == 3:
            server_api.Exit();
            safe_print('������ ���������\n\n');
            return
        safe_print('������� 1-3 \n\n');


if __name__ == '__main__':
    process();
