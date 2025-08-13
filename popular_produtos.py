import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from produto.models import Produto, Categoria

User = get_user_model()

# 1. Cria o superusuário se ele não existir
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuário "admin" criado com senha "admin123"')
else:
    print('ℹ️ Superusuário "admin" já existe')

# 2. Define as categorias que queremos criar
categorias_para_criar = [
    'Placas-mãe',
    'Placas de vídeo',
    'Periféricos',
    'Outros'
]
for nome_cat in categorias_para_criar:
    # get_or_create evita a criação de categorias duplicadas
    Categoria.objects.get_or_create(nome=nome_cat)
print(f'✅ Categorias garantidas no banco: {Categoria.objects.count()}')

# 3. Define os produtos, associando-os pelo nome da categoria
produtos = [
    ('ASUS TUF Gaming B550M-PLUS', 'Placa-mãe AM4 micro-ATX', 'Placas-mãe', 849.90, 10),
    ('MSI MAG B460 Tomahawk', 'Placa-mãe LGA1200 ATX', 'Placas-mãe', 999.90, 8),
    ('NVIDIA RTX 4060', 'Placa de vídeo 8GB GDDR6', 'Placas de vídeo', 2399.90, 5),
    ('AMD Radeon RX 7600', 'Placa de vídeo 8GB', 'Placas de vídeo', 1999.90, 6),
    ('Logitech G502 Mouse', 'Mouse gamer com sensor HERO', 'Periféricos', 299.90, 20),
    ('Redragon K552 Teclado', 'Teclado mecânico compacto', 'Periféricos', 199.90, 18),
    ('Kingston A400 SSD 480GB', 'SSD SATA III 2.5"', 'Outros', 249.90, 25),
    ('Seagate Barracuda 1TB', 'HD 7200RPM 3.5"', 'Outros', 219.90, 30),
]

# 4. Cria os produtos se eles não existirem
for nome, desc, cat_nome, preco, estoque in produtos:
    # Busca o objeto Categoria pelo nome
    categoria_obj = Categoria.objects.get(nome=cat_nome)
    # Cria o produto usando o objeto Categoria
    Produto.objects.get_or_create(
        nome=nome,
        defaults={
            'descricao': desc,
            'categoria': categoria_obj,
            'preco': preco,
            'estoque': estoque,
        }
    )
print(f'✅ Produtos no banco: {Produto.objects.count()}')