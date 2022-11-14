from fastapi import APIRouter, Depends, status, Response

from ..services.accounts import AccountServices
from ..schemas.accounts import (
    ListAccountSchema,
    AccountResponse,
    CreateAccountSchema,
    UpdateAccountSchema,
)
from ..services.auth import RoleChecker

router = APIRouter(prefix="/api/accounts", tags=['accounts'])

ok = "ok"
allow_create_resource = RoleChecker(["admin"])
allow_read_resource = RoleChecker(["admin", "user"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ListAccountSchema,
    dependencies=[Depends(allow_read_resource)]
)
def get_accounts(
    service: AccountServices = Depends(),
    page: int = 0,
    page_size: int = None,
    order_by=None,
    is_desc: bool = False,
) -> dict:
    res, total, out_page_size, count = service.get_accounts(
     page, page_size, order_by, is_desc
    )
    return {
        "status": ok,
        "total": total,
        "count": count,
        "page": page,
        "page_size": page_size or out_page_size,
        "accounts": res,
    }


@router.get(
    "/{account_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountResponse,
    dependencies=[Depends(allow_read_resource)]
)
def get_account(
        account_id: str,
        service: AccountServices = Depends()
) -> dict:
    res = service.get_account(account_id)
    return {"status": ok, "account": res}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponse,
    dependencies=[Depends(allow_create_resource)]
)
def create_account(
    account: CreateAccountSchema,
    service: AccountServices = Depends()
) -> dict:
    res = service.create_account(account)
    return {"status": ok, "account": res}


@router.put(
    "/{account_id}",
    response_model=AccountResponse,
    dependencies=[Depends(allow_create_resource)]
)
def update_account(
    account_id: str,
        account: UpdateAccountSchema,
        service: AccountServices = Depends()
) -> dict:
    res = service.update_account(account_id, account)
    return {"status": ok, "account": res}


@router.delete(
    "/{account_id}",
    dependencies=[Depends(allow_create_resource)]
)
def delete_account(
        account_id: str,
        service: AccountServices = Depends()
) -> Response:
    return service.delete_account(account_id)
