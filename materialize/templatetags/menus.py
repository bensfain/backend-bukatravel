from django import template
from django.utils.safestring import mark_safe

from materialize.views import admin_menus

register = template.Library()


@register.simple_tag
def get_menus(user=None, path=None):
    menus = ""
    menu_list = admin_menus(user)
    for item in menu_list:
        if item.get("header", None):
            menus += f"""
                <li class="menu-header fw-light mt-4">
                    <span class="menu-header-text">{item["title"]}</span>
                </li>
                """
        else:
            children = item.get("children", None)
            if children:
                is_active = False
                for child in item["children"]:
                    if child.get("url", "#") == path:
                        is_active = True

                menus += f"""
                    <li class="menu-item {"active open" if is_active else ""}">
                        <a href="javascript:void(0);" class="menu-link menu-toggle">
                            <i class="menu-icon tf-icons mdi mdi-form-select"></i>
                            <div>{item["title"]}</div>
                        </a>
                        <ul class="menu-sub">
                    """
                for child in item["children"]:
                    is_active_child = child["url"] == path
                    menus += f"""
                    <li class="menu-item {"active" if is_active_child else ""}">
                        <a href="{child.get("url", "#")}" class="menu-link">
                            <div>{child.get("title", "")}</div>
                        </a>
                    </li>
                    """
                menus += """
                    </ul>
                </li>
                """
            else:
                is_active = item["url"] == path
                menus += f"""
                    <li class="menu-item {"active" if is_active else ""}">
                        <a href="{item["url"]}" class="menu-link">
                            <i class="menu-icon tf-icons {item["icon"]}"></i>
                            <div data-i18n="{item["title"]}">{item["title"]}</div>
                        </a>
                    </li>
                    """
    return mark_safe(menus)
