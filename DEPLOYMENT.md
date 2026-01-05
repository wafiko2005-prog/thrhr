# Руководство по развертыванию и использованию Telegram Bot Scanner

## Быстрый старт

### 1. Получение API credentials для Telegram

1. Перейдите на https://my.telegram.org
2. Войдите используя ваш номер телефона
3. Перейдите в раздел "API development tools"
4. Создайте новое приложение:
   - App title: Telegram Scanner
   - Short name: scanner
   - Platform: Other
5. Сохраните `api_id` и `api_hash`

### 2. Локальный запуск

```bash
# Клонировать репозиторий
git clone https://github.com/wafiko2005-prog/thrhr.git
cd thrhr

# Установить зависимости
pip install -r requirements.txt

# Создать файл .env на основе .env.example
cp .env.example .env

# Отредактировать .env и добавить свои credentials
nano .env  # или любой другой редактор

# Запустить бота
python bot.py

# Или использовать удобный скрипт
./run_bot.sh
```

### 3. Первый запуск и авторизация

При первом запуске бот попросит вас:
1. Ввести номер телефона (если не указан в .env)
2. Ввести код подтверждения из Telegram
3. Возможно, ввести пароль двухфакторной аутентификации

После успешной авторизации создастся файл сессии (`.session`), и при следующих запусках авторизация не потребуется.

⚠️ **Важно**: Файл сессии содержит токены доступа. Храните его в безопасности!

## Настройка GitHub Actions

Для автоматического запуска бота через GitHub Actions:

### 1. Добавить Secrets в GitHub

Перейдите в Settings → Secrets and variables → Actions → New repository secret

Добавьте следующие секреты:

- `TELEGRAM_API_ID` - ваш API ID
- `TELEGRAM_API_HASH` - ваш API Hash
- `TELEGRAM_PHONE` - номер телефона (опционально)

Для загрузки в Google Drive (опционально):
- `GDRIVE_SERVICE_ACCOUNT_JSON` - JSON ключ Service Account
- `GDRIVE_FOLDER_ID` - ID папки в Google Drive

### 2. Создание Session File для GitHub Actions

Поскольку GitHub Actions не может интерактивно авторизоваться:

**Вариант А: Локальная авторизация и сохранение сессии**

1. Запустите бот локально один раз для создания session файла
2. Закодируйте session file в base64:
   ```bash
   base64 telegram_scanner.session > session.txt
   ```
3. Добавьте содержимое session.txt как GitHub Secret `TELEGRAM_SESSION_BASE64`
4. Обновите workflow для декодирования сессии перед запуском

**Вариант Б: Использовать bot token вместо user session**

Если требуется полная автоматизация, рассмотрите использование Telegram Bot API вместо user account.

### 3. Запуск workflow

- **Автоматический**: Workflow запускается ежедневно в 00:00 UTC
- **Ручной**: Перейдите в Actions → Telegram Bot Scanner → Run workflow

## Настройка Google Drive для загрузки результатов

### 1. Создание Service Account

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google Drive API:
   - API & Services → Enable APIs and Services
   - Найдите "Google Drive API" и включите
4. Создайте Service Account:
   - IAM & Admin → Service Accounts → Create Service Account
   - Дайте имя: telegram-uploader
   - Grant this service account access: Project → Editor (опционально)
   - Create and download JSON key

### 2. Настройка доступа к папке

1. Создайте папку в Google Drive
2. Откройте JSON ключ и найдите поле `client_email`
3. Поделитесь папкой с этим email адресом (дайте права Editor)
4. Скопируйте ID папки из URL (часть после `/folders/`)

### 3. Добавление credentials

**Для локального использования:**

```bash
export GDRIVE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
export GDRIVE_FOLDER_ID='your_folder_id'
```

**Для GitHub Actions:**

Добавьте весь JSON (одной строкой) как GitHub Secret `GDRIVE_SERVICE_ACCOUNT_JSON`

