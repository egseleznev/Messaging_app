﻿#pragma once
#include "pch.h"
#include "Message.h"

class Session
{
private:
	// Идентификатор сессии (задается сервером)
	int session_id;
	// Очередь  сообщений
	queue<Message> messages;
	// Критическая секция для защиты очереди от одновременного использования
	CRITICAL_SECTION criricalSection;
	// Последнее время активности клиента
	clock_t  time;
public:
	// Конструктор по умолчанию
	Session() {
		session_id = 0;
		InitializeCriticalSection(&criricalSection);
	}

	// Конструктор с параметрами
	Session(int ID, clock_t t)
		:session_id(ID), time(t) {
		InitializeCriticalSection(&criricalSection);
	}

	// Деструктор следящий за уничтожением критической секции 
	~Session() {
		DeleteCriticalSection(&criricalSection);
	}

	// Геттер идентификатора сессии
	int getId() {
		return session_id;
	}

	// Сеттер идентификатора сессии
	void setId(int i) {
		session_id = i;
	}

	// Геттер времени последней активности
	clock_t getTime() {
		return time;
	}


	// Сеттер времени последней активности
	void setTime(clock_t t) {
		time = t;
	}

	// Добавление сообщения в очередь
	void Add(Message& m) {
		EnterCriticalSection(&criricalSection);

		messages.push(m);

		LeaveCriticalSection(&criricalSection);
	}

	// Отправка сообщения
	void send(CSocket& s) {
		EnterCriticalSection(&criricalSection);

		if (messages.empty())
		{
			Message::send(s, session_id, MIDDLEWARE, NODATA);
		}
		else
		{
			messages.front().send(s);
			messages.pop();
		}

		LeaveCriticalSection(&criricalSection);
	}
};

