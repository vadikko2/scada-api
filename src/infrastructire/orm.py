from __future__ import annotations

from infrastructire import logging
import sqlalchemy
from sqlalchemy import orm

from domain import models

mapper_registry = orm.registry()

company = sqlalchemy.Table(
    "companies",
    mapper_registry.metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор компании",
    ),
    sqlalchemy.Column(
        "name",
        sqlalchemy.String(255),
        nullable=False,
        comment="Название компании",
    ),
    sqlalchemy.Column(
        "inn",
        sqlalchemy.Integer,
        nullable=False,
        comment="ИНН компании",
    ),
    sqlalchemy.Column(
        "kpp",
        sqlalchemy.Integer,
        nullable=False,
        comment="КПП компании",
    ),
)

location = sqlalchemy.Table(
    "locations",
    mapper_registry.metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор местоположения",
    ),
    sqlalchemy.Column(
        "latitude",
        sqlalchemy.DECIMAL(11, 8),
        nullable=False,
    ),
    sqlalchemy.Column(
        "longitude",
        sqlalchemy.DECIMAL(11, 8),
        nullable=False,
    ),
    sqlalchemy.Column(
        "address",
        sqlalchemy.String(255),
        nullable=True,
        comment="Адрес",
    ),
)

tech_nest = sqlalchemy.Table(
    "tech_nests",
    mapper_registry.metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор технического гнезда",
        index=True,
    ),
    sqlalchemy.Column(
        "location_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("locations.id"),
    ),
    sqlalchemy.Column(
        "holder_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("companies.id"),
    ),
)

device = sqlalchemy.Table(
    "devices",
    mapper_registry.metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор устройства",
    ),
    sqlalchemy.Column(
        "name",
        sqlalchemy.String(255),
        nullable=False,
        comment="Название устройства",
    ),
    sqlalchemy.Column(
        "model",
        sqlalchemy.String(255),
        nullable=False,
        comment="Модель устройства",
    ),
)


async def start_mappers():
    logging.logger.info("Starting mappers")
    device_mapper = mapper_registry.map_imperatively(models.Device, device)
    location_mapper = mapper_registry.map_imperatively(models.TechNestLocation, location)
    tech_nest_mapper = mapper_registry.map_imperatively(
        models.TechNest,
        tech_nest,
        properties={
            "devices": orm.relationship(
                device_mapper,
                secondary=device,
                collection_class=list,
            ),
            "location": orm.relationship(
                location_mapper,
                secondary=location,
            ),
        },
    )
    mapper_registry.map_imperatively(
        models.Company,
        company,
        properties={
            "tech_nests": orm.relationship(
                tech_nest_mapper,
                secondary=tech_nest,
                collection_class=list,
            )
        },
    )
