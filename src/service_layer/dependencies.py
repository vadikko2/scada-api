import di
from di import dependent

from infrastructire import factories, storages, uow

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


RedisClientFactoryBind = di.bind_by_type(
    dependent.Dependent(factories.RedisClientFactory, scope="request"),
    factories.RedisClientFactory,
)

TechNestIndicatorValuesStorageBind = di.bind_by_type(
    dependent.Dependent(storages.RedisTechNestIndicatorValuesStorage, scope="request"),
    storages.TechNestIndicatorValuesStorage,
)

DeviceIndicatorValuesStorageBind = di.bind_by_type(
    dependent.Dependent(storages.RedisDeviceIndicatorValuesStorage, scope="request"),
    storages.DeviceIndicatorValuesStorage,
)


container.bind(RedisClientFactoryBind)
container.bind(SessionFactoryBind)
container.bind(RepositoryFactoryBind)
container.bind(UoWBind)
container.bind(TechNestIndicatorValuesStorageBind)
container.bind(DeviceIndicatorValuesStorageBind)
