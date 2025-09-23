from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    name: str = Field(..., description="三个点是必填的标记")
    age: int = Field(default=20, gt=0, le=150, description="default设置默认值，大于0小于等于150")
    sex: bool = False  # 可以不用Field，直接设置默认值，偷懒写法
    zip_code: str = Field(default="10000", pattern=r"^\d{5}$", description="正则验证，五位数字邮编")


class Demo4Params(BaseModel):
    user: User
    other: str = '其他参数'


class UserOut(BaseModel):
    # 没有定义的属性不会返回
    age: int
    sex: bool

    model_config = ConfigDict(from_attributes=True)  # 该行用于配合 model_validate()
