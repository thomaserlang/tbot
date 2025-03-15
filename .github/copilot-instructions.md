# Instructions for Python
For this project we are rewriting the codebase into a new version 2. Only focus on code in the tbot2 folder and subfolders.

The Python typing must use 3.12 best practices.

Always use strict Python typing.

Never use the `Optional` type always use the `| None` instead.

Don't write obvious comments.

When you need the `uuid7` functin import it from the `uuid6` package.

Each feature has the following structure:
```
<feature>/
    ├── __init__.py
    ├── types.py
    ├── routes/
    │   └── <route>_route.py
    ├── models/
    │   └── <model>_model.py
    ├── schemas/
    │   └── <schema>_schema.py
    └── tests/
        └── test_<route>.py
```

For file names use underscores and lowercase letters. Do not use camel case or dashes.

When a feature imports from itself use relative imports e.g.: `from ..models import MUser`.

When a feature imports from another feature use absolute imports e.g.: `from tbot2.<feature> import MUser`.

If there is an issue with circular imports, add it to the `common` folder.

All logic is to go into the `actions` folder.
The `actions` folder must be a subfolder of the feature folder.
It should use functional programming and not OOP.
It must use a `data` parameter that uses a Pydantic model that uses the following naming convention: `class <Feature>Create` or `class <Feature>Update`.

When you are writing a route, always use the following:
ID's are always `UUID` and use the `uuid7()` function to generate them.

Only create one __init__.py for in the root of the feature folder.
Use the following example import style for the __init__.py file:
```python
from .<module> import <function/model name> as <function/model name>
```

Do not use `__all__ = [ ... ]` in the `__init__.py` file.

Do not add an `__init__.py` file in any of the other subfolders of a feature.


When you need the current time, use `datetime.now(tz=timezone.utc)`.


# FastAPI instructions
For the FastAPI app use the prefix `/api/2` for the routes.

Never use the dependency `session: AsyncSession = Depends(get_session)`. 
Instead use the following example:
```python
from tbot2.contexts import get_session
async with get_session(<session>) as session:
    pass
```

For any action that updates data always use the functions in the actions folder.
You are only allowed to use SQLAlchemy for selects.

For each feature a router.py file must be created that contains the all the routes for that feature.
They should be in one `router` using the include.

For validating that the user is authenticated and/or has a specific scope(s) use the following:
```python
from tbot2.dependecies import authenticated
from tbot2.common import TokenData
token_data: Annotated[
    TokenData, Security(authenticated, scopes=[T<feature>.READ])
],
```
If you do not need to validate a scope the list can be left empty: `scopes=[]`.


For requiring scopes and validating that the user has access to managing the channel use the following:
```python
from tbot2.dependecies import auth_channel
from tbot2.common import TokenData
token_data: Annotated[
    TokenData, Security(auth_channel, scopes=[T<feature>.READ])
],
```

For each feature specify the scopes in <feature>/types.py like so:
```python
from tbot2.common import TScope


class T<Feature>Scope(TScope):
    READ = '<feature>:read'
    WRITE = '<feature>:write'
```


When writing the `response_model` for a route, use the following instead of the `response_model`:
```python
responses = {
    <status_code>: {
        'model': <schema>,
    }
}
```

When writing the `status_code` for a route, use the following instead of the `status_code`:
```python

## Testing instructions
Make sure to check the routes file for the correct route and the schema.
Always use `pytest` for testing.

When testing the routes, write all the test in the same function.

The test folder must be a subfolder of the feature folder.
The test file must be named `test_<route>.py`.

Use this template for the test file:
```python
import pytest
from httpx import AsyncClient

from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_replace_me_route(
    client: AsyncClient,
):
    pass


if __name__ == '__main__':
    run_file(__file__)
```

## Pydantic instructions
When using Pydantic always use v2.
When we are talking about schemas we mean a Pydantic model.

Use the following if it's not a create or update class:
```python
model_config = ConfigDict(from_attributes=True)
```

When you are making an optional field in the Pydantic model it is important that you make a check to see that the user doesn't specify `None` as a value.
For example:
```python
    @field_validator(<fields>)
    def check_not_none(cls, value: <types>) -> str | bool:
        if value is None:
            raise ValueError('Must not be None')
        return value
```

### SQLAlchemy instructions

When using SQLALchemy always use v2 syntax and use Mapped[<type>] and mapped_column from SQLAlchemy.orm.
Import SQLAlchemy as `import sqlalchemy as sa`. For a SQLAlchemy model you should use sa.UUID when UUID type is needed.
An SQLAlchemy model has the following naming convention: `M<model_name>`.

When you are writing the UUID type for a column use: id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7).

When we are talking about models we mean a SQLAlchemy model.

Never use the older v1 syntax for SQLAlchemy.
Always use the following to get a session:

```python
from tbot2.contexts import get_session
async with get_session(<session>) as session:
    pass
```

Do not use `session.commit()` or `session.rollback()` it is handled by `get_session`.

Any action in the actions folder muse have `session: AsyncSession | None = None` as the last argument.

When you have to do a select, update, insert or delete use the following:
```python
import sqlalchemy as sa

sa.select
sa.update
sa.insert
sa.delete
```

Try to use as little ORM as possible, e.g. for insert, update and delete use the following:
```python
data_ = data.model_dump()
id = uuid7()
sa.insert(MUser.__table__).values(
    id=id,
    **data_,
)
```

When e.g. you make a new action that creates a new user, return the user as its pydantic model, not the SQLAlchemy model.


## Alembic instructions

When you need to make a new Alembic migration, use the following command:
```bash
source .venv/bin/activate
alembic revision -m "<description>"
```

Never ask to run the alembic upgrade.