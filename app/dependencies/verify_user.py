from typing import Optional
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT

from app.dependencies.data_conexion import get_db
from app.models.users import Users



class UserNotFound(Exception):
    pass


def require_user(
    db: Session = Depends(get_db), 
    Authorize: AuthJWT = Depends()
)-> Optional[HTTPException]:
    """_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
        Authorize (AuthJWT, optional): _description_. Defaults to Depends().

    Raises:
        UserNotFound: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Optional[HTTPException]: _description_
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = db.query(Users).filter(Users.id == current_user)\
            .filter(Users.is_deleted == False)\
            .first()

        if not user:
            raise UserNotFound('User no longer exist')
    except Exception as e:
        error = e.__class__.__name__
        #print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST, detail={
                    'status':False,
                    'msg': "You are not logged in"
                })
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_421_MISDIRECTED_REQUEST, detail={
                'status':False,
                'msg': 'User no longer exist'
                })
        raise HTTPException(
            status_code=status.HTTP_421_MISDIRECTED_REQUEST, detail={
                'status':False,
                'msg':'Token is invalid or has expired'
            })
        
    return user
