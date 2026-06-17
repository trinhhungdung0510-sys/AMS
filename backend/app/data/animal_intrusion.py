"""Default animal intrusion zone policies for AMS v3.3."""

ANIMAL_OBJECT_TYPES = {"dog", "cat", "rat", "bird"}

ZONE_ALIASES = {
    "nursery_barn": "weaning_barn",
    "feed_warehouse": "feed_storage",
    "medicine_warehouse": "vet_medicine_storage",
}

DEFAULT_ANIMAL_INTRUSION_POLICIES = [
    {
        "id": "AIP-DOG",
        "object_type": "dog",
        "allowed_zones": ["parking_zone", "reception_zone", "pig_loading_zone"],
        "restricted_zones": ["gestation_barn", "farrowing_barn", "weaning_barn", "nursery_barn"],
        "severity": "critical",
        "enabled": True,
    },
    {
        "id": "AIP-CAT",
        "object_type": "cat",
        "allowed_zones": ["parking_zone", "reception_zone", "guard_house"],
        "restricted_zones": ["gestation_barn", "farrowing_barn", "weaning_barn", "boar_barn", "nursery_barn"],
        "severity": "high",
        "enabled": True,
    },
    {
        "id": "AIP-RAT",
        "object_type": "rat",
        "allowed_zones": ["parking_zone", "reception_zone"],
        "restricted_zones": ["vet_medicine_storage", "feed_storage", "medicine_warehouse", "feed_warehouse"],
        "severity": "critical",
        "enabled": True,
    },
    {
        "id": "AIP-BIRD",
        "object_type": "bird",
        "allowed_zones": ["parking_zone", "reception_zone", "guard_house"],
        "restricted_zones": ["feed_storage", "feed_warehouse"],
        "severity": "warning",
        "enabled": True,
    },
]
