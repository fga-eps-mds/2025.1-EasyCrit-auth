from app.schemas import CharacterCreate, CharacterList, CharacterUpdate, CharacterPublic
from app.database.database import get_session
from app.models import Character, User
from app.middleware.auth import check_auth_token

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix='/characters', tags=['characters'])


# Create a new character (Action for a logged-in user)
@router.post('/', response_model=CharacterPublic, status_code=status.HTTP_201_CREATED)
def create_character(
  character: CharacterCreate, db: Session = Depends(get_session), current_user: User = Depends(check_auth_token)
):
  stmt = select(Character).where(Character.name == character.name, Character.user_id == current_user.id)
  db_character = db.scalar(stmt)

  if db_character:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You already have a character with this name.')

  db_character = Character(
    name=character.name, biography=character.biography, circle_color=character.circle_color, user_id=character.user_id
  )

  db.add(db_character)
  db.commit()
  db.refresh(db_character)
  return db_character


# List all characters
@router.get('/', response_model=CharacterList, dependencies=[Depends(check_auth_token)])
def get_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
  stmt = select(Character).offset(skip).limit(limit).order_by(Character.id)
  characters = db.scalars(stmt).all()
  return {'characters': characters}


# Get a specific character by ID
@router.get(
  '/{character_id}',
  response_model=CharacterPublic,
  dependencies=[Depends(check_auth_token)],
  status_code=status.HTTP_200_OK,
)
def get_character_by_id(character_id: int, db: Session = Depends(get_session)):
  stmt = select(Character).where(Character.id == character_id)
  character = db.scalar(stmt)

  if not character:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character not found')

  return character


# Update a character
@router.patch('/{character_id}', response_model=CharacterPublic, status_code=status.HTTP_200_OK)
def partial_update_character(
  character_id: int,
  character: CharacterUpdate,
  db: Session = Depends(get_session),
  current_user: User = Depends(check_auth_token),
):
  stmt = select(Character).where(Character.id == character_id)
  db_character = db.scalar(stmt)

  if not db_character:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character not found')

  if db_character.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')

  for key, value in character.model_dump(exclude_unset=True).items():
    setattr(db_character, key, value)

  db.commit()
  db.refresh(db_character)
  return db_character


# Delete a character
@router.delete('/{character_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
  character_id: int, db: Session = Depends(get_session), current_user: User = Depends(check_auth_token)
):
  stmt = select(Character).where(Character.id == character_id)
  db_character = db.scalar(stmt)

  if not db_character:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character not found')

  if db_character.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')

  db.delete(db_character)
  db.commit()

  return {'message': 'character deleted successfully'}
