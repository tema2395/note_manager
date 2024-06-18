from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@app.get("/notes/", response_model=list[schemas.Note])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes
    
@app.get("/notes/{note_id}", response_model=schemas.Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.delete("/notes/{note_id}", response_model=schemas.Note)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    success = crud.delete_note_by_id(db, note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Failed to delete note")
    return db_note


@app.get("/notes/search/", response_model=list[schemas.Note])
def search_notes(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    notes = crud.search_notes(db=db, keyword=keyword)
    return notes