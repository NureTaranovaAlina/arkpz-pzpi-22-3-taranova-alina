from fastapi import FastAPI, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, database, service_crud
from app.auth import authenticate_user, create_access_token, get_current_user
import os

os.makedirs("uploads/flashcards", exist_ok=True)

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = service_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return service_crud.create_user(db=db, user=user)

@app.post("/token/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/topic/", response_model=schemas.TopicResponse)
def create_topic(topic: schemas.TopicCreate,
    db = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.create_topic(db=db, topic=topic, user_id=current_user.id)

@app.get("/topic/", response_model=list[schemas.TopicResponse])
def get_user_topics(db = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.get_topics_by_user_id(db, current_user.id)

@app.post("/flashcards/", response_model=schemas.FlashcardResponse)
def create_flashcard(
    flashcard: schemas.FlashcardCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.create_flashcard(db=db, flashcard=flashcard)

@app.get("/flashcards/topic/{topic_id}", response_model=list[schemas.FlashcardResponse])
def read_flashcards(
    topic_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.get_flashcards_by_topic_id(db=db, topic_id=topic_id)

@app.post("/flashcards/{flashcard_id}/upload-image/")
async def upload_flashcard_image(
    flashcard_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db)
):

    if file.content_type not in ["image/png", "image/jpeg"]:
        return {"error": "Неверный тип файла. Разрешены только .png и .jpeg"}
    
    if (file.size or 0) > 5 * 1024 * 1024:  # Ограничение в 5 МБ
        return {"error": "Файл слишком большой"}

    file_location = f"uploads/flashcards/{flashcard_id}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    service_crud.update_flashcard_image(db, flashcard_id=flashcard_id, image_path=file_location)

    return {"info": "Файл успешно загружен", "path": file_location}

@app.get("/flashcards/{flashcard_id}/image")
def get_flashcard_image(flashcard_id: int, db: Session = Depends(database.get_db)):
    flashcard = service_crud.get_flashcard_by_id(db, flashcard_id)
    if not flashcard or not flashcard.image_path: # type: ignore
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(flashcard.image_path) # type: ignore

@app.post("/crosswords/", response_model=schemas.CrosswordResponse)
def create_crossword(
    crossword: schemas.CrosswordCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.create_crossword(db=db, crossword=crossword)

@app.get("/crosswords/topic/{topic_id}", response_model=list[schemas.CrosswordResponse])
def read_crosswords(
    topic_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return service_crud.get_crosswords_by_topic_id(db=db, topic_id=topic_id)

@app.post("/grade/topic/", response_model=schemas.UserTopicGradeResponse)
def grade_user_topic(
    payload: schemas.UserTopicGradeCreate,
    db = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    return service_crud.put_user_topic_grade(db, payload, current_user.id)

@app.get("/grade/user/", response_model=list[schemas.UserTopicGradeResponse])
def get_all_user_grades(
    db = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    return service_crud.get_all_user_grades(db, current_user.id)

@app.get("/schedule/")
def repetition_schedule(
    db: Session = Depends(database.get_db),
    current_user = Depends(get_current_user)
):
    try:
        schedule = service_crud.get_repetition_schedule(db, current_user.id)
        return {"user_id": current_user.id, "schedule": schedule}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
import subprocess
from datetime import datetime
from fastapi import APIRouter, HTTPException

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

BACKUP_DIR = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

@admin_router.post("/backup/")
def create_backup(
    current_user: models.User = Depends(get_current_user)
):

    if(not current_user.is_admin): # type: ignore
        return {"message": "not authorized"}
    
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.sql")

    db_name = os.getenv("POSTGRES_DB", "mydatabase")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "password")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")

    os.environ["PGPASSWORD"] = db_password

    dump_command = [
        "pg_dump",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-F", "c",  
        "-f", backup_file,  
        db_name
    ]

    try:
        subprocess.run(dump_command, check=True)
        return {"message": "Backup created successfully", "backup_path": backup_file}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error during backup: {str(e)}")

@admin_router.post("/restore/")
def restore_backup(
    backup_name: str,
    current_user: models.User = Depends(get_current_user)
):

    if(not current_user.is_admin): # type: ignore
        return {"message": "not authorized"}    
    
    backup_file = os.path.join(BACKUP_DIR, backup_name)

    if not os.path.exists(backup_file):
        raise HTTPException(status_code=404, detail="Backup file not found")

    db_name = os.getenv("POSTGRES_DB", "mydatabase")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "password")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")

    print(f"Database parameters: host={db_host}, port={db_port}, user={db_user}, db={db_name}")
    print(f"Backup file: {backup_file}")

    env = os.environ.copy()
    env["PGPASSWORD"] = db_password
    print(f"Environment variables: {env}")

    restore_command = [
        "pg_restore",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-d", db_name,
        "-c",  
        backup_file
    ]
    print(f"Restore command: {' '.join(restore_command)}")

    try:
        result = subprocess.run(
            restore_command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"Restore completed. stdout: {result.stdout}, stderr: {result.stderr}")
        return {"message": "Database restored successfully", "details": result.stdout}
    except subprocess.CalledProcessError as e:
        print(f"Error during restore. stdout: {e.stdout}, stderr: {e.stderr}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Restore failed",
                "stdout": e.stdout,
                "stderr": e.stderr
            }
        )

app.include_router(admin_router)