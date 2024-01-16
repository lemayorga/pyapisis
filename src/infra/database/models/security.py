from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm  import relationship
from infra.database.setting_db import Base

class Rol (Base):
    __tablename__ = 'rol'
    __table_args__ = {"schema":"security"}

    id = Column(Integer, primary_key=True, autoincrement=True,index = True)
    code = Column('cod_rol', String(100), nullable=False)
    name = Column('rol_name', String(100), nullable=False)


# class Permission (Base):
#     __tablename__ = 'permission'
#     __table_args__ = {"schema":"security"}

#     id = Column(Integer, primary_key=True, autoincrement=True, index = True)
#     name = Column(String(550), nullable=False)
#     orden = Column(Integer, nullable=True)
#     icon = Column(String(80), nullable=True)
#     icon = Column(String(500), nullable=True)
#     id_higher_permission = Column('id_higher_permission', Integer, nullable=True)
#     is_Active = Column('is_active', Boolean, nullable=False, default=True)
#     users = relationship('User', secondary='security.usersroles')


class User (Base):
    __tablename__ = 'user'
    __table_args__ = {"schema":"security"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique= True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=True)
    is_active = Column('is_active', Boolean, nullable=False, default=True)
    rols = relationship('Rol', secondary='security.usersroles')
    

class UsersRoles (Base):
    __tablename__ = 'usersroles'
    __table_args__ = {"schema":"security"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column('id_user', Integer, ForeignKey('security.rol.id'), nullable=False) 
    id_rol = Column('id_rol', Integer,ForeignKey('security.user.id'), nullable=False) 



