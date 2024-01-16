from sqlalchemy.orm import Session
from utils.context_auth_crypt import get_password_hash
from infra.database.models.security import Rol, User, UsersRoles

def execute_seed(session: Session) -> str:
    create_rolea_and_user(session)
    
    return "Seeds executed successfully"


def create_rolea_and_user (session: Session):
    try:
        roles : list[Rol] = session.query(Rol).filter(Rol.code.in_(['SUPER_ADMIN','ADMIN','GUESS'])).all()
        if roles is None:
            roles = [
                    Rol(code="SUPER_ADMIN",name = "super administrador" ), 
                    Rol(code="ADMIN",name = "administrador" ), 
                    Rol(code="GUESS",name = "invitado" )
                ]
            session.add_all(roles)
            session.commit()  
        
        role_superadmin = session.query(Rol).filter( Rol.code == "SUPER_ADMIN").first()
        superadmin = session.query(User).filter( User.username == "sadmin").first()
        
        if role_superadmin is not None and superadmin is not None:
            return
        
        user = User( 
            username = "sadmin",
            email =  "sadmin",
            password = get_password_hash("Managua01*"),
            firstname =  "sadmin",
            lastname =  "sadmin",
            is_active =  True,
        )   

        session.add(user)
        session.commit()
        session.refresh(user)

        user_roles = UsersRoles(
                id_user=user.id,
                id_rol=role_superadmin.id
        )
        
        session.add(user_roles)
        session.commit()
    
    except Exception as ex:
        print(ex)




