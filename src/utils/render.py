from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('tennis_match_scoreboard', 'src/views/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class Render:
    def render_template(self, template_html: str, context: dict) -> str:
        template = env.get_template(template_html)
        return template.render(context)
