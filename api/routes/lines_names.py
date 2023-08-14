from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from database.base import get_db
from database.models.line_name import LineName

router = APIRouter()


@router.get('')
async def get_all(db: Session = Depends(get_db)):
    line_name: LineName = LineName(db)
    return line_name.get_all()


@router.get('/seed')
async def seed(db: Session = Depends(get_db)):
    line_name: LineName = LineName(db)
    return line_name.seed()
