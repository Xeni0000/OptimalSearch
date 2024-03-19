import re

from backend.models import Template, Segment, Attachment, Role, Subsystem, Folder, Task
from backend.serv.common import WriteTemplate, WriteSegment, WriteAttachment, WriteRole, WriteSubsystem, WriteFolder, \
    WriteTask


class WriteOnDBServ:
    @staticmethod
    async def write_templates(templates: list) -> dict[str: WriteTemplate]:
        """Функция для записи шаблонов в бд. Возвращает словарь с созданными шаблонами"""

        templates_dict: dict[str: WriteTemplate] = {}

        # Записываем шаблоны в БД и словарь
        for row in templates:
            name: str = row[0]
            templates_dict[name] = WriteTemplate(name)
            templates_dict[name].template = await Template.objects.acreate(name=name)

        return templates_dict

    @staticmethod
    async def write_segments(segments: list) -> tuple[dict[str: WriteSegment], dict[str: WriteRole]]:
        """Функция для записи базовых зависимостей ролей в БД. Возвращает кортеж с двумя словарями: представление
        ролей в 'Неуверен как это написать правильно, имею в виду, что здесь записаны сперва сегменты, потом приложения
         и потом роли.' и полный список созданных ролей"""

        last_segment: Segment
        last_attachment: Attachment
        last_role: Role

        segments_dict: dict[str: WriteSegment] = {}
        roles: dict[str: WriteRole] = {}

        # Проходимся циклом по полученным данным и, на основании выполняемых условий, записываем в БД сегменты,
        # приложения и шаблоны.
        for row in segments:
            is_segment = row[0] is not None and row[0] != '' and row[0] != 'Сегмент'
            is_attachment = row[1] is not None and row[1] != '' and row[1] != 'Приложение'
            is_role = row[2] is not None and row[2] != '' and row[2] != 'Роль'

            if is_segment:
                name: str = row[0]
                segments_dict[name] = WriteSegment(name)
                last_segment = await Segment.objects.acreate(name=name)
                segments_dict[name].segment = last_segment
                continue

            if is_attachment:
                name: str = row[1]
                segments_dict[last_segment.name].attachments[name] = WriteAttachment(name)
                last_attachment = await Attachment.objects.acreate(segment_id=last_segment.id, name=name)
                segments_dict[last_segment.name].attachments[name].attachment = last_attachment
                continue

            if is_role:
                name: str = row[2]
                role = WriteRole(name)
                segments_dict[last_segment.name].attachments[last_attachment.name].roles[name] = role
                last_role = await Role.objects.acreate(attachment_id=last_attachment.id, name=name)
                segments_dict[last_segment.name].attachments[last_attachment.name].roles[name].role = last_role
                roles[name] = role
                continue

        return segments_dict, roles

    @staticmethod
    async def write_subsystems(subsystems: list, templates: dict[str: WriteTemplate], roles: dict[str: WriteRole]) \
            -> tuple[dict[str: WriteSubsystem], dict[str: WriteTemplate], dict[str: WriteRole]]:
        """Функция для записи базовых зависимостей задач в БД, а так же для построения зависимостей между ролями,
         задачами и шаблонами. Возвращает кортеж с тремя словарями: представление
        задач в 'Тоже что и в функции выше, та же фигня ((', а так же дополненные списки ролей и шаблонов"""

        last_subsystem: Subsystem
        last_folder: Folder
        last_task: Task
        last_role_name: str

        subsystems_dict: dict[str: WriteSubsystem] = {}
        tasks: dict[str: WriteTask] = {}

        # Проходимся циклом по полученным данным и, на основании выполняемых условий, записываем в БД подсистемы,
        # папки и задачи. Для каждой из ролей указываем зависимые задачи
        for row in subsystems:
            is_subsystem = row[0] is not None and row[0] != '' and row[0] != 'Подсистема'
            is_folder = row[1] is not None and row[1] != '' and row[1] != 'Папка'
            is_task = row[2] is not None and row[2] != '' and row[2] != 'Задача'
            is_role = row[3] is not None and row[3] != '' and row[3] != 'Роль' and row[3] != 'Тип'
            is_template = row[4] is not None and row[4] != '' and row[4] != 'Шаблон' \
                          and row[4] != 'Куратор' and row[4] != 'Категории'

            if is_subsystem:
                name: str = row[0]
                subsystems_dict[name] = WriteSubsystem(name)
                last_subsystem = await Subsystem.objects.acreate(name=name)
                subsystems_dict[name].subsystem = last_subsystem
                continue

            if is_folder:
                name: str = row[1]
                subsystems_dict[last_subsystem.name].folders[name] = WriteFolder(name)
                last_folder = await Folder.objects.acreate(subsystem_id=last_subsystem.id, name=name)
                subsystems_dict[last_subsystem.name].folders[name].folder = last_folder
                continue

            if is_task:
                name: str = row[2]
                task = WriteTask(name)
                subsystems_dict[last_subsystem.name].folders[last_folder.name].tasks[name] = task
                last_task = await Task.objects.acreate(folder_id=last_folder.id, name=name)
                subsystems_dict[last_subsystem.name].folders[last_folder.name].tasks[name].task = last_task
                tasks[name] = task
                continue

            if is_role:
                name: str = row[3].split(' [')[0]
                subsystems_dict[last_subsystem.name].folders[last_folder.name].tasks[last_task.name].roles.add(name)

                last_role_name: str = name
                if name not in roles:
                    roles[name] = WriteRole(name)

                continue

            if is_template:
                name: str = row[4]
                roles[last_role_name].templates.add(name)

                if name not in templates:
                    templates[name] = WriteTemplate(name)
                    templates[name].template = await Template.objects.acreate(name=name)
                    continue

        return subsystems_dict, templates, roles

    @staticmethod
    async def write_attachments(attachments: list, templates: dict[str: WriteTemplate], roles: dict[str: WriteTemplate],
                                subsystems: dict[str: WriteSubsystem], segments: dict[str: WriteSegment]) \
            -> tuple[
                dict[str: WriteTemplate], dict[str: WriteTemplate], dict[str: WriteSubsystem], dict[str: WriteTask]]:
        """Финальная функция для построения зависимостей между моделями БД. Возвращает дополненные списки необходимых
         данных"""

        last_attachment: WriteAttachment
        last_role_name: str
        last_subsystem: WriteSubsystem
        last_folder: WriteFolder

        # Проходимся циклом по полученным данным и, на основании выполняемых условий, записываем данные в БД
        # и дополняем зависимости
        for row in attachments:
            is_attachment = row[0] is not None
            is_role = row[2] is not None
            is_template = row[5] is not None
            is_subsystem = row[6] is not None
            is_folder = row[7] is not None
            is_tasks = row[8] is not None

            if is_attachment:
                name: str = row[0]
                for s in segments.values():
                    if name in s.attachments:
                        last_attachment = s.attachments[name]
                        break

            if is_role:
                name: str = row[2]
                last_role_name = name

                if name not in roles:
                    roles[name] = WriteRole(name)
                    role_db = await Role.objects.acreate(attachment_id=last_attachment.attachment.id, name=name)
                    roles[name].role = role_db
                elif roles[name].role is None:
                    role_db = await Role.objects.acreate(attachment_id=last_attachment.attachment.id, name=name)
                    roles[name].role = role_db

            if is_template:
                role_templates = re.sub('\n', '', row[5])
                role_templates = re.sub('_x000D_', '', role_templates)
                role_templates = role_templates.split(',')

                for t in role_templates:
                    if t not in templates:
                        templates[t] = WriteTemplate(t)
                        templates[t].template = await Template.objects.acreate(name=t)

                    roles[last_role_name].templates.add(t)

            if is_subsystem:
                name: str = row[6]
                if name not in subsystems:
                    last_subsystem = WriteSubsystem(name)
                    subsystems[name] = last_subsystem
                    subsystems[name].subsystem = await Subsystem.objects.acreate(name=name)
                else:
                    last_subsystem = subsystems[name]

            if is_folder:
                name: str = row[7]
                if name not in last_subsystem.folders:
                    last_folder = WriteFolder(name)
                    last_subsystem.folders[name] = last_folder
                    last_subsystem.folders[name].folder = await Folder.objects.acreate(
                        subsystem_id=last_subsystem.subsystem.id,
                        name=name)
                else:
                    last_folder = last_subsystem.folders[name]

            if is_tasks:
                name = row[8]
                if name not in last_folder.tasks:
                    task = WriteTask(name)
                    last_folder.tasks[name] = task
                    last_folder.tasks[name].task = await Task.objects.acreate(folder_id=last_folder.folder.id,
                                                                              name=name)

                last_folder.tasks[name].roles.add(last_role_name)

        # создаём словарь задач
        tasks: dict[str: WriteTask] = {}
        for s in subsystems.values():
            for f in s.folders.values():
                for k, v in f.tasks.items():
                    tasks[k] = v

        return templates, roles, subsystems, tasks
