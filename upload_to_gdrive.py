#!/usr/bin/env python3
"""
upload_to_gdrive.py

Загружает указанный файл (по умолчанию results.csv) в Google Drive используя
Service Account JSON, переданный через переменную окружения GDRIVE_SERVICE_ACCOUNT_JSON.

Требуется:
- Включить Drive API в Google Cloud Console.
- Создать Service Account и скачать JSON. Добавить JSON в Secrets GitHub как GDRIVE_SERVICE_ACCOUNT_JSON.
- (Опционально) укажите GDRIVE_FOLDER_ID — ID папки в Google Drive, куда загружать.
  Убедитесь, что вы поделились этой папкой с email сервисного аккаунта (service-account@...).
"""
import os
import json
import argparse
import tempfile
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def load_service_account_json_from_env(env_var='GDRIVE_SERVICE_ACCOUNT_JSON'):
    data = os.environ.get(env_var)
    if not data:
        raise RuntimeError(f"Environment variable {env_var} is not set")
    return data

def upload_file(service, local_path, folder_id=None):
    file_metadata = {'name': os.path.basename(local_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(local_path, mimetype='text/csv', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='results.csv', help='Path to file to upload')
    parser.add_argument('--env', default='GDRIVE_SERVICE_ACCOUNT_JSON', help='Env var with SA JSON')
    parser.add_argument('--folder', default=None, help='Drive folder ID (optional)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    sa_json_text = load_service_account_json_from_env(args.env)
    
    # Validate JSON format
    try:
        json.loads(sa_json_text)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in service account data: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Save JSON to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(sa_json_text)
        sa_path = f.name

    try:
        credentials = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
        folder_id = args.folder or os.environ.get('GDRIVE_FOLDER_ID')
        uploaded = upload_file(service, args.file, folder_id)
        file_id = uploaded.get('id')
        web_link = uploaded.get('webViewLink') or f"https://drive.google.com/file/d/{file_id}/view"
        print(f"Uploaded file id: {file_id}")
        print(f"File link: {web_link}")
    except Exception as e:
        print("Upload failed:", e, file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            os.remove(sa_path)
        except Exception:
            pass

if __name__ == '__main__':
    main()