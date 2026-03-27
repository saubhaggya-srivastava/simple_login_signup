from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from db.database import get_db
from models.sku import SKU
from schemas.sku import SKUFilterOptionsResponse, SKUListResponse

router = APIRouter(prefix="/skus", tags=["SKU"])

SORTABLE_FIELDS = {
    "id": SKU.id,
    "sku_code": SKU.sku_code,
    "sku_description": SKU.sku_description,
    "brand": SKU.brand,
    "category": SKU.category,
    "supplier": SKU.supplier,
    "sku_status": SKU.sku_status,
    "case_price": SKU.case_price,
    "unit_price": SKU.unit_price,
    "created_at": SKU.created_at,
}


def serialize_sku(sku: SKU) -> dict:
    return {
        "id": sku.id,
        "sku_parent_code": sku.sku_parent_code,
        "sku_code": sku.sku_code,
        "case_barcode": sku.case_barcode,
        "outer_barcode": sku.outer_barcode,
        "unit_barcode": sku.unit_barcode,
        "sku_description": sku.sku_description,
        "unit_images": sku.unit_images,
        "outer_images": sku.outer_images,
        "cases_images": sku.cases_images,
        "master_distributor": sku.master_distributor,
        "distributor": sku.distributor,
        "line_of_business": sku.line_of_business,
        "supplier": sku.supplier,
        "agency": sku.agency,
        "category": sku.category,
        "segment": sku.segment,
        "brand": sku.brand,
        "sub_brand": sku.sub_brand,
        "sku_type": sku.sku_type,
        "promotion": sku.promotion,
        "sku_status": sku.sku_status,
        "shelf_life_days": sku.shelf_life_days,
        "temperature": sku.temperature,
        "case_length_cm": sku.case_length_cm,
        "case_width_cm": sku.case_width_cm,
        "case_height_cm": sku.case_height_cm,
        "case_cbm": sku.case_cbm,
        "outer_length_cm": sku.outer_length_cm,
        "outer_width_cm": sku.outer_width_cm,
        "outer_height_cm": sku.outer_height_cm,
        "outer_cbm": sku.outer_cbm,
        "unit_length_cm": sku.unit_length_cm,
        "unit_width_cm": sku.unit_width_cm,
        "unit_height_cm": sku.unit_height_cm,
        "unit_cbm": sku.unit_cbm,
        "unit_weight_gm": sku.unit_weight_gm,
        "outer_per_case": sku.outer_per_case,
        "units_per_outer": sku.units_per_outer,
        "case_weight_kg": sku.case_weight_kg,
        "case_cost": sku.case_cost,
        "case_price": sku.case_price,
        "outer_price": sku.outer_price,
        "unit_price": sku.unit_price,
        "unit_rsp": sku.unit_rsp,
        "created_at": sku.created_at,
        "deactivated_at": sku.deactivated_at,
    }


def get_distinct_values(db: Session, column) -> list[str]:
    rows = (
        db.query(column)
        .filter(column.isnot(None))
        .distinct()
        .order_by(asc(column))
        .all()
    )

    values: list[str] = []
    for (value,) in rows:
        if not isinstance(value, str):
            continue

        cleaned = value.strip()
        if cleaned:
            values.append(cleaned)

    return values


def normalize_multi(values: list[str] | None) -> list[str] | None:
    """
    Supports both:
    - repeated params: ?brand=Rasna&brand=Creamwhip
    - comma-separated: ?brand=Rasna,Creamwhip
    """
    if not values:
        return None

    normalized: list[str] = []
    for v in values:
        if v is None:
            continue
        for part in str(v).split(","):
            cleaned = part.strip()
            if cleaned:
                normalized.append(cleaned)

    return normalized or None


