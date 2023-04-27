from .category import category_paginator_ikb
from .brand import brand_paginator_ikb
from .model import brand_model_paginator_ikb
from .product import product_paginator_ikb, product_detail_ikb
from .sex import sex_ikb


__all__: list[str] = [
    'brand_paginator_ikb',
    'brand_model_paginator_ikb',
    'category_paginator_ikb',
    'product_detail_ikb',
    'product_paginator_ikb',
    'sex_ikb',
]
