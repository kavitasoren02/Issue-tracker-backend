from __future__ import annotations
from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

Status = Literal["open", "in-progress", "resolved", "closed"]
Priority = Literal["low", "medium", "high", "critical"]

class IssueBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: Status = "open"
    priority: Priority = "medium"
    assignee: Optional[str] = None
    description: Optional[str] = None

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    assignee: Optional[str] = None
    description: Optional[str] = None

class IssueOut(IssueBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

class PaginatedIssues(BaseModel):
    items: list[IssueOut]
    page: int
    pageSize: int
    total: int
    totalPages: int
