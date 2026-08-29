import boto3
from botocore.config import Config
import os
import time

# Перед запуском задайте переменные окружения:
#   export YC_ACCESS_KEY_ID="ваш_access_key"
#   export YC_SECRET_KEY="ваш_secret_key"
# или сделать через vault

YC_ACCESS_KEY_ID = os.environ.get('YC_ACCESS_KEY_ID')
YC_SECRET_KEY = os.environ.get('YC_SECRET_KEY')

if not YC_ACCESS_KEY_ID or not YC_SECRET_KEY:
    raise SystemExit(
        "Ошибка: не заданы переменные окружения YC_ACCESS_KEY_ID и/или YC_SECRET_KEY.\n"
        "Перед запуском выполните:\n"
        "  export YC_ACCESS_KEY_ID='ваш_access_key'\n"
        "  export YC_SECRET_KEY='ваш_secret_key'"
    )

# Эмуляция 1С: генерируем stock.csv
with open('/tmp/stock.csv', 'w') as f:
    f.write('product_id,quantity\n')
    f.write('A001,100\n')
    f.write('A002,200\n')

# Загрузка в S3
s3 = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YC_ACCESS_KEY_ID,
    aws_secret_access_key=YC_SECRET_KEY,
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )
)

try:
    s3.upload_file('/tmp/stock.csv', 'k8s-migration-backup', 'uploads/stock.csv')
    print(f"✅ Uploaded at {time.strftime('%Y-%m-%d %H:%M:%S')}")
except Exception as e:
    print(f"❌ Error: {e}")