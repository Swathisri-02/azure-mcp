from aiohttp import web
import json
from handlers.postgres_handler import query_postgres

routes = web.RouteTableDef()

@routes.post("/api/actions/run_postgres_query")
async def run_query(request):
    try:
        body = await request.json()
        question = body.get("input", {}).get("question")
        if not question:
            return web.json_response({"error": "Missing 'question'"}, status=400)
        
        results = query_postgres(question)
        return web.json_response({"type": "message", "message": results})

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=3000)