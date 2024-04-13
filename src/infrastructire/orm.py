from __future__ import annotations

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "inn",
            "kpp",
            name="inn_kpp_unique_index",
            comment="Уникальный индекс ИНН КПП",
        ),
    )
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор компании",
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        comment="Название компании",
    )
    inn = sqlalchemy.Column(
        sqlalchemy.String(12),
        nullable=False,
        comment="ИНН компании",
    )
    kpp = sqlalchemy.Column(
        sqlalchemy.String(9),
        nullable=True,
        comment="КПП компании",
        default=None,
    )
    nests = orm.relationship("TechNest", back_populates="holder")


class Locations(Base):
    __tablename__ = "locations"
    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "address",
            name="inn_kpp_unique_index",
            comment="Уникальный индекс для локации",
        ),
    )
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор местоположения",
    )
    latitude = sqlalchemy.Column(
        sqlalchemy.DECIMAL(11, 8),
        nullable=False,
    )
    longitude = sqlalchemy.Column(
        sqlalchemy.DECIMAL(11, 8),
        nullable=False,
    )
    address = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=True,
        comment="Адрес",
    )
    nest = orm.relationship("TechNest", back_populates="location")


class Devices(Base):
    __tablename__ = "devices"
    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "nest_id",
            "name",
            name="nest_id_device_name_unique_index",
            comment="Уникальный индекс Идентификатор узла + название устройства",
        ),
    )
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор устройства",
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        comment="Название устройства",
    )
    model = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        comment="Модель устройства",
    )
    nest_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("tech_nests.id"),
    )
    nest = orm.relationship("TechNest", back_populates="devices")


class TechNest(Base):
    __tablename__ = "tech_nests"
    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "holder_id",
            "name",
            name="holder_id_device_name_unique_index",
            comment="Уникальный индекс владелец + название узла",
        ),
    )
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор технического гнезда",
        index=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        comment="Название технического узла",
    )
    location_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("locations.id"),
    )
    holder_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("companies.id"),
    )
    location = orm.relationship("Locations", back_populates="nest")
    devices = orm.relationship("Devices", back_populates="nest")
    holder = orm.relationship("Company", back_populates="nests")
