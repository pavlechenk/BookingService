from abc import ABC, abstractmethod
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.database import async_session_maker


class AbstractBaseDAO(ABC):
    model = None
    
    @classmethod
    @abstractmethod
    async def find_all(cls, **filter_by: dict):
        raise NotImplementedError
    
    
    @classmethod
    @abstractmethod
    async def find_one_or_none(cls, **filter_by: dict):
        raise NotImplementedError
    
    
    @classmethod
    @abstractmethod
    async def add(cls, **data: dict):
        raise NotImplementedError
    
    
    @classmethod
    @abstractmethod
    async def update(cls, **data: dict):
        raise NotImplementedError
    
    
    @classmethod
    @abstractmethod
    async def delete(cls, **filter_by: dict):
        raise NotImplementedError
    
    
    
class SQLAlchemyDAO(AbstractBaseDAO):
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        

    @classmethod
    async def add(cls, **data: dict):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = "Database Exc: " if isinstance(e, SQLAlchemyError) else "Unknown Exc: "
            msg += "Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
        
        
    @classmethod
    async def update(cls, user_id: int, **data: dict):
        try:
            query = update(cls.model).where(cls.model.id == user_id).values(**data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = "Database Exc: " if isinstance(e, SQLAlchemyError) else "Unknown Exc: "
            msg += "Cannot update data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
    

    @classmethod
    async def delete(cls, **filter_by: dict):
        try:
            query = delete(cls.model).filter_by(**filter_by).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = "Database Exc: " if isinstance(e, SQLAlchemyError) else "Unknown Exc: "
            msg += "Cannot delete data from a table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
            

    @classmethod
    async def add_bulk(cls, *data):
        query = insert(cls.model).values(*data).returning(cls.model.id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
