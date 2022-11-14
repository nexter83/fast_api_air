from sqlalchemy import desc


def create_query(
        session, model, filters=None, page=0, page_size=None, order_by=None, is_desc=None
):
    query = session.query(model)
    if filters:
        query = query.filter_by(**filters)
    if order_by:
        if is_desc:
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)
    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset(page * page_size)
    total = query.count()
    if total > 100:
        page_size = 100
        query = query.limit(page_size)
        query = query.offset(page * page_size)
    return query, total, page_size
