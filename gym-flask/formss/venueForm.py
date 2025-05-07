from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ValidationError,model_validator
from typing import Optional
from enum import Enum

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class ReservationForm(BaseModel):
    venue_id: int = Field(..., gt=0, description="场馆ID必须为正整数")
    user_id: int = Field(..., gt=0, description="用户ID必须为正整数")
    start_time: datetime = Field(..., description="预约开始时间")
    end_time: datetime = Field(..., description="预约结束时间")
    notes: Optional[str] = Field(None, max_length=500, description="备注信息")
    status: ReservationStatus = Field(default=ReservationStatus.PENDING, description="预约状态")

    @field_validator("start_time", "end_time", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("时间格式应为 ISO 格式 (YYYY-MM-DD HH:MM:SS)")
        return value

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError("结束时间必须晚于开始时间")
        if (self.end_time - self.start_time).total_seconds() < 1800:
            raise ValueError("预约时长至少30分钟")
        return self

    @field_validator("status")
    def validate_status(cls, v):
        if v == ReservationStatus.CANCELLED and not cls.notes:
            raise ValueError("取消预约必须填写原因")
        return v
