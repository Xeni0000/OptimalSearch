from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from backend.common.arch.forms import WriteToDBForm
from backend.common.decorators import require_POST
from backend.common.http import ErrorResponse, SuccessResponse
from backend.models import Subsystem, Folder, Task, Segment, Attachment, Role, Template
from backend.serv.WriteOnDBServ import WriteOnDBServ


@require_POST
async def write_on_db(request):
    form = WriteToDBForm.from_POST(request)

    try:
        subsystems_wb = load_workbook(form.path_to_tasks)
    except InvalidFileException as ex:
        return ErrorResponse({'path_to_tasks': str(ex)})
    except FileNotFoundError as ex:
        return ErrorResponse({'path_to_tasks': str(ex)})

    try:
        templates_wb = load_workbook(form.path_to_templates)
    except InvalidFileException as ex:
        return ErrorResponse({'path_to_templates': str(ex)})
    except FileNotFoundError as ex:
        return ErrorResponse({'path_to_templates': str(ex)})

    try:
        roles_wb = load_workbook(form.path_to_roles)
    except InvalidFileException as ex:
        return ErrorResponse({'path_to_roles': str(ex)})
    except FileNotFoundError as ex:
        return ErrorResponse({'path_to_roles': str(ex)})

    try:
        segments_wb = load_workbook(form.path_to_roles_list_wb)
    except InvalidFileException as ex:
        return ErrorResponse({'path_to_roles_list_wb': str(ex)})
    except FileNotFoundError as ex:
        return ErrorResponse({'path_to_roles_list_wb': str(ex)})

    # region Templates

    templates_ws = templates_wb.active
    templates_list = [t for t in templates_ws.values]
    templates = await WriteOnDBServ.write_templates(templates_list[1:])

    # endregion

    # region Segments

    segments_ws = segments_wb.active
    segments_list = segments_ws.values
    segments, roles = await WriteOnDBServ.write_segments(segments_list)

    # endregion

    # region Tasks
    subsystems_ws = subsystems_wb.active
    subsystems_list = subsystems_ws.values
    subsystems, templates, roles = await WriteOnDBServ.write_subsystems(subsystems_list, templates, roles)

    # endregion

    # region Roles

    roles_ws = roles_wb.active
    roles_list = [r for r in roles_ws.values]
    templates, roles, subsystems, tasks = await WriteOnDBServ.write_attachments(roles_list[1:], templates, roles,
                                                                                subsystems, segments)

    # endregion
    not_added_roles: list[str] = []
    not_added_tasks: list[str] = []

    for r in roles.values():
        r_templates = [v.template for k, v in templates.items() if k in r.templates]

        if not r.role:
            not_added_roles.append(r.name)
            continue

        await r.role.templates.aadd(*r_templates)

    for t in tasks.values():
        t_roles = [v.role for k, v in roles.items() if k in t.roles]

        if not t.task:
            not_added_tasks.append(t.name)
            continue

        await t.task.roles.aadd(*t_roles)

    return SuccessResponse({
        'not_added_roles': not_added_roles,
        'not_added_tasks': not_added_tasks,
    })
