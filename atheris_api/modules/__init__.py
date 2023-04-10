# Own imports (Models)
from .file.models import models as file_models
from .home.models import models as home_models

# Own imports (Routes)
from .file.routes import router as file_router
from .home.routes import router as home_router

routers = [
    file_router,
    home_router,
]

models = [
    *file_models,
    *home_models,
]
