from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path

def render_spend_jinja_template(template_name: str, **extra_context) -> str:
    """
    Рендерит Jinja2 шаблон для трат из папки templates и возвращает строку результата.
    """
    templates_dir = Path(__file__).resolve().parents[1] / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_name)

    context = {
        "now": datetime.now(),
        "timedelta": timedelta,
        "relativedelta": relativedelta,
    }
    context.update(extra_context)

    return template.render(**context)