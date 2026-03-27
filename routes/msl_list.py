from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from db.database import get_db
from models.msl_list import MSLList
from schemas.msl_list import MSLListFilterOptionsResponse, MSLListPageResponse

router = APIRouter(prefix="/msl-list", tags=["MSL List"])

SORTABLE_FIELDS = {
    "id": MSLList.id,
    "sku_parent_code": MSLList.sku_parent_code,
    "sku_code": MSLList.sku_code,
    "sku_description": MSLList.sku_description,
    "created_at": MSLList.created_at,
}

NUMERIC_FILTER_FIELDS = {
    "warehouse",
    "hyper_a",
    "hyper_b",
    "super_a",
    "super_b",
    "minimart_a",
    "minimart_b",
    "grocery_a",
    "grocery_b",
    "grocery_c",
    "ecom_a",
    "ecom_b",
    "petrol_pumps_a",
    "petrol_pumps_b",
    "petrol_pumps_c",
    "pharmacy_a",
    "pharmacy_b",
    "pharmacy_c",
    "wholesale",
    "horeca",
}


def serialize_msl_item(item: MSLList) -> dict:
    return {
        "id": item.id,
        "sku_parent_code": item.sku_parent_code,
        "sku_code": item.sku_code,
        "sku_description": item.sku_description,
        "warehouse": item.warehouse,
        "hyper_a": item.hyper_a,
        "hyper_b": item.hyper_b,
        "super_a": item.super_a,
        "super_b": item.super_b,
        "minimart_a": item.minimart_a,
        "minimart_b": item.minimart_b,
        "grocery_a": item.grocery_a,
        "grocery_b": item.grocery_b,
        "grocery_c": item.grocery_c,
        "ecom_a": item.ecom_a,
        "ecom_b": item.ecom_b,
        "petrol_pumps_a": item.petrol_pumps_a,
        "petrol_pumps_b": item.petrol_pumps_b,
        "petrol_pumps_c": item.petrol_pumps_c,
        "pharmacy_a": item.pharmacy_a,
        "pharmacy_b": item.pharmacy_b,
        "pharmacy_c": item.pharmacy_c,
        "wholesale": item.wholesale,
        "horeca": item.horeca,
        "created_at": item.created_at,
        "deactivated_at": item.deactivated_at,
    }


def apply_msl_filters(
    query,
    *,
    sku_parent_code: str | None,
    sku_code: str | None,
    sku_description: str | None,
    warehouse: int | None,
    hyper_a: int | None,
    hyper_b: int | None,
    super_a: int | None,
    super_b: int | None,
    minimart_a: int | None,
    minimart_b: int | None,
    grocery_a: int | None,
    grocery_b: int | None,
    grocery_c: int | None,
    ecom_a: int | None,
    ecom_b: int | None,
    petrol_pumps_a: int | None,
    petrol_pumps_b: int | None,
    petrol_pumps_c: int | None,
    pharmacy_a: int | None,
    pharmacy_b: int | None,
    pharmacy_c: int | None,
    wholesale: int | None,
    horeca: int | None,
    created_at_from: datetime | None,
    created_at_to: datetime | None,
    is_active: bool | None,
):
    if sku_parent_code:
        query = query.filter(MSLList.sku_parent_code.ilike(f"%{sku_parent_code.strip()}%"))
    if sku_code:
        query = query.filter(MSLList.sku_code.ilike(f"%{sku_code.strip()}%"))
    if sku_description:
        query = query.filter(MSLList.sku_description.ilike(f"%{sku_description.strip()}%"))

    numeric_filters = {
        "warehouse": warehouse,
        "hyper_a": hyper_a,
        "hyper_b": hyper_b,
        "super_a": super_a,
        "super_b": super_b,
        "minimart_a": minimart_a,
        "minimart_b": minimart_b,
        "grocery_a": grocery_a,
        "grocery_b": grocery_b,
        "grocery_c": grocery_c,
        "ecom_a": ecom_a,
        "ecom_b": ecom_b,
        "petrol_pumps_a": petrol_pumps_a,
        "petrol_pumps_b": petrol_pumps_b,
        "petrol_pumps_c": petrol_pumps_c,
        "pharmacy_a": pharmacy_a,
        "pharmacy_b": pharmacy_b,
        "pharmacy_c": pharmacy_c,
        "wholesale": wholesale,
        "horeca": horeca,
    }
    for field_name, value in numeric_filters.items():
        if value is not None:
            query = query.filter(getattr(MSLList, field_name) == value)

    if created_at_from is not None:
        query = query.filter(MSLList.created_at >= created_at_from)
    if created_at_to is not None:
        query = query.filter(MSLList.created_at <= created_at_to)

    if is_active is True:
        query = query.filter(MSLList.deactivated_at.is_(None))
    elif is_active is False:
        query = query.filter(MSLList.deactivated_at.is_not(None))

    return query


