from backend.models import Template, Segment, Attachment, Role, Subsystem, Folder, Task


class WriteTemplate:
    def __init__(self, name: str):
        self.name = name
        self.template: Template | None = None


class WriteSegment:
    def __init__(self, name: str):
        self.name = name
        self.attachments: dict[str: WriteAttachment] = {}
        self.segment: Segment | None = None


class WriteAttachment:
    def __init__(self, name: str):
        self.name = name
        self.roles: dict[str: WriteRole] = {}
        self.attachment: Attachment | None = None


class WriteRole:
    def __init__(self, name: str):
        self.name = name
        self.templates: set[str] = set()
        self.role: Role | None = None


class WriteSubsystem:
    def __init__(self, name: str):
        self.name = name
        self.folders: dict[str: WriteFolder] = {}
        self.subsystem: Subsystem | None = None


class WriteFolder:
    def __init__(self, name: str):
        self.name = name
        self.tasks: dict[str: WriteTask] = {}
        self.folder: Folder | None = None


class WriteTask:
    def __init__(self, name: str):
        self.name = name
        self.roles: set[str] = set()
        self.task: Task | None = None