## Параметры конфигурации

### Переменные окружения

| Переменная | Обязательна | По умолчанию | Описание |
|------------|-------------|--------------|----------|
| TELEGRAM_API_ID | Да | - | API ID из my.telegram.org |
| TELEGRAM_API_HASH | Да | - | API Hash из my.telegram.org |
| TELEGRAM_PHONE | Нет | - | Номер телефона для авторизации |
| SESSION_NAME | Нет | telegram_scanner | Имя файла сессии |
| OUTPUT_FILE | Нет | results.csv | Имя выходного файла |
| DAYS_BACK | Нет | 7 | Дней назад для поиска активных чатов |
| GDRIVE_SERVICE_ACCOUNT_JSON | Нет | - | JSON Service Account для Google Drive |
| GDRIVE_FOLDER_ID | Нет | - | ID папки в Google Drive |

## Формат выходных данных

CSV файл содержит следующие поля:

```csv
chat_id,chat_name,chat_type,last_message_date,unread_count
-1001234567890,My Channel,channel,2026-01-05 10:30:00,0
1234567890,John Doe,user,2026-01-05 09:15:00,3
-987654321,Project Group,group,2026-01-04 18:45:00,12
```

## Примеры использования

### Сканирование за последний месяц

```bash
export DAYS_BACK=30
python bot.py
```

### Сохранение в другой файл

```bash
export OUTPUT_FILE=my_chats.csv
python bot.py
```

### Полный цикл с загрузкой в Drive

```bash
# 1. Сканируем чаты
python bot.py

# 2. Загружаем в Google Drive
python upload_to_gdrive.py --file results.csv

# Или одной командой через скрипт
./run_bot.sh
```

## Troubleshooting

### "Ошибка: Необходимо установить TELEGRAM_API_ID и TELEGRAM_API_HASH"

Убедитесь, что переменные окружения установлены или файл `.env` существует и содержит корректные значения.

### "Error: Could not find the input entity"

Убедитесь, что:
1. У вас есть доступ к чатам
2. Session файл актуален
3. Вы авторизованы правильным аккаунтом

### "FloodWaitError"

Telegram ограничивает частоту запросов. Подождите указанное время и повторите попытку.

### GitHub Actions не может авторизоваться

GitHub Actions не может интерактивно авторизоваться. Вам нужно:
1. Создать session файл локально
2. Закодировать его в base64 и добавить как GitHub Secret
3. Обновить workflow для использования этой сессии

### "Upload failed" при загрузке в Google Drive

Проверьте:
1. Service Account JSON корректен
2. Drive API включен в Google Cloud Console
3. Папка существует и доступна Service Account email
4. GDRIVE_FOLDER_ID правильный

## Безопасность

⚠️ **Критически важно:**

1. **Никогда не коммитьте:**
   - Файлы `.env`
   - Файлы `.session`
   - Service Account JSON
   - API credentials

2. **Используйте .gitignore:**
   - Уже настроен в репозитории
   - Проверяйте перед каждым коммитом

3. **GitHub Secrets:**
   - Используйте для CI/CD
   - Не выводите в логи
   - Регулярно обновляйте

4. **Session файлы:**
   - Содержат токены доступа
   - Храните как пароли
   - Не передавайте другим

## Дополнительные возможности

### Фильтрация чатов

Можно модифицировать `bot.py` для фильтрации по типу чата:

```python
# Только каналы
if isinstance(entity, Channel) and entity.broadcast:
    results.append(...)

# Только группы
if isinstance(entity, Chat):
    results.append(...)
```

### Экспорт в другие форматы

Можно добавить экспорт в JSON или Excel:

```python
import json

# JSON экспорт
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

## Лицензия

MIT License

## Поддержка

Если у вас возникли проблемы:
1. Проверьте этот документ
2. Посмотрите Issues на GitHub
3. Создайте новый Issue с описанием проблемы
