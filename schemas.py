from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from datetime import datetime

class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """
    name: str = Field(..., min_length=3, max_length=50, description="Название категории (3-50 символов)")
    parent_id: int | None = Field(None, description="ID родительской категории, если есть")

class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории")
    parent_id: int | None = Field(None,description="ID родительской категории, если есть")
    is_active: bool = Field(..., description="Активность категории")
    model_config = ConfigDict(from_attributes=True)#Настройка ConfigDict(from_attributes=True) обеспечивает совместимость с ORM, позволяя преобразовывать данные из базы в JSON-ответы.

#=============================================================================================
class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах
    """
    name: str = Field(..., min_length=3, max_length=100, description="Название товара (3-100 символов)")
    description: str | None = Field(None, max_length=500, description="Описание товара (до 500 символов)")
    price: Decimal = Field(..., gt = 0, description="Цена товара (больше 0)", decimal_places=2)
    image_url: str | None = Field(None, max_length=200, description="URL изображения товара")
    stock: int = Field(..., ge = 0, description="Количество товара на складе(0 или больше)")
    category_id: int = Field(..., description="ID категории к которой относится товар")
    is_active: bool = Field(True, description="Активность товара (по умолчанию True)")  # ✅ ДОБАВЛЕНО!

class Product(BaseModel):
    """
       Модель для ответа с данными категории.
       Используется в GET-запросах.
       """
    id: int = Field(..., description="Уникальный идентификатор товара")
    name: str = Field(..., description="Название товара", example="Iphone 13")
    description: str | None = Field(None, description="Описание товара")
    price: Decimal = Field(..., description="Цена товара в рублях", gt=0, decimal_places=2, examples=[Decimal("9.77")])
    image_url: str | None = Field(None, description="URL изображение товара")
    stock: int = Field(..., description="ID категории")
    category_id: int = Field(..., description="ID категории")
    is_active: bool = Field(..., description="Активность товара")
    model_config = ConfigDict(from_attributes=True) #настройка обеспечивает совместимость с ORM, позволяя преобразовывать данные из базы в JSON-ответы.

#=============================================================================================
class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer", pattern="^(buyer|seller)$", description="Роль: 'buyer' или 'seller'")


class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
class TokenResponse(BaseModel):
    access_token: str

#================================REVIEW=============================================================
class ReviewCreate(BaseModel):
    """
    Модель для создания и обновления отзыва.
    Используется в POST и PUT запросах
    """

    comment: str| None = Field(None, description="Комментарий к товару", example="Товар отличный, рекомендую!")
    grade: int = Field(..., ge=1, le=5, description="Оценка товара", example=5)
    product_id: int = Field(..., description="ID товара, на который оставляют отзыв", example=1)

class Review(BaseModel):
        """
       Модель для ответа с данными отзыва.
       Используется в GET-запросах.
       """
        id: int = Field(..., description="Уникальный идентификатор отзыва", example=1)
        user_id: int = Field(..., description="Уникальный идентификатор пользователя", example=5)
        product_id: int = Field(..., description="Уникальный идентификатор товара", example=3)
        comment: str|None = Field(None, description="Комментарий пользователя", example="Отличный товар, рекомендую!")
        comment_date: datetime = Field(..., description="Дата написания отзыва", example="2025-08-26T21:30:00Z")
        grade: int = Field(...,description="Оценка товара 1-5", example=5)
        is_active: bool = Field(...,description="Активность отзыва, мягкое удаление")
        model_config = ConfigDict(from_attributes=True)  # настройка обеспечивает совместимость с ORM, позволяя преобразовывать данные из базы в JSON-ответы.
