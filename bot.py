#!/usr/bin/env python3
"""
Telegram Bot для сканирования активных чатов
Сканирует активные чаты пользователя и сохраняет результаты в CSV файл
"""
import os
import sys
import csv
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel

# Настройки из переменных окружения
API_ID = os.environ.get('TELEGRAM_API_ID')
API_HASH = os.environ.get('TELEGRAM_API_HASH')
PHONE = os.environ.get('TELEGRAM_PHONE')
SESSION_NAME = os.environ.get('SESSION_NAME', 'telegram_scanner')
OUTPUT_FILE = os.environ.get('OUTPUT_FILE', 'results.csv')
DAYS_BACK = int(os.environ.get('DAYS_BACK', '7'))

async def scan_active_chats(client):
    """Сканирует активные чаты за последние N дней"""
    print(f"Сканирование активных чатов за последние {DAYS_BACK} дней...")
    
    results = []
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
    
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        
        # Проверяем дату последнего сообщения
        if dialog.date and dialog.date >= cutoff_date:
            chat_type = 'unknown'
            chat_name = dialog.name or 'Без имени'
            chat_id = dialog.id
            
            if isinstance(entity, User):
                chat_type = 'user'
            elif isinstance(entity, Chat):
                chat_type = 'group'
            elif isinstance(entity, Channel):
                chat_type = 'channel' if entity.broadcast else 'supergroup'
            
            results.append({
                'chat_id': chat_id,
                'chat_name': chat_name,
                'chat_type': chat_type,
                'last_message_date': dialog.date.strftime('%Y-%m-%d %H:%M:%S'),
                'unread_count': dialog.unread_count
            })
            
            print(f"Найден активный чат: {chat_name} ({chat_type})")
    
    return results

async def save_to_csv(results, filename):
    """Сохраняет результаты в CSV файл"""
    if not results:
        print("Активные чаты не найдены")
        return
    
    print(f"\nСохранение {len(results)} активных чатов в {filename}...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chat_id', 'chat_name', 'chat_type', 'last_message_date', 'unread_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    
    print(f"Результаты сохранены в {filename}")

async def main():
    """Основная функция бота"""
    # Проверка необходимых переменных окружения
    if not API_ID or not API_HASH:
        print("Ошибка: Необходимо установить TELEGRAM_API_ID и TELEGRAM_API_HASH", file=sys.stderr)
        sys.exit(1)
    
    print("Запуск Telegram бота для сканирования активных чатов...")
    print(f"API ID: {'*' * 8 if API_ID else 'Не установлен'}")
    print(f"Телефон: {PHONE[:4] + '***' + PHONE[-4:] if PHONE and len(PHONE) > 8 else 'Не указан'}")
    
    # Создаем клиента
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # Подключаемся к Telegram
        await client.start(phone=PHONE)
        
        # Проверяем авторизацию
        if not await client.is_user_authorized():
            print("Ошибка: Не удалось авторизоваться", file=sys.stderr)
            sys.exit(1)
        
        me = await client.get_me()
        print(f"Авторизован как: {me.first_name} (@{me.username})")
        
        # Сканируем чаты
        results = await scan_active_chats(client)
        
        # Сохраняем результаты
        await save_to_csv(results, OUTPUT_FILE)
        
        print("\n✅ Сканирование завершено успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
