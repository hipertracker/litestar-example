from pathlib import Path

from jinjax import Catalog
from litestar import get, Litestar
from litestar import post
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.enums import MediaType
from litestar.logging import StructLoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.response import Response, Template
from litestar.template.config import TemplateConfig

logging_config = StructLoggingConfig()

catalog = Catalog()
catalog.add_folder("components")

compression_config = (CompressionConfig(backend="gzip", gzip_compress_level=9),)

cors_config = CORSConfig(allow_origins=["*"])
csrf_config = CSRFConfig(secret="my-secret")


def render(*args, **kwargs) -> Response:
    return Response(content=catalog.render(*args, **kwargs), media_type=MediaType.HTML)


@get(path="/")
async def index() -> Response:
    return render("Welcome", message="Litestar + JinjaX with Tailwind+Flowbite example")


#
@post(path="/test1", exclude_from_csrf=True)
async def test1(request: HTMXRequest) -> Response:
    message = "Feedback from HTMX and JinjaX components"
    return render("Feedback", message=message)


@post(path="/test2", exclude_from_csrf=True)
async def test2(request: HTMXRequest) -> Template:
    message = "Feedback from HTMX and Jinja2 templates"
    return Template(template_name="feedback.jinja2", context={"message": message})


#
app = Litestar(
    route_handlers=[index, test1, test2],
    debug=True,
    csrf_config=csrf_config,
    cors_config=cors_config,
    compression_config=CompressionConfig(backend="gzip", gzip_compress_level=9),
    template_config=TemplateConfig(
        engine=JinjaTemplateEngine,
        directory=Path("templates"),
    ),
    logging_config=logging_config,
    openapi_config=OpenAPIConfig(
        title="My API",
        version="1.0.0",
        root_schema_site="rapidoc",
    ),
)
