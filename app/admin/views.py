from db.models import Link, Task
from sqladmin import ModelView


class TaskAdmin(ModelView, model=Task):
    name = "Задача"
    name_plural = "Задачи"
    icon = "fa-solid fa-gear"
    column_list = [
        Task.task_id,
        Task.created_at,
        Task.name,
    ]
    form_columns = [
        Task.name,
    ]


class LinkAdmin(ModelView, model=Link):
    name = "Ссылка"
    name_plural = "Ссылки"
    icon = "fa-solid fa-link"
    column_list = [
        Link.link_id,
        Link.created_at,
        Link.url,
        Link.status,
        Link.title,
        Link.redirect_urls,
        Link.referer,
        Link.task_id,
        Link.task,
    ]
    form_columns = [
        Link.url,
        Link.status,
        Link.title,
        Link.redirect_urls,
        Link.referer,
        Link.task,
    ]
