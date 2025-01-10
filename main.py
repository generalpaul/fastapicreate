from fastapi import FastAPI
import models
from database import engine
from routers import auth, admin, product, user, product_sub

app = FastAPI()
#handler = Mangum(app)

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)

app.include_router(product.router)
app.include_router(product_sub.router)

app.include_router(admin.router)
app.include_router(user.router)