def apply_sku_filters(
    query,
    *,
    sku_code: str | None,
    sku_description: str | None,
    master_distributor: list[str] | None,
    distributor: list[str] | None,
    line_of_business: list[str] | None,
    supplier: list[str] | None,
    agency: list[str] | None,
    category: list[str] | None,
    segment: list[str] | None,
    brand: list[str] | None,
    sub_brand: list[str] | None,
    sku_type: list[str] | None,
    promotion: list[str] | None,
    sku_status: list[str] | None,
    case_price_min: float | None,
    case_price_max: float | None,
    unit_price_min: float | None,
    unit_price_max: float | None,
    shelf_life_days_min: int | None,
    shelf_life_days_max: int | None,
    created_at_from: datetime | None,
    created_at_to: datetime | None,
    is_active: bool | None,
):
    if sku_code:
        query = query.filter(SKU.sku_code.ilike(f"%{sku_code.strip()}%"))
    if sku_description:
        query = query.filter(SKU.sku_description.ilike(f"%{sku_description.strip()}%"))

    exact_multi_filters = {
        "master_distributor": normalize_multi(master_distributor),
        "distributor": normalize_multi(distributor),
        "line_of_business": normalize_multi(line_of_business),
        "supplier": normalize_multi(supplier),
        "agency": normalize_multi(agency),
        "category": normalize_multi(category),
        "segment": normalize_multi(segment),
        "brand": normalize_multi(brand),
        "sub_brand": normalize_multi(sub_brand),
        "sku_type": normalize_multi(sku_type),
        "promotion": normalize_multi(promotion),
        "sku_status": normalize_multi(sku_status),
    }

    for field_name, values in exact_multi_filters.items():
        if values:
            query = query.filter(getattr(SKU, field_name).in_(values))

    if case_price_min is not None:
        query = query.filter(SKU.case_price >= case_price_min)
    if case_price_max is not None:
        query = query.filter(SKU.case_price <= case_price_max)
    if unit_price_min is not None:
        query = query.filter(SKU.unit_price >= unit_price_min)
    if unit_price_max is not None:
        query = query.filter(SKU.unit_price <= unit_price_max)
    if shelf_life_days_min is not None:
        query = query.filter(SKU.shelf_life_days >= shelf_life_days_min)
    if shelf_life_days_max is not None:
        query = query.filter(SKU.shelf_life_days <= shelf_life_days_max)
    if created_at_from is not None:
        query = query.filter(SKU.created_at >= created_at_from)
    if created_at_to is not None:
        query = query.filter(SKU.created_at <= created_at_to)

    if is_active is True:
        query = query.filter(SKU.deactivated_at.is_(None))
    elif is_active is False:
        query = query.filter(SKU.deactivated_at.is_not(None))

    return query