@router.get(
    "",
    response_model=MSLListPageResponse,
    status_code=status.HTTP_200_OK,
    summary="List and filter MSL records",
    description=(
        "Returns paginated records from `msl_list`.\n\n"
        "Supported features:\n"
        "- partial text search on `sku_parent_code`, `sku_code`, and `sku_description`\n"
        "- exact-match filters for all MSL numeric flags\n"
        "- range filter on `created_at`\n"
        "- sorting and pagination"
    ),
    responses={
        200: {"description": "Filtered MSL list returned successfully."},
        400: {"description": "Invalid sorting parameter supplied."},
    },
)
def list_msl_items(
    sku_parent_code: str | None = Query(default=None, description="Partial match search on SKU parent code.", examples=["1104000700"]),
    sku_code: str | None = Query(default=None, description="Partial match search on SKU code.", examples=["1104000700"]),
    sku_description: str | None = Query(default=None, description="Partial match search on SKU description.", examples=["Delphy"]),
    warehouse: int | None = Query(default=None, ge=0, le=1, description="Exact filter for warehouse flag.", examples=[1]),
    hyper_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Hyper A flag.", examples=[1]),
    hyper_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Hyper B flag.", examples=[1]),
    super_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Super A flag.", examples=[1]),
    super_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Super B flag.", examples=[1]),
    minimart_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Minimart A flag.", examples=[0]),
    minimart_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Minimart B flag.", examples=[0]),
    grocery_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Grocery A flag.", examples=[0]),
    grocery_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Grocery B flag.", examples=[0]),
    grocery_c: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Grocery C flag.", examples=[0]),
    ecom_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for ECom A flag.", examples=[0]),
    ecom_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for ECom B flag.", examples=[0]),
    petrol_pumps_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Petrol Pumps A flag.", examples=[0]),
    petrol_pumps_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Petrol Pumps B flag.", examples=[0]),
    petrol_pumps_c: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Petrol Pumps C flag.", examples=[0]),
    pharmacy_a: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Pharmacy A flag.", examples=[0]),
    pharmacy_b: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Pharmacy B flag.", examples=[0]),
    pharmacy_c: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Pharmacy C flag.", examples=[0]),
    wholesale: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Wholesale flag.", examples=[0]),
    horeca: int | None = Query(default=None, ge=0, le=1, description="Exact filter for Horeca flag.", examples=[0]),
    created_at_from: datetime | None = Query(default=None, description="Filter created_at >= this datetime (ISO format).", examples=["2026-03-01T00:00:00Z"]),
    created_at_to: datetime | None = Query(default=None, description="Filter created_at <= this datetime (ISO format).", examples=["2026-03-31T23:59:59Z"]),
    is_active: bool | None = Query(default=None, description="Filter by active or inactive record using `deactivated_at`.", examples=[True]),
    page: int = Query(default=1, ge=1, description="Page number for paginated results.", examples=[1]),
    limit: int = Query(default=20, ge=1, le=100, description="Number of records per page. Maximum is 100.", examples=[20]),
    sort_by: str = Query(default="sku_code", description="Sort field. Allowed: id, sku_parent_code, sku_code, sku_description, created_at.", examples=["sku_code"]),
    sort_dir: str = Query(default="asc", description="Sort direction: asc or desc.", examples=["asc"]),
    db: Session = Depends(get_db),
) -> MSLListPageResponse:
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

    query = apply_msl_filters(
        db.query(MSLList),
        sku_parent_code=sku_parent_code,
        sku_code=sku_code,
        sku_description=sku_description,
        warehouse=warehouse,
        hyper_a=hyper_a,
        hyper_b=hyper_b,
        super_a=super_a,
        super_b=super_b,
        minimart_a=minimart_a,
        minimart_b=minimart_b,
        grocery_a=grocery_a,
        grocery_b=grocery_b,
        grocery_c=grocery_c,
        ecom_a=ecom_a,
        ecom_b=ecom_b,
        petrol_pumps_a=petrol_pumps_a,
        petrol_pumps_b=petrol_pumps_b,
        petrol_pumps_c=petrol_pumps_c,
        pharmacy_a=pharmacy_a,
        pharmacy_b=pharmacy_b,
        pharmacy_c=pharmacy_c,
        wholesale=wholesale,
        horeca=horeca,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        is_active=is_active,
    )

    total = query.count()
    sort_column = SORTABLE_FIELDS[sort_by]
    order_by_clause = asc(sort_column) if normalized_sort_dir == "asc" else desc(sort_column)

    items = (
        query.order_by(order_by_clause, asc(MSLList.id))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return MSLListPageResponse(
        items=[serialize_msl_item(item) for item in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get(
    "/filter-options",
    response_model=MSLListFilterOptionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get MSL filter dropdown options",
    description=(
        "Returns distinct values for MSL filter fields so the frontend can populate "
        "dropdowns and select boxes.\n\n"
        "Supports cascading filters: pass the current selection and the response "
        "will be calculated from only the matching MSL rows."
    ),
    responses={
        200: {"description": "Distinct filter values returned successfully."},
    },
)
def get_msl_filter_options(
    sku_parent_code: str | None = Query(default=None, description="Partial match on SKU parent code."),
    sku_code: str | None = Query(default=None, description="Partial match on SKU code."),
    sku_description: str | None = Query(default=None, description="Partial match on SKU description."),
    warehouse: int | None = Query(default=None, ge=0, le=1, description="Filter warehouse flag."),
    hyper_a: int | None = Query(default=None, ge=0, le=1, description="Filter Hyper A flag."),
    hyper_b: int | None = Query(default=None, ge=0, le=1, description="Filter Hyper B flag."),
    super_a: int | None = Query(default=None, ge=0, le=1, description="Filter Super A flag."),
    super_b: int | None = Query(default=None, ge=0, le=1, description="Filter Super B flag."),
    minimart_a: int | None = Query(default=None, ge=0, le=1, description="Filter Minimart A flag."),
    minimart_b: int | None = Query(default=None, ge=0, le=1, description="Filter Minimart B flag."),
    grocery_a: int | None = Query(default=None, ge=0, le=1, description="Filter Grocery A flag."),
    grocery_b: int | None = Query(default=None, ge=0, le=1, description="Filter Grocery B flag."),
    grocery_c: int | None = Query(default=None, ge=0, le=1, description="Filter Grocery C flag."),
    ecom_a: int | None = Query(default=None, ge=0, le=1, description="Filter ECom A flag."),
    ecom_b: int | None = Query(default=None, ge=0, le=1, description="Filter ECom B flag."),
    petrol_pumps_a: int | None = Query(default=None, ge=0, le=1, description="Filter Petrol Pumps A flag."),
    petrol_pumps_b: int | None = Query(default=None, ge=0, le=1, description="Filter Petrol Pumps B flag."),
    petrol_pumps_c: int | None = Query(default=None, ge=0, le=1, description="Filter Petrol Pumps C flag."),
    pharmacy_a: int | None = Query(default=None, ge=0, le=1, description="Filter Pharmacy A flag."),
    pharmacy_b: int | None = Query(default=None, ge=0, le=1, description="Filter Pharmacy B flag."),
    pharmacy_c: int | None = Query(default=None, ge=0, le=1, description="Filter Pharmacy C flag."),
    wholesale: int | None = Query(default=None, ge=0, le=1, description="Filter Wholesale flag."),
    horeca: int | None = Query(default=None, ge=0, le=1, description="Filter Horeca flag."),
    created_at_from: datetime | None = Query(default=None, description="Filter created_at >= this datetime."),
    created_at_to: datetime | None = Query(default=None, description="Filter created_at <= this datetime."),
    is_active: bool | None = Query(default=None, description="Filter by active/inactive using deactivated_at."),
    db: Session = Depends(get_db),
) -> MSLListFilterOptionsResponse:
    base_query = apply_msl_filters(
        db.query(MSLList),
        sku_parent_code=sku_parent_code,
        sku_code=sku_code,
        sku_description=sku_description,
        warehouse=warehouse,
        hyper_a=hyper_a,
        hyper_b=hyper_b,
        super_a=super_a,
        super_b=super_b,
        minimart_a=minimart_a,
        minimart_b=minimart_b,
        grocery_a=grocery_a,
        grocery_b=grocery_b,
        grocery_c=grocery_c,
        ecom_a=ecom_a,
        ecom_b=ecom_b,
        petrol_pumps_a=petrol_pumps_a,
        petrol_pumps_b=petrol_pumps_b,
        petrol_pumps_c=petrol_pumps_c,
        pharmacy_a=pharmacy_a,
        pharmacy_b=pharmacy_b,
        pharmacy_c=pharmacy_c,
        wholesale=wholesale,
        horeca=horeca,
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
        out: list = []
        for (value,) in rows:
            if isinstance(value, str):
                cleaned = value.strip()
                if cleaned:
                    out.append(cleaned)
            elif isinstance(value, int):
                out.append(value)
        return out

    return MSLListFilterOptionsResponse(
        sku_parent_code=distinct_for(MSLList.sku_parent_code),
        sku_code=distinct_for(MSLList.sku_code),
        sku_description=distinct_for(MSLList.sku_description),
        warehouse=distinct_for(MSLList.warehouse),
        hyper_a=distinct_for(MSLList.hyper_a),
        hyper_b=distinct_for(MSLList.hyper_b),
        super_a=distinct_for(MSLList.super_a),
        super_b=distinct_for(MSLList.super_b),
        minimart_a=distinct_for(MSLList.minimart_a),
        minimart_b=distinct_for(MSLList.minimart_b),
        grocery_a=distinct_for(MSLList.grocery_a),
        grocery_b=distinct_for(MSLList.grocery_b),
        grocery_c=distinct_for(MSLList.grocery_c),
        ecom_a=distinct_for(MSLList.ecom_a),
        ecom_b=distinct_for(MSLList.ecom_b),
        petrol_pumps_a=distinct_for(MSLList.petrol_pumps_a),
        petrol_pumps_b=distinct_for(MSLList.petrol_pumps_b),
        petrol_pumps_c=distinct_for(MSLList.petrol_pumps_c),
        pharmacy_a=distinct_for(MSLList.pharmacy_a),
        pharmacy_b=distinct_for(MSLList.pharmacy_b),
        pharmacy_c=distinct_for(MSLList.pharmacy_c),
        wholesale=distinct_for(MSLList.wholesale),
        horeca=distinct_for(MSLList.horeca),
    )
