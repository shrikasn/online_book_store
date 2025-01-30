from fastapi import FastAPI
from users.views import router as user_router
from authors.views import router as author_router
from books.views import router as books_router
from feedback.views import router as feedback_router  # Importing feedback router
from orders.view import router as orders_router  # Importing orders router


app = FastAPI()

# Include routers for different sections of the app
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(author_router, prefix="/authors", tags=["Authors"])
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])  # Adding feedback router
app.include_router(orders_router, prefix="/orders", tags=["Orders"])  # Adding orders router

