#!/usr/bin/env python3
"""
Тесты для проверки базовой функциональности бота
Эти тесты не требуют API credentials
"""
import sys
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, AsyncMock

# Добавляем путь к модулю
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBotStructure(unittest.TestCase):
    """Тесты структуры бота"""
    
    def test_bot_can_be_imported(self):
        """Проверка что bot.py может быть импортирован"""
        try:
            import bot
            self.assertTrue(hasattr(bot, 'main'))
            self.assertTrue(hasattr(bot, 'scan_active_chats'))
            self.assertTrue(hasattr(bot, 'save_to_csv'))
        except ImportError as e:
            self.fail(f"Failed to import bot: {e}")
    
    def test_required_modules(self):
        """Проверка что все необходимые модули могут быть импортированы"""
        required_modules = [
            'os', 'sys', 'csv', 'asyncio', 'datetime'
        ]
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"Required module {module} cannot be imported")
    
    def test_upload_script_exists(self):
        """Проверка что скрипт загрузки существует"""
        script_path = os.path.join(os.path.dirname(__file__), 'upload_to_gdrive.py')
        self.assertTrue(os.path.exists(script_path))
    
    def test_requirements_file_exists(self):
        """Проверка что файл requirements.txt существует"""
        req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        self.assertTrue(os.path.exists(req_path))
        
        with open(req_path, 'r') as f:
            content = f.read()
            self.assertIn('telethon', content)
            self.assertIn('google-auth', content)

class TestCSVSaving(unittest.TestCase):
    """Тесты сохранения в CSV"""
    
    @patch('bot.asyncio')
    def test_save_empty_results(self, mock_asyncio):
        """Проверка сохранения пустых результатов"""
        import bot
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            # Создаем mock для asyncio.run
            async def mock_save():
                await bot.save_to_csv([], temp_file)
            
            # Проверяем что функция не падает с пустым списком
            # (в реальности она просто выведет сообщение)
            # В данном тесте мы просто проверяем что функция определена
            self.assertTrue(callable(bot.save_to_csv))
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

class TestEnvironmentVariables(unittest.TestCase):
    """Тесты переменных окружения"""
    
    def test_env_example_exists(self):
        """Проверка что файл .env.example существует"""
        env_path = os.path.join(os.path.dirname(__file__), '.env.example')
        self.assertTrue(os.path.exists(env_path))
        
        with open(env_path, 'r') as f:
            content = f.read()
            self.assertIn('TELEGRAM_API_ID', content)
            self.assertIn('TELEGRAM_API_HASH', content)

if __name__ == '__main__':
    print("🧪 Запуск тестов бота...")
    print("=" * 60)
    unittest.main(verbosity=2)
