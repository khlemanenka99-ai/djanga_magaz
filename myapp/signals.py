from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from myapp.models import Product


@receiver(post_save, sender=Product)
def clear_cache_on_product_add(sender, instance, created, **kwargs):
    if created:
        cache.clear()  # Очищает весь кеш
        # Или, например, очистка конкретных ключей:
        # cache.delete('конкретный ключ')

        print("Кеш очищен после добавления нового продукта.")