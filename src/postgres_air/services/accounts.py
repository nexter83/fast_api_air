from datetime import datetime

from fastapi import Depends, HTTPException, status, Response
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi_pagination import paginate
from ..database import get_session
from ..models.accounts import Account


class AccountServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_account(self, account_id):
        query = self.session.query(Account).filter_by(account_id=account_id)
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return query

    def get_accounts(self, order_by=None, is_desc: bool = False):
        query = self.session.query(Account)
        if order_by:
            query = query.order_by(desc(order_by)) if is_desc else query.order_by(order_by)
        return paginate(query.all())

    def get_account(self, account_id):
        res = self._get_account(account_id)
        return res.first()

    def create_account(self, account):
        new_account = Account(**account.dict())
        self.session.add(new_account)
        self.session.commit()
        self.session.refresh(new_account)
        return new_account

    def update_account(self, account_id, account):
        account_query = self._get_account(account_id)
        if not account_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        account.update_ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        account_query.update(account.dict(exclude_none=True))
        self.session.commit()
        return account_query.first()

    def delete_account(self, account_id):
        account_query = self._get_account(account_id)
        if not account_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        account_m = account_query.first()
        if not account_m:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No account with this id: {account_id} found",
            )
        account_query.delete()
        self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
