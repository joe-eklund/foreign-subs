from fastapi import APIRouter

from app.models.movie import Movie
router = APIRouter()

@router.post("/", response_model=Item)
def create_movie(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Create new item.
    """
    item = crud.item.create(db_session=db, item_in=item_in, owner_id=current_user.id)
    return item