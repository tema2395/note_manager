from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    """ Функция зависимости для получения экземпляра сессии базы данных

    Yields:
         Session: Сессия базы данных SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """ Создает новую заметку в базе данных.

    Args:
        note (schemas.NoteCreate): Данные новой заметки.
        db (Session, optional): Сессия базы данных SQLAlchemy. Defaults to Depends(get_db).

    Returns:
        schemas.Note: Созданная заметка.
    """
    return crud.create_note(db=db, note=note)


@app.get("/notes/", response_model=list[schemas.Note])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """ Возвращает список всех заметок.

    Args:
        skip (int, optional): Количество заметок для пропуска. Defaults to 0.
        limit (int, optional): Максимальное количество заметок для возврата. Defaults to 10.
        db (Session, optional): Сессия базы данных SQLAlchemy. Defaults to Depends(get_db).

    Returns:
         list[schemas.Note]: Список заметок.
    """
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes
    
@app.get("/notes/{note_id}", response_model=schemas.Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    """Возвращает заметку по её ID.

    Args:
        note_id (int): ID заметки.
        db (Session, optional): Сессия базы данных SQLAlchemy. Defaults to Depends(get_db).

    Raises:
        HTTPException: Записка не найдена

    Returns:
        schemas.Note: Заметка с указанным ID.
    """
    db_note = crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.delete("/notes/{note_id}", response_model=schemas.Note)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """ Удаляет заметку по её ID.

    Args:
        note_id (int): ID заметки.
        db (Session, optional): Сессия базы данных SQLAlchemy. Defaults to Depends(get_db).

    Raises:
        HTTPException: Заметка не найдена
        HTTPException: Не удалось удалить заметку

    Returns:
        schemas.Note: Удалённая заметка.
    """
    db_note = crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    success = crud.delete_note_by_id(db, note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Failed to delete note")
    return db_note


@app.get("/notes/search/", response_model=list[schemas.Note])
def search_notes(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Поиск заметок по ключевому слову или фразе в заголовке или содержании.


    Args:
        keyword (str, optional): Ключевое слово или фраза для поиска.
        db (Session, optional): Сессия базы данных SQLAlchemy. Defaults to Depends(get_db).

    Returns:
        list[schemas.Note]: Список заметок, содержащих указанное ключевое слово или фразу.
    """
    notes = crud.search_notes(db=db, keyword=keyword)
    return notes