from jinja2 import Template

from src.const.path import ASSETS, build_path
from src.utils.generate import generate
from src.utils.network import Request
from src.templates import SimpleHTML, get_saohua
from src.config import Config
from ._template import template_role_monsters

async def get_role_monsters_map(server: str, role_name: str):
    role_monster_data = (await Request(f"{Config.jx3.api.url}/data/role/monster?server={server}&name={role_name}&token={Config.jx3.api.token}").get()).json()
    data = role_monster_data["data"]
    content = []
    for i in range(len(data["skillList"])):
        skill = data["skillList"][i]
        icon = f'https://icon.jx3box.com/icon/{skill["dwOutSkillID"]}.png'
        print(icon)
        new = Template(template_role_monsters).render(
            icon = icon,
            level = str(skill["nLevel"]),
            name = skill["szSkillName"]
        )
        content.append(new)
    html = str(
        SimpleHTML(
            "jx3",
            "role_monster.html",
            font = build_path(ASSETS, ["font", "PingFangSC-Medium.otf"]),
            table_content = "\n".join(content),
            gameEnergy = data["gameEnergy"],
            gameStamina = data["gameStamina"],
            server = data["serverName"],
            name = data["roleName"],
            msg = get_saohua()
        )
    )
    image = await generate(html, ".m-bmap.is-map-phone")
    return image