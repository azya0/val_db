from fastapi import APIRouter, HTTPException

from queries import test_queries
from routers.schemas import TestResults

router = APIRouter(
    prefix="/test",
    tags=["test"],
)


commands = [
    test_queries.fill_tables,
    test_queries.search_by_key,
    test_queries.search_by_non_key,
    test_queries.search_by_mask,
    test_queries.add_one_row,
    test_queries.add_many_rows,
    test_queries.update_row_by_key,
    test_queries.update_row_by_non_key,
    test_queries.delete_row_by_key,
    test_queries.delete_row_by_non_key,
    test_queries.delete_rows,
    test_queries.delete_rows_by_non_key,
    test_queries.delete_200_rows,
    test_queries.remain_200_rows,
    test_queries.vacuum_tables
]


@router.post('/create')
async def create():
    try:
        await test_queries.fill_tables()
    except Exception:
        return "Уже создана!"


@router.get('/do/all', response_model=list[TestResults])
async def do_test_all():
    result = []
    for test_id in range(1, 14):
        result.append(await do_test(test_id))
    
    return result


@router.get('/do/{test_nubmer}', response_model=TestResults)
async def do_test(test_nubmer: int):
    data = None

    if test_nubmer == 14:
        data = await test_queries.vacuum_tables()

    if 1 <= test_nubmer <= 13:
        data = await commands[test_nubmer](1)

    if data is None:
        raise HTTPException(404, detail="no such test nubmer")

    return TestResults(test_name=data[0],
                result_100000=data[1][0],
                result_10000=data[1][1],
                result_1000=data[1][2])


