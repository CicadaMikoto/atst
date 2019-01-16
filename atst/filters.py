import re
import datetime
from atst.utils.localization import translate
from atst.forms.data import translate_duration
from flask import current_app as app, render_template
from jinja2 import contextfilter
from jinja2.exceptions import TemplateNotFound


def iconSvg(name):
    with open("static/icons/" + name + ".svg") as contents:
        return contents.read()


def dollars(value):
    try:
        numberValue = float(value)
    except ValueError:
        numberValue = 0
    return "${:,.0f}".format(numberValue)


def usPhone(number):
    phone = re.sub(r"\D", "", number)
    return "+1 ({}) {} - {}".format(phone[0:3], phone[3:6], phone[6:])


def readableInteger(value):
    try:
        numberValue = int(value)
    except ValueError:
        numberValue = 0
    return "{:,}".format(numberValue)


def getOptionLabel(value, options):
    if hasattr(value, "value"):
        value = value.name
    try:
        return next(tup[1] for tup in options if tup[0] == value)  # pragma: no branch
    except StopIteration:
        return


def mixedContentToJson(value):
    """
    This coerces the file upload in form data to its filename
    so that the data can be JSON serialized.
    """
    if (
        isinstance(value, dict)
        and "legacy_task_order" in value
        and hasattr(value["legacy_task_order"]["pdf"], "filename")
    ):
        value["legacy_task_order"]["pdf"] = value["legacy_task_order"]["pdf"].filename
    return app.jinja_env.filters["tojson"](value)


def findFilter(value, filter_name, filter_args=[]):
    if not filter_name:
        return value
    elif filter_name in app.jinja_env.filters:
        return app.jinja_env.filters[filter_name](value, *filter_args)
    else:
        raise ValueError("filter name {} not found".format(filter_name))


def renderList(value):
    return app.jinja_env.filters["safe"]("<br>".join(value))


def formattedDate(value, formatter="%m/%d/%Y"):
    if value:
        return value.strftime(formatter)
    else:
        return "-"


def dateFromString(value, formatter="%m/%Y"):
    return datetime.datetime.strptime(value, formatter)


def pageWindow(pagination, size=2):
    page = pagination.page
    num_pages = pagination.pages

    over = max(0, page + size - num_pages)
    under = min(0, page - size - 1)

    return (max(1, (page - size) - over), min(num_pages, (page + size) - under))


def renderAuditEvent(event):
    template_name = "audit_log/events/{}.html".format(event.resource_type)
    try:
        return render_template(template_name, event=event)
    except TemplateNotFound:
        return render_template("audit_log/events/default.html", event=event)


def removeHtml(text):
    html_tags = re.compile("<.*?>")
    return re.sub(html_tags, "", text)


def normalizeOrder(title):
    # reorders titles from "Army, Department of the" to "Department of the Army"
    text = title.split(", ")
    reordered_text = text[0:-1]
    reordered_text.insert(0, text[-1])
    return " ".join(reordered_text)


def register_filters(app):
    app.jinja_env.filters["iconSvg"] = iconSvg
    app.jinja_env.filters["dollars"] = dollars
    app.jinja_env.filters["usPhone"] = usPhone
    app.jinja_env.filters["readableInteger"] = readableInteger
    app.jinja_env.filters["getOptionLabel"] = getOptionLabel
    app.jinja_env.filters["mixedContentToJson"] = mixedContentToJson
    app.jinja_env.filters["findFilter"] = findFilter
    app.jinja_env.filters["renderList"] = renderList
    app.jinja_env.filters["formattedDate"] = formattedDate
    app.jinja_env.filters["dateFromString"] = dateFromString
    app.jinja_env.filters["pageWindow"] = pageWindow
    app.jinja_env.filters["renderAuditEvent"] = renderAuditEvent
    app.jinja_env.filters["removeHtml"] = removeHtml
    app.jinja_env.filters["normalizeOrder"] = normalizeOrder
    app.jinja_env.filters["translateDuration"] = translate_duration

    @contextfilter
    def translateWithoutCache(context, *kwargs):
        return translate(*kwargs)

    if app.config["DEBUG"]:
        app.jinja_env.filters["translate"] = translateWithoutCache
    else:
        app.jinja_env.filters["translate"] = translate
