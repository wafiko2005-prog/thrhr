# Telegram Active Chats Scanner Bot

Бот для сканирования активных чатов в Telegram и сохранения результатов в CSV файл.

## Описание

Этот бот подключается к вашему аккаунту Telegram, сканирует все активные чаты (диалоги, группы, каналы) за указанный период времени и сохраняет информацию о них в CSV файл.

## Функциональность

- ✅ Сканирование активных чатов за последние N дней
- ✅ Определение типа чата (личный, группа, канал, супергруппа)
- ✅ Сохранение результатов в CSV файл
- ✅ Возможность загрузки результатов в Google Drive

## Требования

- Python 3.7+
- Telegram API credentials (API_ID и API_HASH)
- Номер телефона, привязанный к Telegram аккаунту

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/wafiko2005-prog/thrhr.git
cd thrhr
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Получите API credentials:
   - Перейдите на https://my.telegram.org
   - Войдите с помощью вашего номера телефона
   - Перейдите в "API development tools"
   - Создайте новое приложение и получите `api_id` и `api_hash`

## Настройка

Создайте файл `.env` в корне проекта со следующими переменными:

```bash
# Обязательные параметры
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+1234567890

# Опциональные параметры
SESSION_NAME=telegram_scanner
OUTPUT_FILE=results.csv
DAYS_BACK=7
```

Или экспортируйте переменные окружения:

```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
export TELEGRAM_PHONE=+1234567890
```

## Запуск бота

```bash
python bot.py
```

При первом запуске бот попросит вас ввести код подтверждения, который придет в Telegram.

## Параметры

- `TELEGRAM_API_ID` - API ID из my.telegram.org (обязательно)
- `TELEGRAM_API_HASH` - API Hash из my.telegram.org (обязательно)
- `TELEGRAM_PHONE` - Номер телефона в международном формате (опционально, для первой авторизации)
- `SESSION_NAME` - Имя файла сессии (по умолчанию: telegram_scanner)
- `OUTPUT_FILE` - Имя выходного CSV файла (по умолчанию: results.csv)
- `DAYS_BACK` - Количество дней назад для поиска активных чатов (по умолчанию: 7)

## Формат выходного файла

CSV файл содержит следующие колонки:

- `chat_id` - ID чата
- `chat_name` - Название чата
- `chat_type` - Тип чата (user, group, channel, supergroup)
- `last_message_date` - Дата последнего сообщения
- `unread_count` - Количество непрочитанных сообщений

## Загрузка результатов в Google Drive

После сканирования вы можете загрузить результаты в Google Drive:

```bash
python upload_to_gdrive.py --file results.csv
```

Для этого необходимо:
1. Настроить Service Account в Google Cloud Console
2. Установить переменную окружения `GDRIVE_SERVICE_ACCOUNT_JSON` с JSON ключом
3. (Опционально) Установить `GDRIVE_FOLDER_ID` с ID папки в Google Drive

Подробнее см. комментарии в файле `upload_to_gdrive.py`.

## Примеры использования

### Базовое использование

```bash
export TELEGRAM_API_ID=12345678
export TELEGRAM_API_HASH=abcdef1234567890
python bot.py
```

### Сканирование за последние 30 дней

```bash
export DAYS_BACK=30
python bot.py
```

### Полный workflow с загрузкой в Google Drive

```bash
# 1. Сканируем чаты
python bot.py

# 2. Загружаем результаты в Google Drive
python upload_to_gdrive.py --file results.csv
```

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте файлы `.env` или `.session` в репозиторий
- Храните API credentials в безопасном месте
- Используйте переменные окружения для CI/CD
- Файлы сессий содержат токены доступа - храните их в безопасности

## Структура проекта

```
thrhr/
├── bot.py                  # Основной скрипт бота
├── upload_to_gdrive.py    # Скрипт для загрузки в Google Drive
├── requirements.txt       # Python зависимости
├── .gitignore            # Файлы для игнорирования git
├── .env.example          # Пример файла конфигурации
└── README.md             # Документация
```

## Troubleshooting

### Ошибка "Could not find the input entity"
Убедитесь, что у вас есть доступ к чатам, которые вы пытаетесь сканировать.

### Ошибка авторизации
Убедитесь, что правильно ввели код подтверждения из Telegram.

### Ошибка API
Проверьте, что API_ID и API_HASH правильные и активны.

## Лицензия

MIT

## Автор

wafiko2005-prog
