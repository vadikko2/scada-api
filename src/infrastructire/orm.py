from __future__ import annotations

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import registry

from infrastructire import logging

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Company(Base):
    __tablename__ = "companies"
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
        sqlalchemy.Integer,
        nullable=False,
        comment="ИНН компании",
    )
    kpp = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        comment="КПП компании",
    )
    nests = orm.relationship("TechNest", back_populates="holder")


class Locations(Base):
    __tablename__ = "locations"
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
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор технического гнезда",
        index=True,
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


async def start_mappers():
    logging.logger.info("Starting mappers")
    # device_mapper = mapper_registry.map_imperatively(models.Device, device)
    # location_mapper = mapper_registry.map_imperatively(models.TechNestLocation, location)
    # tech_nest_mapper = mapper_registry.map_imperatively(
    #     models.TechNest,
    #     tech_nest,
    #     properties={
    #         "devices": orm.relationship(
    #             device_mapper,
    #             secondary=device,
    #             collection_class=list,
    #         ),
    #         "location": orm.relationship(
    #             location_mapper,
    #             secondary=location,
    #         ),
    #     },
    # )
    # mapper_registry.map_imperatively(
    #     models.Company,
    #     company,
    #     properties={
    #         "tech_nests": orm.relationship(
    #             tech_nest_mapper,
    #             secondary=tech_nest,
    #             collection_class=list,
    #         )
    #     },
    # )
