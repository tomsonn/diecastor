from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy import UUID, Boolean, Column, DateTime, Float, ForeignKey, String, text


class TierEnum(Enum):
    TOP = "top"
    MIDDLE = "middle"
    LOW = "low"


class ConditionEnum(Enum):
    NEW = "new"
    UNPACKED = "unpacked"
    USED = "used"
    DAMAGED = "damaged"


class PackageEnum(Enum):
    BOX = "box"
    BLISTER = "blister"
    WITHOUT = "withou"


Base = declarative_base()


class Shops(Base):
    __tablename__ = "shops"

    id = Column(UUID, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    ships_to_czech = Column(Boolean, nullable=False)
    shipping_fee = Column(Float, nullable=True)
    other_fees = Column(Float, nullable=True)
    free_shipping_from_price = Column(Float, nullable=False)
    is_in_eu_market = Column(Boolean, nullable=False)


class Models(Base):
    __tablename__ = "models"

    id = Column(UUID, primary_key=True, nullable=False)
    brand_id = Column(UUID, ForeignKey("brands.id"), nullable=False)
    model_id = Column(String, nullable=True)
    car_brand = Column(String, nullable=False)
    category_id = Column(UUID, ForeignKey("categories.id"), nullable=False)
    has_chase_version = Column(Boolean, nullable=False)
    # we won't be storing limited_collection within this table
    # if the model is part of the limited collection will be distingished by the category  
    # limited_collection = Column(String, nullable=True)
    release_year = Column(String, nullable=True)


class Brands(Base):
    __tablename__ = "brands"

    id = Column(UUID, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    tier = Column(SQLEnum(TierEnum), nullable=False)


class Categories(Base):
    __tablename__ = "categories"

    id = Column(UUID, primary_key=True, nullable=False)
    is_limited = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)


# TODO - add history table for the shop products
class ShopProducts(Base):
    __tablename__ = "shop_products"
    id = Column(UUID, primary_key=True, nullable=False)
    shop_id = Column(UUID, ForeignKey("shops.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    price_in_czk = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    model_id = Column(UUID, ForeignKey("models.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
    updated_at = Column(DateTime, nullable=False, server_default=text("NOW()"))
    original_name = Column(String, nullable=False)
    is_last = Column(Boolean, nullable=False)
    condition = Column(SQLEnum(ConditionEnum), nullable=False)
    packaging = Column(SQLEnum(PackageEnum), nullable=False)


class Customers(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    country = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    currency = Column(String, nullable=False)


class CustomerModels(Base):
    __tablename__ = "customer_models"

    id = Column(UUID, primary_key=True, nullable=False)
    model_id = Column(UUID, ForeignKey("models.id"), nullable=False)
    price = Column(Float, nullable=False)
    condition = Column(SQLEnum(ConditionEnum), nullable=False)
    # TODO - add photos
