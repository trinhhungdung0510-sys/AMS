from app.api.deps import get_current_user
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.animal_intrusion import ANIMAL_OBJECT_TYPES, DEFAULT_ANIMAL_INTRUSION_POLICIES
from app.database.session import get_db
from app.models import AnimalIntrusionPolicy
from app.schemas.animal_intrusion import (
    AnimalIntrusionPolicyCreate,
    AnimalIntrusionPolicyResponse,
    AnimalIntrusionPolicyUpdate,
)

router = APIRouter(prefix="/animal-intrusion", tags=["animal-intrusion"],
    dependencies=[Depends(get_current_user)]
)


def _get_policy_or_404(policy_id: str, db: Session) -> AnimalIntrusionPolicy:
    policy = db.get(AnimalIntrusionPolicy, policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal intrusion policy not found")
    return policy


@router.get("/policies", response_model=list[AnimalIntrusionPolicyResponse])
def list_policies(db: Session = Depends(get_db)) -> list[AnimalIntrusionPolicy]:
    return list(db.scalars(select(AnimalIntrusionPolicy).order_by(AnimalIntrusionPolicy.object_type)))


@router.get("/policies/{policy_id}", response_model=AnimalIntrusionPolicyResponse)
def get_policy(policy_id: str, db: Session = Depends(get_db)) -> AnimalIntrusionPolicy:
    return _get_policy_or_404(policy_id, db)


@router.post("/policies", response_model=AnimalIntrusionPolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(payload: AnimalIntrusionPolicyCreate, db: Session = Depends(get_db)) -> AnimalIntrusionPolicy:
    object_type = payload.object_type.lower()
    if object_type not in ANIMAL_OBJECT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"object_type must be one of: {', '.join(sorted(ANIMAL_OBJECT_TYPES))}",
        )

    policy_id = payload.id or f"AIP-{object_type.upper()}"
    if db.get(AnimalIntrusionPolicy, policy_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Policy id already exists")

    existing = db.scalar(select(AnimalIntrusionPolicy).where(AnimalIntrusionPolicy.object_type == object_type))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Policy for object_type already exists")

    policy = AnimalIntrusionPolicy(
        id=policy_id,
        object_type=object_type,
        allowed_zones=payload.allowed_zones,
        restricted_zones=payload.restricted_zones,
        severity=payload.severity.lower(),
        enabled=payload.enabled,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@router.put("/policies/{policy_id}", response_model=AnimalIntrusionPolicyResponse)
def update_policy(
    policy_id: str,
    payload: AnimalIntrusionPolicyUpdate,
    db: Session = Depends(get_db),
) -> AnimalIntrusionPolicy:
    policy = _get_policy_or_404(policy_id, db)
    values = payload.model_dump(exclude_unset=True)
    if "severity" in values and values["severity"] is not None:
        values["severity"] = values["severity"].lower()
    for field, value in values.items():
        setattr(policy, field, value)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@router.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: str, db: Session = Depends(get_db)) -> None:
    policy = _get_policy_or_404(policy_id, db)
    db.delete(policy)
    db.commit()


@router.post("/policies/seed-defaults", response_model=list[AnimalIntrusionPolicyResponse])
def seed_default_policies(db: Session = Depends(get_db)) -> list[AnimalIntrusionPolicy]:
    seeded: list[AnimalIntrusionPolicy] = []
    for item in DEFAULT_ANIMAL_INTRUSION_POLICIES:
        policy = db.get(AnimalIntrusionPolicy, item["id"]) or AnimalIntrusionPolicy(
            id=item["id"],
            object_type=item["object_type"],
            allowed_zones=item["allowed_zones"],
            restricted_zones=item["restricted_zones"],
            severity=item["severity"],
            enabled=item["enabled"],
        )
        policy.allowed_zones = item["allowed_zones"]
        policy.restricted_zones = item["restricted_zones"]
        policy.severity = item["severity"]
        policy.enabled = item["enabled"]
        db.merge(policy)
        seeded.append(policy)
    db.commit()
    for policy in seeded:
        db.refresh(policy)
    return seeded
