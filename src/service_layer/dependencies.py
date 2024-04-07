import di
from di import dependent

from infrastructire import factories, uow

container = di.Container()

SessionFactoryBind = di.bind_by_type(
    dependent.Dependent(factories.SQLAlchemySessionFactory, scope="request"),
    factories.SessionFactory[uow.S],
)

RepositoryFactoryBind = di.bind_by_type(
    dependent.Dependent(factories.SQLAlchemyRepositoryFactory, scope="request"),
    factories.RepositoryFactory[uow.S],
)


UoWBind = di.bind_by_type(
    dependent.Dependent(uow.SQLAlchemyUoW, scope="request"),
    uow.UoW,
)

container.bind(SessionFactoryBind)
container.bind(RepositoryFactoryBind)
container.bind(UoWBind)
