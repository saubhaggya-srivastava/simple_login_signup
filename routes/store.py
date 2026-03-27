from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from db.database import get_db
from models.store import Store
from schemas.store import StoreFilterOptionsResponse, StoreListResponse

router = APIRouter(prefix="/stores", tags=["Store"])

SORTABLE_FIELDS = {
    "id": Store.id,
    "store_code": Store.store_code,
    "store_name": Store.store_name,
    "retailer_name": Store.retailer_name,
    "city": Store.city,
    "channel": Store.channel,
    "store_status": Store.store_status,
    "distributor": Store.distributor,
    "created_at": Store.created_at,
}


def serialize_store(store: Store) -> dict:
    return {
        "id": store.id,
        "region": store.region,
        "country": store.country,
        "master_distributor": store.master_distributor,
        "retailer_code": store.retailer_code,
        "retailer_name": store.retailer_name,
        "store_code": store.store_code,
        "store_name": store.store_name,
        "store_code_distributor": store.store_code_distributor,
        "distributor": store.distributor,
        "store_code_lob": store.store_code_lob,
        "line_of_business": store.line_of_business,
        "city": store.city,
        "area": store.area,
        "retailer_group": store.retailer_group,
        "retailer_sub_group": store.retailer_sub_group,
        "channel": store.channel,
        "sub_channel": store.sub_channel,
        "store_status": store.store_status,
        "central_buying": store.central_buying,
        "central_store_code": store.central_store_code,
        "salesmen": store.salesmen,
        "gps_coordinate": store.gps_coordinate,
        "created_at": store.created_at,
        "deactivated_at": store.deactivated_at,
    }


def normalize_multi(values: list[str] | None) -> list[str] | None:
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


def apply_store_filters(
    query,
    *,
    store_code: str | None,
    store_name: str | None,
    retailer_code: str | None,
    region: list[str] | None,
    country: list[str] | None,
    master_distributor: list[str] | None,
    retailer_name: list[str] | None,
    distributor: list[str] | None,
    line_of_business: list[str] | None,
    city: list[str] | None,
    area: list[str] | None,
    retailer_group: list[str] | None,
    retailer_sub_group: list[str] | None,
    channel: list[str] | None,
    sub_channel: list[str] | None,
    store_status: list[str] | None,
    central_buying: list[str] | None,
    salesmen: list[str] | None,
    created_at_from: datetime | None,
    created_at_to: datetime | None,
    is_active: bool | None,
):
    if store_code:
        query = query.filter(Store.store_code.ilike(f"%{store_code.strip()}%"))
    if store_name:
        query = query.filter(Store.store_name.ilike(f"%{store_name.strip()}%"))
    if retailer_code:
        query = query.filter(Store.retailer_code.ilike(f"%{retailer_code.strip()}%"))

    exact_multi_filters = {
        "region": normalize_multi(region),
        "country": normalize_multi(country),
        "master_distributor": normalize_multi(master_distributor),
        "retailer_name": normalize_multi(retailer_name),
        "distributor": normalize_multi(distributor),
        "line_of_business": normalize_multi(line_of_business),
        "city": normalize_multi(city),
        "area": normalize_multi(area),
        "retailer_group": normalize_multi(retailer_group),
        "retailer_sub_group": normalize_multi(retailer_sub_group),
        "channel": normalize_multi(channel),
        "sub_channel": normalize_multi(sub_channel),
        "store_status": normalize_multi(store_status),
        "central_buying": normalize_multi(central_buying),
        "salesmen": normalize_multi(salesmen),
    }

    for field_name, values in exact_multi_filters.items():
        if values:
            query = query.filter(getattr(Store, field_name).in_(values))

    if created_at_from is not None:
        query = query.filter(Store.created_at >= created_at_from)
    if created_at_to is not None:
        query = query.filter(Store.created_at <= created_at_to)

    if is_active is True:
        query = query.filter(Store.deactivated_at.is_(None))
    elif is_active is False:
        query = query.filter(Store.deactivated_at.is_not(None))

    return query


