import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.models import Comment, Incident, Task, User
from app.schemas.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/api/comments", tags=["comments"])
logger = logging.getLogger("opstrack")


def _assert_entity_exists(entity_type: str, entity_id: str, db: Session) -> None:
    model = Task if entity_type == "task" else Incident
    exists = db.query(model).filter(model.id == entity_id).first()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_type.capitalize()} not found",
        )


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _assert_entity_exists(payload.entity_type, payload.entity_id, db)

    comment = Comment(
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        body=payload.body,
        author_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    logger.info(
        "comment_created comment_id=%s entity_type=%s entity_id=%s author=%s",
        comment.id,
        comment.entity_type,
        comment.entity_id,
        current_user.id,
    )
    return comment


@router.get("", response_model=list[CommentOut])
def list_comments(
    entity_type: str,
    entity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if entity_type not in {"task", "incident"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="entity_type must be 'task' or 'incident'"
        )
    return (
        db.query(Comment)
        .filter(Comment.entity_type == entity_type, Comment.entity_id == entity_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own comments"
        )
    db.delete(comment)
    db.commit()
    return None
