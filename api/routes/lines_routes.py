from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas.line_route import LineString
from database.base import get_db
from database.models.line_route import LineRoute

router = APIRouter()


@router.post('/compare-linestrings')
async def compare_linestrings(linestring: LineString, db: Session = Depends(get_db)):
    line_route: LineRoute = LineRoute(db)
    return line_route.compare_linestrings(linestring.string)


@router.get('/{name}')
async def get_by_name(name: str, db: Session = Depends(get_db)):
    line_route: LineRoute = LineRoute(db)
    return line_route.get_by_name(name)