@router.get(
    "",
    response_model=StoreListResponse,
    status_code=status.HTTP_200_OK,
    summary="List and filter stores",
    description=(
        "Returns paginated store records from `store_master`.\n\n"
        "Supported features:\n"
        "- partial text search on `store_code`, `store_name`, and `retailer_code`\n"
        "- exact-match filters for business fields like `region`, `city`, `channel`, `distributor`, etc.\n"
        "- multi-select filters using repeated params or comma-separated values\n"
        "- range filter on `created_at`\n"
        "- sorting and pagination"
    ),
    responses={
        200: {"description": "Filtered store list returned successfully."},
        400: {"description": "Invalid sorting parameter supplied."},
    },
)
def list_stores(
    store_code: str | None = Query(
        default=None,
        description="Partial match search on store code.",
        examples=["1790021"],
    ),
    store_name: str | None = Query(
        default=None,
        description="Partial match search on store name.",
        examples=["HYPERMARKET"],
    ),
    retailer_code: str | None = Query(
        default=None,
        description="Partial match search on retailer code.",
        examples=["131829"],
    ),
    region: list[str] | None = Query(
        default=None,
        description="Exact match filter for region (multi-select).",
        examples=["Middle East"],
    ),
    country: list[str] | None = Query(
        default=None,
        description="Exact match filter for country (multi-select).",
        examples=["Qatar"],
    ),
    master_distributor: list[str] | None = Query(
        default=None,
        description="Exact match filter for master distributor (multi-select).",
        examples=["Abu Ali"],
    ),
    retailer_name: list[str] | None = Query(
        default=None,
        description="Exact match filter for retailer name (multi-select).",
        examples=["2022 HYPERMARKET"],
    ),
    distributor: list[str] | None = Query(
        default=None,
        description="Exact match filter for distributor (multi-select).",
        examples=["Ali Products"],
    ),
    line_of_business: list[str] | None = Query(
        default=None,
        description="Exact match filter for line of business (multi-select).",
        examples=["Delmond"],
    ),
    city: list[str] | None = Query(
        default=None,
        description="Exact match filter for city (multi-select).",
        examples=["DOHA"],
    ),
    area: list[str] | None = Query(
        default=None,
        description="Exact match filter for area (multi-select).",
        examples=["DOHA"],
    ),
    retailer_group: list[str] | None = Query(
        default=None,
        description="Exact match filter for retailer group (multi-select).",
        examples=["Others"],
    ),
    retailer_sub_group: list[str] | None = Query(
        default=None,
        description="Exact match filter for retailer sub group (multi-select).",
        examples=["Others"],
    ),
    channel: list[str] | None = Query(
        default=None,
        description="Exact match filter for channel (multi-select).",
        examples=["Minimart"],
    ),
    sub_channel: list[str] | None = Query(
        default=None,
        description="Exact match filter for sub channel (multi-select).",
        examples=["Minimart A"],
    ),
    store_status: list[str] | None = Query(
        default=None,
        description="Exact match filter for store status (multi-select).",
        examples=["Active"],
    ),
    central_buying: list[str] | None = Query(
        default=None,
        description="Exact match filter for central buying (multi-select).",
        examples=["Yes"],
    ),
    salesmen: list[str] | None = Query(
        default=None,
        description="Exact match filter for salesmen (multi-select).",
        examples=["Arun Kareem"],
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
        description="Filter by active or inactive store using `deactivated_at`.",
        examples=[True],
    ),
    page: int = Query(
        default=1, ge=1,
        description="Page number for paginated results.",
        examples=[1],
    ),
    limit: int = Query(
        default=20, ge=1, le=100,
        description="Number of records per page. Maximum is 100.",
        examples=[20],
    ),
    sort_by: str = Query(
        default="store_code",
        description=(
            "Sort field. Allowed: id, store_code, store_name, retailer_name, "
            "city, channel, store_status, distributor, created_at."
        ),
        examples=["store_code"],
    ),
    sort_dir: str = Query(
        default="asc",
        description="Sort direction: asc or desc.",
        examples=["asc"],
    ),
    db: Session = Depends(get_db),
) -> StoreListResponse:
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

    query = apply_store_filters(
        db.query(Store),
        store_code=store_code,
        store_name=store_name,
        retailer_code=retailer_code,
        region=region,
        country=country,
        master_distributor=master_distributor,
        retailer_name=retailer_name,
        distributor=distributor,
        line_of_business=line_of_business,
        city=city,
        area=area,
        retailer_group=retailer_group,
        retailer_sub_group=retailer_sub_group,
        channel=channel,
        sub_channel=sub_channel,
        store_status=store_status,
        central_buying=central_buying,
        salesmen=salesmen,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        is_active=is_active,
    )

    total = query.count()

    sort_column = SORTABLE_FIELDS[sort_by]
    order_by_clause = asc(sort_column) if normalized_sort_dir == "asc" else desc(sort_column)

    items = (
        query.order_by(order_by_clause, asc(Store.id))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return StoreListResponse(
        items=[serialize_store(item) for item in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get(
    "/filter-options",
    response_model=StoreFilterOptionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get store filter dropdown options",
    description=(
        "Returns distinct values for common store filter fields so the frontend can populate "
        "dropdowns and select boxes.\n\n"
        "Supports cascading filters: pass the current selection and the response "
        "will be calculated from only the matching store rows."
    ),
    responses={
        200: {"description": "Distinct filter values returned successfully."},
    },
)
def get_store_filter_options(
    store_code: str | None = Query(default=None, description="Partial match on store code."),
    store_name: str | None = Query(default=None, description="Partial match on store name."),
    retailer_code: str | None = Query(default=None, description="Partial match on retailer code."),
    region: list[str] | None = Query(default=None, description="Filter region (multi-select)."),
    country: list[str] | None = Query(default=None, description="Filter country (multi-select)."),
    master_distributor: list[str] | None = Query(default=None, description="Filter master distributor (multi-select)."),
    retailer_name: list[str] | None = Query(default=None, description="Filter retailer name (multi-select)."),
    distributor: list[str] | None = Query(default=None, description="Filter distributor (multi-select)."),
    line_of_business: list[str] | None = Query(default=None, description="Filter line of business (multi-select)."),
    city: list[str] | None = Query(default=None, description="Filter city (multi-select)."),
    area: list[str] | None = Query(default=None, description="Filter area (multi-select)."),
    retailer_group: list[str] | None = Query(default=None, description="Filter retailer group (multi-select)."),
    retailer_sub_group: list[str] | None = Query(default=None, description="Filter retailer sub group (multi-select)."),
    channel: list[str] | None = Query(default=None, description="Filter channel (multi-select)."),
    sub_channel: list[str] | None = Query(default=None, description="Filter sub channel (multi-select)."),
    store_status: list[str] | None = Query(default=None, description="Filter store status (multi-select)."),
    central_buying: list[str] | None = Query(default=None, description="Filter central buying (multi-select)."),
    salesmen: list[str] | None = Query(default=None, description="Filter salesmen (multi-select)."),
    created_at_from: datetime | None = Query(default=None, description="Filter created_at >= this datetime."),
    created_at_to: datetime | None = Query(default=None, description="Filter created_at <= this datetime."),
    is_active: bool | None = Query(default=None, description="Filter by active/inactive using deactivated_at."),
    db: Session = Depends(get_db),
) -> StoreFilterOptionsResponse:
    base_query = apply_store_filters(
        db.query(Store),
        store_code=store_code,
        store_name=store_name,
        retailer_code=retailer_code,
        region=region,
        country=country,
        master_distributor=master_distributor,
        retailer_name=retailer_name,
        distributor=distributor,
        line_of_business=line_of_business,
        city=city,
        area=area,
        retailer_group=retailer_group,
        retailer_sub_group=retailer_sub_group,
        channel=channel,
        sub_channel=sub_channel,
        store_status=store_status,
        central_buying=central_buying,
        salesmen=salesmen,
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

    return StoreFilterOptionsResponse(
        region=distinct_for(Store.region),
        country=distinct_for(Store.country),
        master_distributor=distinct_for(Store.master_distributor),
        retailer_name=distinct_for(Store.retailer_name),
        distributor=distinct_for(Store.distributor),
        line_of_business=distinct_for(Store.line_of_business),
        city=distinct_for(Store.city),
        area=distinct_for(Store.area),
        retailer_group=distinct_for(Store.retailer_group),
        retailer_sub_group=distinct_for(Store.retailer_sub_group),
        channel=distinct_for(Store.channel),
        sub_channel=distinct_for(Store.sub_channel),
        store_status=distinct_for(Store.store_status),
        central_buying=distinct_for(Store.central_buying),
        salesmen=distinct_for(Store.salesmen),
    )
