# Own imports (Routes)
from .file.routes import router as file_router
from .home.routes import router as home_router
from .product.routes import router as product_router

# Own imports (Models)
from .file.models import models as file_models
from .home.models import models as home_models
from .product.models import models as product_models

routers = [
    file_router,
    home_router,
    product_router,
]

models = [
    *file_models,
    *home_models,
    *product_models,
]
