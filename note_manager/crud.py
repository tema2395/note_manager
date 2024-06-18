from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def get_note_by_id(db: Session, note_id: int):
    """Получает заметку по её идентификатору.

    Args:
        db (Session): Сессия базы данных SQLAlchemy.
        note_id (int): ID заметки.

    Returns:
        models.Note: Заметка с указанным идентификатором, если найдена, иначе None.
    """
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(db: Session, skip: int = 0, limit: int = 10):
    """
    Возвращает список всех заметок с возможностью пагинации.

    Args:
        db (Session): Сессия базы данных SQLAlchemy.
        skip (int, optional): Количество заметок для пропуска. Defaults to 0.
        limit (int, optional): Максимальное количество заметок для возврата. Defaults to 10.

    Returns:
        list[models.Note]: Список заметок.
    """
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate):
    """
    Создает новую заметку в базе данных.

    Args:
        db (Session): Сессия базы данных SQLAlchemy.
        note (schemas.NoteCreate): Данные новой заметки.

    Returns:
        models.Note: Созданная заметка.
    """
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note_by_id(db: Session, note_id: int):
    """
    Удаляет заметку из базы данных по её ID.

    Args:
        db (Session): Сессия базы данных SQLAlchemy.
        note_id (int): ID заметки.

    Returns:
        bool: True, если заметка успешно удалена, иначе False.
    """
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False


def search_notes(db: Session, keyword: str):
    """
    Ищет заметки по ключевому слову или фразе в заголовке или содержании.

    Args:
        db (Session): Сессия базы данных SQLAlchemy.
        keyword (str): Ключевое слово или фраза для поиска.

    Returns:
        list[models.Note]: Список заметок, содержащих указанное ключевое слово или фразу.
    """
    return (
        db.query(models.Note)
        .filter(
            or_(
                models.Note.title.contains(keyword),
                models.Note.content.contains(keyword),
            )
        )
        .all()
    )
