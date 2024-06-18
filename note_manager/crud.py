from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note_by_id(db: Session, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False

def search_notes(db: Session, keyword: str):
    return db.query(models.Note).filter(
        or_(
            models.Note.title.contains(keyword),
            models.Note.content.contains(keyword)
        )
    ).all()

