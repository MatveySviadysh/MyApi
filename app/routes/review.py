from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.models import Review as ReviewModel
from utils.helpers import get_db
from models.review_model import ReviewCreate, ReviewResponse
from models.travel_model import TravelResponse
from sqlalchemy.orm import Session, joinedload

review_router = APIRouter()

@review_router.post('/review/create', tags=["Reviews"], summary="Создать новый отзыв", response_model=ReviewResponse)
async def create_review(
    review: ReviewCreate, db: Session = Depends(get_db)
) -> ReviewResponse:
    """
    Создает новый отзыв.
    
    - **user_id**: ID пользователя, оставившего отзыв.
    - **travel_id**: ID путешествия, на которое оставлен отзыв.
    - **rating**: Оценка.
    - **comment**: Комментарий.
    
    Возвращает созданный объект отзыва.
    """
    new_review = ReviewModel(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return ReviewResponse(
        id=new_review.id,  # type: ignore
        rating=new_review.rating,  # type: ignore
        comment=new_review.comment,  # type: ignore
        created_at=new_review.created_at,  # type: ignore
        user_id=review.user_id,  # Исправлено на использование user_id из объекта review
        travel=TravelResponse(id=review.travel_id)  # type: ignore
    )


@review_router.get('/reviews', tags=["Reviews"], summary="Получает список всех отзывов", response_model=List[ReviewResponse])
async def get_reviews(db: Session = Depends(get_db)) -> List[ReviewModel]:
    """
    Получает список всех отзывов.
    Возвращает список объектов отзывов.
    """
    reviews = db.query(ReviewModel).all()
    return reviews


@review_router.get('/review/{review_id}', tags=["Reviews"], summary="Получает отзыв по его ID", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)) -> ReviewResponse:
    """
    Получает отзыв по его ID.

    - **review_id**: ID отзыва.

    Если отзыв не найден, возвращает ошибку 404.
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@review_router.delete('/review/{review_id}', tags=["Reviews"], summary="Удалить отзыв", response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Удаляет отзыв по его ID.

    - **review_id**: ID удаляемого отзыва.
    
    Возвращает сообщение об успешном удалении.
    """
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}


@review_router.put('/review/{review_id}', tags=["Reviews"], summary="Изменить отзыв", response_model=ReviewResponse)
async def update_review(review_id: int, review: ReviewCreate, db: Session = Depends(get_db)) -> ReviewResponse:
    """
    Обновляет отзыв по его ID.

    - **review_id**: ID отзыва, который нужно обновить.
    - **review**: Объект ReviewCreate с новой информацией для обновления отзыва.
        - **rating**: Новая оценка отзыва.
        - **comment**: Новый текст отзыва.
    
    Возвращает обновленный объект отзыва.
    Если отзыв с указанным ID не найден, возвращает ошибку 404.
    """
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db_review.rating = review.rating
    db_review.comment = review.comment
    db.commit()
    db.refresh(db_review)
    return db_review
