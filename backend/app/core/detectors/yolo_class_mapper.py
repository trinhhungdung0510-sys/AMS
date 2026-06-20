from __future__ import annotations

"""Map Ultralytics COCO class names to AMS observation classes."""

# COCO ids for supported YOLO classes
COCO_PERSON = 0
COCO_BIRD = 14
COCO_DOG = 16
COCO_CAT = 17

SUPPORTED_COCO_CLASS_IDS: tuple[int, ...] = (COCO_PERSON, COCO_BIRD, COCO_DOG, COCO_CAT)

YOLO_TO_AMS_CLASS: dict[str, str] = {
    "person": "person",
    "dog": "animal",
    "cat": "animal",
    "bird": "animal",
}


def map_yolo_class(class_name: str) -> str | None:
    """Return AMS class (person/animal) or None if unsupported."""
    if not class_name:
        return None
    return YOLO_TO_AMS_CLASS.get(class_name.strip().lower())


def map_coco_class_id(class_id: int, names: dict[int, str] | list[str]) -> str | None:
    if isinstance(names, list):
        label = names[class_id] if 0 <= class_id < len(names) else ""
    else:
        label = names.get(class_id, "")
    return map_yolo_class(str(label))
