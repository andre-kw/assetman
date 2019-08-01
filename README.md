# assetman

### Installation
- Copy .env.example to .env
- Create Python virtual environment: `python -m venv .venv`
- Enter virtual environment: `source venv/bin/activate` (MacOS/Linux)
- Install [pipenv](https://pipenv.readthedocs.io/en/latest)
- Install dependencies: `pipenv install`
- Run: `flask run`
- To exit environment, run: `deactivate`

### Endpoints
`GET /furnidata?action=<action>`

Perform an action on the server's `furnidata.xml`.

|`<action>`| Effect |
|--|--|
| `save` | Outputs the working copy to a new `furnidata.xml` |
| `download` | Fetch a copy of Habbo's `furnidata.xml` |
| `copy` | Replace created `furnidata.xml` with Habbo's |
| `search` | *(GET params: key, val)* Search furnitypes by `key` and `val` |


`GET,POST,PATCH,DELETE /furnidata/room/furnitype/<id>`
`GET,POST,PATCH,DELETE /furnidata/wall/furnitype/<id>`

Interact with room/wall furnitypes in a RESTful manner.

