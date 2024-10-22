from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Product Model class
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    quantity: int

# Order Model class
class Order(BaseModel):
    product_id: int
    quantity: int

# In-memory database to store products
products = [
    Product(id=1, name="Apple", price=150, quantity=20),
    Product(id=2, name="Banana", price=50, quantity=100),
]

# In-memory database to store orders
orders = []

# Endpoint to get all products
@app.get("/products/", response_model=List[Product])
def get_products():
    return products

# Endpoint to get a product by ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# Endpoint to add a new product
@app.post("/products/", response_model=Product)
def add_product(product: Product):
    # Assigning a new ID by incrementing the max current ID
    product.id = max([p.id for p in products]) + 1 if products else 1
    products.append(product)
    return product

# Endpoint to update a product by ID
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    for idx, product in enumerate(products):
        if product.id == product_id:
            updated_product.id = product_id
            products[idx] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

# Endpoint to delete a product by ID
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for idx, product in enumerate(products):
        if product.id == product_id:
            del products[idx]
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

# Endpoint to add an order
@app.post("/orders/", response_model=Order)
def add_order(order: Order):
    # Check if the product exists and if enough quantity is available
    for product in products:
        if product.id == order.product_id:
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                orders.append(order)
                return order
            else:
                raise HTTPException(status_code=400, detail="Not enough quantity available")
    raise HTTPException(status_code=404, detail="Product not found")

# Endpoint to get all orders
@app.get("/orders/", response_model=List[Order])
def get_orders():
    return orders

# Endpoint to access the admin dashboard
@app.get("/admin-dashboard")
def admin_dashboard():
    return {"message": "Welcome to the Admin Dashboard. You can manage products and orders here."}
