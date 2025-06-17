from aiohttp import web
import json
from handlers.postgres_handler import query_postgres
from handlers.nl_sql_utils import get_table_schema, nl_to_sql

routes = web.RouteTableDef()

@routes.post("/api/actions/run_postgres_query")
async def run_postgres_query(request):
    try:
        body = await request.json()
        nl_question = body["input"]["question"]

        # Hardcoded table for now — we can extract it later with GPT
        table_name = "transactions_2021"
        schema_str = get_table_schema(table_name)
        sql_query = nl_to_sql(nl_question, schema_str)
        result = query_postgres(sql_query)

        return web.json_response({
            "type": "message",
            "message": {
                "query": sql_query,
                "result": result
            }
        })

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=3000)