from typing import List, Tuple

from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import LineString, Polygon

from .. import schemas
from ..models import Segment, Subsegment
from .users import get_user_by_email


def serialize_segment(segment: Segment) -> schemas.Segment:
    subsegments = []
    if segment.subsegments:
        subsegments = list(
            map(lambda sub: schemas.Subsegment(**sub.__dict__), segment.subsegments)
        )
    shape = to_shape(segment.geometry)
    return schemas.Segment(
        id=segment.id,
        properties={"subsegments": subsegments},
        geometry={"coordinates": shape.coords[:]},
        bbox=shape.bounds
    )


def get_segments(
    db: Session,
    bbox: List[Tuple[float, float]] = None,
    exclude: List[int] = None,
) -> schemas.SegmentCollection:
    if exclude:
        segments = db.query(Segment).filter(Segment.id.notin_(exclude)).all()
    elif bbox:
        polygon = from_shape(Polygon(bbox), srid=4326)
        segments = db.query(Segment).filter(polygon.ST_Intersects(Segment.geometry)).all()
    elif bbox and exclude:
        polygon = from_shape(Polygon(bbox), srid=4326)
        segments = db.query(Segment)\
            .filter(polygon.ST_Intersects(Segment.geometry))\
            .filter(Segment.id.notin_(exclude)).all()
    else:
        segments = db.query(Segment).all()
    collection = list(map(lambda feat: serialize_segment(feat), segments))
    return schemas.SegmentCollection(features=collection)


def create_segment(
    db: Session, segment: schemas.SegmentCreate, email: str
) -> schemas.Segment:
    geometry = from_shape(
        LineString(coordinates=segment.geometry.coordinates), srid=4326
    )

    user = get_user_by_email(db, email)
    db_feature = Segment(geometry=geometry, owner=user, owner_id=user.id)

    for prop in segment.properties.subsegments:
        db_prop = Subsegment(
            segment_id=db_feature.id, segment=db_feature, **prop.__dict__
        )
        db.add(db_prop)

    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return serialize_segment(db_feature)


def update_segment(
    db: Session, segment_id: int, segment: schemas.SegmentCreate, email: str
) -> schemas.Segment:
    geometry = from_shape(
        LineString(coordinates=segment.geometry.coordinates), srid=4326
    )

    user = get_user_by_email(db, email)
    db_feature = db.query(Segment).get(segment_id)

    db_feature.geometry = geometry
    db_feature.owner_id = user.id

    db.commit()
    return serialize_segment(db_feature)


def delete_segment(db: Session, segment_id: int):
    segment = db.query(Segment).filter(Segment.id == segment_id).first()
    db.delete(segment)
    db.commit()
    return segment


def get_segment(db: Session, segment_id: int):
    segment = db.query(Segment).get(segment_id)
    return serialize_segment(segment)