@router.get(
    "",
    response_model=SKUListResponse,
    status_code=status.HTTP_200_OK,
    summary="List and filter SKUs",
    description=(
        "Returns paginated SKU records from `sku_master`.\n\n"
        "Supported features:\n"
        "- partial text search on `sku_code` and `sku_description`\n"
        "- exact-match filters for business fields like `brand`, `category`, and `supplier`\n"
        "- multi-select filters using repeated params or comma-separated values\n"
        "- range filters for prices, shelf life, and created date\n"
        "- sorting and pagination"
    ),
    responses={
        200: {
            "description": "Filtered SKU list returned successfully.",
        },
        400: {
            "description": "Invalid sorting parameter supplied.",
        },
    },
)
def list_skus(
    sku_code: str | None = Query(
        default=None,
        description="Partial match search on SKU code.",
        examples=["SKU001"],
    ),
    sku_description: str | None = Query(
        default=None,
        description="Partial match search on SKU description.",
        examples=["milk"],
    ),
    master_distributor: list[str] | None = Query(
        default=None,
        description="Exact match filter for master distributor.",
        examples=["ABC Group", "ABC Group,XYZ Group"],
    ),
    distributor: list[str] | None = Query(
        default=None,
        description="Exact match filter for distributor.",
        examples=["ABC Distribution", "ABC Distribution,Other Distribution"],
    ),
    line_of_business: list[str] | None = Query(
        default=None,
        description="Exact match filter for line of business.",
        examples=["Beverages", "Beverages,Food"],
    ),
    supplier: list[str] | None = Query(
        default=None,
        description="Exact match filter for supplier.",
        examples=["Nestle", "Nestle,DELMOND BAHRAIN BISCUITS W.L.L."],
    ),
    agency: list[str] | None = Query(
        default=None,
        description="Exact match filter for agency.",
        examples=["Main Agency", "Main Agency,General Goods"],
    ),
    category: list[str] | None = Query(
        default=None,
        description="Exact match filter for category.",
        examples=["Dairy", "Dairy,Desserts"],
    ),
    segment: list[str] | None = Query(
        default=None,
        description="Exact match filter for segment.",
        examples=["Premium", "Premium,Standard"],
    ),
    brand: list[str] | None = Query(
        default=None,
        description="Exact match filter for brand.",
        examples=["Nescafe", "Rasna,Creamwhip"],
    ),
    sub_brand: list[str] | None = Query(
        default=None,
        description="Exact match filter for sub-brand.",
        examples=["Gold", "Gold,Cream Whip"],
    ),
    sku_type: list[str] | None = Query(
        default=None,
        description="Exact match filter for SKU type.",
        examples=["Unit", "FOOD"],
    ),
    promotion: list[str] | None = Query(
        default=None,
        description="Exact match filter for promotion.",
        examples=["Yes", "Yes,No"],
    ),
    sku_status: list[str] | None = Query(
        default=None,
        description="Exact match filter for SKU status.",
        examples=["Active", "Active,Inactive"],
    ),
    case_price_min: float | None = Query(
        default=None,
        description="Minimum case_price (inclusive).",
        examples=[50],
    ),
    case_price_max: float | None = Query(
        default=None,
        description="Maximum case_price (inclusive).",
        examples=[200],
    ),
    unit_price_min: float | None = Query(
        default=None,
        description="Minimum unit_price (inclusive).",
        examples=[1],
    ),
    unit_price_max: float | None = Query(
        default=None,
        description="Maximum unit_price (inclusive).",
        examples=[50],
    ),
    shelf_life_days_min: int | None = Query(
        default=None,
        description="Minimum shelf_life_days (inclusive).",
        examples=[30],
    ),
    shelf_life_days_max: int | None = Query(
        default=None,
        description="Maximum shelf_life_days (inclusive).",
        examples=[730],
    ),
    created_at_from: datetime | None = Query(
        default=None,
        description="Filter created_at >= this datetime (ISO format).",
        examples=["2026-03-01T00:00:00Z"],
    ),
    created_at_to: datetime | None = Query(
        default=None,
        description="Filter created_at <= this datetime (ISO format).",
        examples=["2026-03-31T23:59:59Z"],
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filter by active or inactive SKU using `deactivated_at`.",
        examples=[True],
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number for paginated results.",
        examples=[1],
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of records per page. Maximum is 100.",
        examples=[20],
    ),
    sort_by: str = Query(
        default="sku_code",
        description="Sort field. Allowed: id, sku_code, sku_description, brand, category, supplier, sku_status, case_price, unit_price, created_at.",
        examples=["sku_code"],
    ),
    sort_dir: str = Query(
        default="asc",
        description="Sort direction: asc or desc.",
        examples=["asc"],
    ),
    db: Session = Depends(get_db),
) -> SKUListResponse:
    if sort_by not in SORTABLE_FIELDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by value. Allowed values: {', '.join(SORTABLE_FIELDS)}",
        )

    normalized_sort_dir = sort_dir.lower()
    if normalized_sort_dir not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort_dir value. Allowed values: asc, desc",
        )

    query = apply_sku_filters(
        db.query(SKU),
        sku_code=sku_code,
        sku_description=sku_description,
        master_distributor=master_distributor,
        distributor=distributor,
        line_of_business=line_of_business,
        supplier=supplier,
        agency=agency,
        category=category,
        segment=segment,
        brand=brand,
        sub_brand=sub_brand,
        sku_type=sku_type,
        promotion=promotion,
        sku_status=sku_status,
        case_price_min=case_price_min,
        case_price_max=case_price_max,
        unit_price_min=unit_price_min,
        unit_price_max=unit_price_max,
        shelf_life_days_min=shelf_life_days_min,
        shelf_life_days_max=shelf_life_days_max,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        is_active=is_active,
    )

    total = query.count()

    sort_column = SORTABLE_FIELDS[sort_by]
    order_by_clause = asc(sort_column) if normalized_sort_dir == "asc" else desc(sort_column)

    items = (
        query.order_by(order_by_clause, asc(SKU.id))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return SKUListResponse(
        items=[serialize_sku(item) for item in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get(
    "/filter-options",
    response_model=SKUFilterOptionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get SKU filter dropdown options",
    description=(
        "Returns distinct values for common SKU filter fields so the frontend can populate "
        "dropdowns and select boxes.\n\n"
        "This endpoint also supports cascading filters: pass the current selection "
        "such as `brand`, `category`, `promotion`, or range filters, and the response "
        "will be calculated from only the matching SKU rows."
    ),
    responses={
        200: {
            "description": "Distinct filter values returned successfully.",
        }
    },
)
def get_sku_filter_options(
    sku_code: str | None = Query(default=None, description="Partial match search on SKU code."),
    sku_description: str | None = Query(default=None, description="Partial match search on SKU description."),
    master_distributor: list[str] | None = Query(default=None, description="Filter master_distributor (supports multi)."),
    distributor: list[str] | None = Query(default=None, description="Filter distributor (supports multi)."),
    line_of_business: list[str] | None = Query(default=None, description="Filter line_of_business (supports multi)."),
    supplier: list[str] | None = Query(default=None, description="Filter supplier (supports multi)."),
    agency: list[str] | None = Query(default=None, description="Filter agency (supports multi)."),
    category: list[str] | None = Query(default=None, description="Filter category (supports multi)."),
    segment: list[str] | None = Query(default=None, description="Filter segment (supports multi)."),
    brand: list[str] | None = Query(default=None, description="Filter brand (supports multi)."),
    sub_brand: list[str] | None = Query(default=None, description="Filter sub_brand (supports multi)."),
    sku_type: list[str] | None = Query(default=None, description="Filter sku_type (supports multi)."),
    promotion: list[str] | None = Query(default=None, description="Filter promotion (supports multi)."),
    sku_status: list[str] | None = Query(default=None, description="Filter sku_status (supports multi)."),
    case_price_min: float | None = Query(default=None, description="Minimum case_price (inclusive)."),
    case_price_max: float | None = Query(default=None, description="Maximum case_price (inclusive)."),
    unit_price_min: float | None = Query(default=None, description="Minimum unit_price (inclusive)."),
    unit_price_max: float | None = Query(default=None, description="Maximum unit_price (inclusive)."),
    shelf_life_days_min: int | None = Query(default=None, description="Minimum shelf_life_days (inclusive)."),
    shelf_life_days_max: int | None = Query(default=None, description="Maximum shelf_life_days (inclusive)."),
    created_at_from: datetime | None = Query(default=None, description="Filter created_at >= this datetime (ISO format)."),
    created_at_to: datetime | None = Query(default=None, description="Filter created_at <= this datetime (ISO format)."),
    is_active: bool | None = Query(default=None, description="Filter by active/inactive using deactivated_at."),
    db: Session = Depends(get_db),
) -> SKUFilterOptionsResponse:
    """
    Cascading filter-options endpoint.
    If the frontend passes any filters here, we apply them first and then return distinct values
    for each dropdown based on the filtered dataset.
    """
    base_query = apply_sku_filters(
        db.query(SKU),
        sku_code=sku_code,
        sku_description=sku_description,
        master_distributor=master_distributor,
        distributor=distributor,
        line_of_business=line_of_business,
        supplier=supplier,
        agency=agency,
        category=category,
        segment=segment,
        brand=brand,
        sub_brand=sub_brand,
        sku_type=sku_type,
        promotion=promotion,
        sku_status=sku_status,
        case_price_min=case_price_min,
        case_price_max=case_price_max,
        unit_price_min=unit_price_min,
        unit_price_max=unit_price_max,
        shelf_life_days_min=shelf_life_days_min,
        shelf_life_days_max=shelf_life_days_max,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        is_active=is_active,
    )

    def distinct_for(column):
        rows = (
            base_query.with_entities(column)
            .filter(column.isnot(None))
            .distinct()
            .order_by(asc(column))
            .all()
        )
        out: list[str] = []
        for (value,) in rows:
            if isinstance(value, str) and value.strip():
                out.append(value.strip())
        return out

    return SKUFilterOptionsResponse(
        master_distributor=distinct_for(SKU.master_distributor),
        distributor=distinct_for(SKU.distributor),
        line_of_business=distinct_for(SKU.line_of_business),
        supplier=distinct_for(SKU.supplier),
        agency=distinct_for(SKU.agency),
        category=distinct_for(SKU.category),
        segment=distinct_for(SKU.segment),
        brand=distinct_for(SKU.brand),
        sub_brand=distinct_for(SKU.sub_brand),
        sku_type=distinct_for(SKU.sku_type),
        promotion=distinct_for(SKU.promotion),
        sku_status=distinct_for(SKU.sku_status),
    )
