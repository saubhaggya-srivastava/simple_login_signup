from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, func
from sqlalchemy.orm import Session

from db.database import get_db
from models.channel import Channel
from schemas.channel import ChannelCreate, ChannelListResponse, ChannelResponse

router = APIRouter(prefix="/channels", tags=["Channel"])


def serialize_channel(channel: Channel) -> dict[str, int | str]:
    return {
        "id": channel.id,
        "name": channel.name,
    }


@router.get(
    "",
    response_model=ChannelListResponse,
    status_code=status.HTTP_200_OK,
    summary="List channels",
    description="Returns all channel master records ordered by `id`.",
    responses={200: {"description": "Channel list returned successfully."}},
)
def list_channels(db: Session = Depends(get_db)) -> ChannelListResponse:
    items = db.query(Channel).order_by(asc(Channel.id)).all()
    return ChannelListResponse(items=[serialize_channel(item) for item in items])


@router.post(
    "",
    response_model=ChannelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create channel",
    description="Creates a new channel master record. This endpoint is open for now.",
    responses={
        201: {"description": "Channel created successfully."},
        400: {"description": "Channel name is blank."},
        409: {"description": "Channel name already exists."},
    },
)
def create_channel(payload: ChannelCreate, db: Session = Depends(get_db)) -> ChannelResponse:
    cleaned_name = payload.name.strip()
    if not cleaned_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Channel name cannot be blank.",
        )

    existing_channel = (
        db.query(Channel)
        .filter(func.lower(Channel.name) == cleaned_name.lower())
        .first()
    )
    if existing_channel is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Channel name already exists.",
        )

    channel = Channel(name=cleaned_name)
    db.add(channel)
    db.commit()
    db.refresh(channel)

    return ChannelResponse(**serialize_channel(channel))
