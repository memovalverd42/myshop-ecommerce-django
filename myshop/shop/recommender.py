import redis
from django.conf import settings
from .models import Product
from typing import List

# Coneccion to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class Recommender:
    def get_product_key(self, id: int) -> str:
        return f'product:{id}:purchased_with'
    
    def products_bought(self, products: List[Product]) -> None:
        product_ids: List[int] = [p.id for p in products]
        
        for product_id in product_ids:
            for with_id in product_ids:
                # Obtener productos comprados con cada producto
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),
                              1,
                              with_id)
                    
    def suggest_products_for(self, products: List[Product], max_results=6) -> List[Product]:
        
        product_ids: List[int] = [p.id for p in products]
        
        if len(products) == 1:
            suggestions = r.zrange(
                            self.get_product_key(product_ids[0]),
                            0, -1, desc=True)[:max_results]
            
        else:
            # Generamos una key temporal
            flat_ids = ''.join([str(id)] for id in product_ids)
            tmp_key = f'tmp_{flat_ids}'
            
            # Multiples productos, combinar puntajes de todos los 
            # productos guardados resultado de ordenar con la key temporal
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            
            r.zrem(tmp_key, *product_ids)
            
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            
            r.delete(tmp_key)
            
        suggested_products_ids = [int(id) for id in suggestions]
        
        suggested_products: List[Product] = list(Product.objects.filter(
                                id__in=suggested_products_ids))
        
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        
        return suggested_products
    
    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
            
            
            
            