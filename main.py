from __future__ import annotations
import os
from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from app.db import get_db
from app.models import IssueCreate, IssueUpdate, IssueOut, PaginatedIssues

app = FastAPI(title="Issue Tracker API")

# CORS
cors_origin = os.getenv("CORS_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin] if cors_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def as_issue_out(doc) -> IssueOut:
    return IssueOut(
        id=str(doc["_id"]),
        title=doc["title"],
        status=doc["status"],
        priority=doc["priority"],
        assignee=doc.get("assignee"),
        description=doc.get("description"),
        createdAt=doc["createdAt"],
        updatedAt=doc["updatedAt"],
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/issues", response_model=PaginatedIssues)
async def list_issues(
    search: Optional[str] = Query(default=None, description="search in title"),
    status: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    assignee: Optional[str] = Query(default=None),
    sortBy: str = Query(default="updatedAt"),
    sortOrder: str = Query(default="desc", pattern="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=10, ge=1, le=100),
):
    db = get_db()
    coll = db["issues"]

    query: dict = {}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if assignee:
        query["assignee"] = {"$regex": assignee, "$options": "i"}

    # allowed sort fields
    sort_field_map = {
        "id": "_id",
        "title": "title",
        "status": "status",
        "priority": "priority",
        "assignee": "assignee",
        "updatedAt": "updatedAt",
        "createdAt": "createdAt",
    }
    sort_field = sort_field_map.get(sortBy, "updatedAt")
    sort_direction = 1 if sortOrder == "asc" else -1

    total = await coll.count_documents(query)
    skip = (page - 1) * pageSize
    cursor = (
        coll.find(query)
        .sort(sort_field, sort_direction)
        .skip(skip)
        .limit(pageSize)
    )
    items = [as_issue_out(doc) async for doc in cursor]
    total_pages = (total + pageSize - 1) // pageSize

    return PaginatedIssues(
        items=items,
        page=page,
        pageSize=pageSize,
        total=total,
        totalPages=total_pages,
    )

@app.get("/issues/{issue_id}", response_model=IssueOut)
async def get_issue(issue_id: str):
    db = get_db()
    coll = db["issues"]
    try:
        oid = ObjectId(issue_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid issue id")
    doc = await coll.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Issue not found")
    return as_issue_out(doc)

@app.post("/issues", response_model=IssueOut, status_code=201)
async def create_issue(payload: IssueCreate):
    db = get_db()
    coll = db["issues"]
    now = datetime.utcnow()
    doc = {
        "title": payload.title,
        "status": payload.status,
        "priority": payload.priority,
        "assignee": payload.assignee,
        "description": payload.description,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await coll.insert_one(doc)
    doc["_id"] = result.inserted_id
    return as_issue_out(doc)

@app.put("/issues/{issue_id}", response_model=IssueOut)
async def update_issue(issue_id: str, payload: IssueUpdate):
    db = get_db()
    coll = db["issues"]
    try:
        oid = ObjectId(issue_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid issue id")

    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    update_data["updatedAt"] = datetime.utcnow()

    result = await coll.find_one_and_update(
        {"_id": oid},
        {"$set": update_data},
        return_document=True,  # type: ignore
    )
    if not result:
        raise HTTPException(status_code=404, detail="Issue not found")
    return as_issue_out(result)
