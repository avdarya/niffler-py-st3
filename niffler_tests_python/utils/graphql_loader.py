from pathlib import Path


def load_graphql_query(name: str) -> str:
    path = Path(__file__).parent.parent / 'graphql_queries' / f"{name}.graphql"
    return path.read_text(encoding="utf-8")