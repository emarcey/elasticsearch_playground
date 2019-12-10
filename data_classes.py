from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Query:
    query_type: str
    query_maker: callable
    index_override: Optional[str] = None


@dataclass
class QueryParams:
    base_url: str
    index: str
    num_iterations: int
    es_from: int
    es_sizes: List[int]
    params: Dict[str, Any] = field(default_factory=dict)
    header: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResults:
    es_size: int
    query_val: str
    query_type: str
    query_times: List[int]
    query_hits: List[Any]
    index_override: Optional[str] = None
