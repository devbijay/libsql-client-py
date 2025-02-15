from __future__ import annotations
from typing import List, Optional, Union
from typing_extensions import Literal, NotRequired, TypedDict

### Errors

Error = TypedDict("Error", {
    "message": str,
    "code": NotRequired[Optional[str]],
})

### Values

ValueNull = TypedDict("ValueNull", {"type": Literal["null"]})
ValueInteger = TypedDict("ValueInteger", {"type": Literal["integer"], "value": str})
ValueFloat = TypedDict("ValueFloat", {"type": Literal["float"], "value": Union[float, int]})
ValueText = TypedDict("ValueText", {"type": Literal["text"], "value": str})
ValueBlob = TypedDict("ValueBlob", {"type": Literal["blob"], "base64": str})
Value = Union[ValueNull, ValueInteger, ValueFloat, ValueText, ValueBlob]

### Execute a statement

NamedArg = TypedDict("NamedArg", {
    "name": str,
    "value": Value,
})

Stmt = TypedDict("Stmt", {
    "sql": str,
    "args": NotRequired[List[Value]],
    "named_args": NotRequired[List[NamedArg]],
    "want_rows": bool,
})

Col = TypedDict("Col", {
    "name": Optional[str],
})

StmtResult = TypedDict("StmtResult", {
    "cols": List[Col],
    "rows": List[List[Value]],
    "affected_row_count": int,
    "last_insert_rowid": NotRequired[Optional[str]],
})

ExecuteReq = TypedDict("ExecuteReq", {
    "type": Literal["execute"],
    "stream_id": int,
    "stmt": Stmt,
})

ExecuteResp = TypedDict("ExecuteResp", {
    "type": Literal["execute"],
    "result": StmtResult,
})

### Execute a batch

BatchCondOk = TypedDict("BatchCondOk", {"type": Literal["ok"], "step": int})
BatchCondError = TypedDict("BatchCondError", {"type": Literal["error"], "step": int})
BatchCondNot = TypedDict("BatchCondNot", {"type": Literal["not"], "cond": "BatchCond"})
BatchCondAnd = TypedDict("BatchCondAnd", {"type": Literal["and"], "conds": List["BatchCond"]})
BatchCondOr = TypedDict("BatchCondOr", {"type": Literal["or"], "conds": List["BatchCond"]})
BatchCond = Union[BatchCondOk, BatchCondError, BatchCondNot, BatchCondAnd, BatchCondOr]

BatchStep = TypedDict("BatchStep", {
    "condition": NotRequired[Optional[BatchCond]],
    "stmt": Stmt,
})

Batch = TypedDict("Batch", {
    "steps": List[BatchStep],
})

BatchReq = TypedDict("BatchReq", {
    "type": Literal["batch"],
    "stream_id": int,
    "batch": Batch,
})

BatchResult = TypedDict("BatchResult", {
    "step_results": List[Optional[StmtResult]],
    "step_errors": List[Optional[Error]],
})

BatchResp = TypedDict("BatchResp", {
    "type": Literal["batch"],
    "result": BatchResult,
})

### Open stream

OpenStreamReq = TypedDict("OpenStreamReq", {
    "type": Literal["open_stream"],
    "stream_id": int,
})

OpenStreamResp = TypedDict("OpenStreamResp", {
    "type": Literal["open_stream"],
})

### Close stream

CloseStreamReq = TypedDict("CloseStreamReq", {
    "type": Literal["close_stream"],
    "stream_id": int,
})

CloseStreamResp = TypedDict("CloseStreamResp", {
    "type": Literal["close_stream"],
})

### Hello

HelloMsg = TypedDict("HelloMsg", {
    "type": Literal["hello"],
    "jwt": Optional[str],
})

HelloOkMsg = TypedDict("HelloOkMsg", {
    "type": Literal["hello_ok"],
})

HelloErrorMsg = TypedDict("HelloErrorMsg", {
    "type": Literal["hello_error"],
    "error": Error,
})

### Request/response

Request = Union[
    OpenStreamReq,
    CloseStreamReq,
    ExecuteReq,
    BatchReq,
]

RequestMsg = TypedDict("RequestMsg", {
    "type": Literal["request"],
    "request_id": int,
    "request": Request,
})

Response = Union[
    OpenStreamResp,
    CloseStreamResp,
    ExecuteResp,
    BatchResp,
]

ResponseOkMsg = TypedDict("ResponseOkMsg", {
    "type": Literal["response_ok"],
    "request_id": int,
    "response": Response,
})

ResponseErrorMsg = TypedDict("ResponseErrorMsg", {
    "type": Literal["response_error"],
    "request_id": int,
    "error": Error,
})

## Messages

ClientMsg = Union[
    HelloMsg,
    RequestMsg,
]
ServerMsg = Union[
    HelloOkMsg,
    HelloErrorMsg,
    ResponseOkMsg,
    ResponseErrorMsg,
]
