"""Popula o banco com superuser admin/admin123 e 20 produto.
Uso:
1) pip install -r requirements.txt
2) python manage.py migrate
3) python seed_db.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from produto.models import Produto

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser "admin" criado com senha "admin123"')
else:
    print('Superuser "admin" já existe')

produtos = [
    # placas-mãe
    ('ASUS TUF Gaming B550M-PLUS', 'Placa-mãe AM4 micro-ATX', 'placa_mae', 849.90, 10),
    ('MSI MAG B460 Tomahawk', 'Placa-mãe LGA1200 ATX', 'placa_mae', 999.90, 8),
    ('Gigabyte A520M S2H', 'Placa-mãe AM4 mATX', 'placa_mae', 499.90, 15),
    ('ASRock B450M Steel Legend', 'Placa-mãe AM4 mATX', 'placa_mae', 599.90, 12),
    ('Biostar B660GTA', 'Placa-mãe LGA1700 micro-ATX', 'placa_mae', 749.90, 7),
    # placas de vídeo
    ('NVIDIA RTX 4060', 'Placa de vídeo 8GB GDDR6', 'placa_video', 2399.90, 5),
    ('AMD Radeon RX 7600', 'Placa de vídeo 8GB', 'placa_video', 1999.90, 6),
    ('NVIDIA GTX 1660 Super', 'Placa de vídeo 6GB', 'placa_video', 1199.90, 4),
    ('ASUS Dual Radeon RX 6700 XT', 'Placa de vídeo 12GB', 'placa_video', 2899.90, 3),
    ('MSI Ventus RTX 3060', 'Placa de vídeo 12GB', 'placa_video', 1699.90, 4),
    # periféricos
    ('Logitech G502 Mouse', 'Mouse gamer com sensor HERO', 'periferico', 299.90, 20),
    ('Redragon K552 Teclado', 'Teclado mecânico compacto', 'periferico', 199.90, 18),
    ('HyperX Cloud II Headset', 'Headset com som 7.1', 'periferico', 399.90, 10),
    ('Razer DeathAdder V2', 'Mouse gamer ergonômico', 'periferico', 349.90, 14),
    ('Corsair K70 RGB', 'Teclado mecânico com iluminação', 'periferico', 999.90, 7),
    # outros
    ('Kingston A400 SSD 480GB', 'SSD SATA III 2.5"', 'outros', 249.90, 25),
    ('Seagate Barracuda 1TB', 'HD 7200RPM 3.5"', 'outros', 219.90, 30),
    ('Corsair RM650X Fonte', 'Fonte 650W 80 Plus Gold', 'outros', 549.90, 10),
    ('Crucial 16GB DDR4', 'Kit 2x8GB 3200MHz', 'outros', 329.90, 16),
    ('Noctua NH-D15', 'Cooler para CPU de alto desempenho', 'outros', 499.90, 5),
]

for nome, desc, cat, preco, estoque in produtos:
    Produto.objects.create(nome=nome, descricao=desc, categoria=cat, preco=preco, estoque=estoque, imagem='')
print('Produtos criados:', Produto.objects.count())
