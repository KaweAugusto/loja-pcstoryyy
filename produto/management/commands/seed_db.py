# produto/management/commands/seed_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from produto.models import Categoria, Produto

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais (superuser, categorias e produtos)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando a população do banco de dados...'))

        # 1. Cria o superusuário
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Superusuário "admin" criado com senha "admin123"'))
        else:
            self.stdout.write(self.style.WARNING('ℹ️ Superusuário "admin" já existe.'))

        # 2. Cria as categorias
        categorias_para_criar = ['Placas-mãe', 'Placas de vídeo', 'Periféricos', 'Outros Componentes']
        for nome_cat in categorias_para_criar:
            Categoria.objects.get_or_create(nome=nome_cat)
        self.stdout.write(self.style.SUCCESS(f'✅ Categorias garantidas no banco: {Categoria.objects.count()}'))

        # 3. Cria os produtos
        produtos = [
            ('ASUS TUF Gaming B550M-PLUS', 'Placa-mãe AM4 micro-ATX.', 'Placas-mãe', 849.90, 10),
            ('MSI MAG B460 Tomahawk', 'Placa-mãe LGA1200 ATX.', 'Placas-mãe', 999.90, 8),
            ('NVIDIA RTX 4060', 'Placa de vídeo 8GB GDDR6.', 'Placas de vídeo', 2399.90, 5),
            ('AMD Radeon RX 7600', 'Placa de vídeo 8GB com RDNA 3.', 'Placas de vídeo', 1999.90, 6),
            ('Logitech G502 Mouse', 'Mouse gamer com sensor HERO.', 'Periféricos', 299.90, 20),
            ('Redragon K552 Teclado', 'Teclado mecânico compacto.', 'Periféricos', 199.90, 18),
            ('Kingston A400 SSD 480GB', 'SSD SATA III 2.5".', 'Outros Componentes', 249.90, 25),
            ('Corsair RM650X Fonte', 'Fonte 650W 80 Plus Gold.', 'Outros Componentes', 549.90, 10),
        ]

        for nome, desc, cat_nome, preco, estoque in produtos:
            try:
                categoria_obj = Categoria.objects.get(nome=cat_nome)
                Produto.objects.get_or_create(
                    nome=nome,
                    defaults={
                        'descricao': desc,
                        'categoria': categoria_obj,
                        'preco': preco,
                        'estoque': estoque,
                        'disponivel': True,
                    }
                )
            except Categoria.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"⚠️ Categoria '{cat_nome}' não encontrada. Pulando produto '{nome}'."))

        self.stdout.write(self.style.SUCCESS(f'✅ Produtos no banco: {Produto.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nPopulação do banco de dados concluída!'))