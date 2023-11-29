from datetime import datetime
from functools import wraps
import logging
from time import sleep
from opensearchpy import OpenSearch
import types

# mute elastic
logging.getLogger("opensearchpy").setLevel(logging.WARNING)

__all__ = ["TasksMonitoring", "payload_to_tasks"]


class TasksMonitoring(list):
    def __init__(self):
        super().__init__()
        self.all_completed = True
        self.es_conn = None
        self.logger = logging.getLogger("TASKS_MONITORING")

    def set_connection(self, es_conn: OpenSearch):
        self.es_conn = es_conn

    def append(self, el):
        super().append({**el, "start_at": datetime.now(), "is_completed": False})
        self.all_completed = False

    def iter_over_not_completed(self):
        for task in super().__iter__():
            if not task["is_completed"]:
                yield task

    def check_task_status(self, task):
        res = self.es_conn.tasks.get(task["id"])
        task["is_completed"] = res["completed"]

        total = res["task"]["status"]["total"]
        updated = res["task"]["status"]["updated"]
        created = res["task"]["status"]["created"]
        deleted = res["task"]["status"]["deleted"]

        total_impacted = updated + created + deleted

        now = datetime.now()
        duration = now - task["start_at"]
        if not res["completed"]:
            self.logger.info(
                "[%s][PENDING] - %s - %s / %s",
                task["id"],
                task["name"],
                total_impacted,
                total,
            )
            return False

        no_error = True
        response_check = total == total_impacted
        if not response_check:
            no_error = False
            self.logger.error(
                "[%s][COMPLETED] - %s - Error - %s != c %s +  u %s + d %s",
                task["id"],
                task["name"],
                total,
                created,
                updated,
                deleted,
            )

        if "error" in res:
            no_error = False
            self.logger.error(
                "[%s][COMPLETED] - %s - Error - %s",
                task["id"],
                task["name"],
                res["error"],
            )

        if "response" in res and res["response"]["failures"]:
            no_error = False

            self.logger.error(
                "[%s][COMPLETED] - %s - Error - %s",
                task["id"],
                task["name"],
                res["response"]["failures"],
            )
            # TODO if res status == 409 retry the task

        if no_error:
            self.logger.info(
                "[%s][COMPLETED] - %s - %s = c %s + u %s + d %s - %s s",
                task["id"],
                task["name"],
                total,
                created,
                updated,
                deleted,
                duration,
            )

        return True

    def pull_not_completed(self):
        all_completed = True

        for task in self.iter_over_not_completed():
            all_completed &= self.check_task_status(task)

        self.all_completed = all_completed

        return all_completed

    def monitor(self, pulling_time=15):
        while not self.all_completed:
            if self.pull_not_completed():
                break
            sleep(pulling_time)

    def finish(self):
        for tasks in super().__iter__():
            if "on_finish" in tasks:
                self.logger.info(tasks["on_finish"])


def parametrized(decorator):
    def layer(*args, **kwargs):
        def repl(func):
            return decorator(func, *args, **kwargs)

        return repl

    return layer


@parametrized
def payload_to_tasks(func, indexes, operation="update_by_query"):
    """A decorator

    Args:
        func (function): the func wrapped
    """

    @wraps(func)
    def wrapper(*args, **kwds):
        instance_class = args[0]
        instance_class.logger.debug("[%s]%s[START]", func.__name__, indexes)
        result_func = func(*args, **kwds)

        is_generator = isinstance(result_func, types.GeneratorType)
        dict_payloads = []
        if not is_generator:
            result_func = [result_func]

        for dict_payload in result_func:
            payload_without_script = dict_payload.copy()

            if "script" in dict_payload:
                del payload_without_script["script"]

            count = instance_class.es_conn.count(
                index=indexes, body=payload_without_script
            )["count"]
            if count:
                instance_class.logger.debug(
                    "[%s]%s[COUNT] - %s", func.__name__, indexes, count
                )

                operation_task = getattr(instance_class.es_conn, operation)(
                    index=indexes,
                    body=dict_payload,
                    params={
                        "timeout": instance_class.args.es_timeout,
                        "wait_for_completion": "false",
                    },
                )

                instance_class.tasks.append(
                    {
                        "id": operation_task["task"],
                        "name": f"{operation} {func.__name__}",
                        "count": count,
                    }
                )

                instance_class.logger.debug(
                    "[%s]%s[TASKS] - %s", func.__name__, indexes, operation_task
                )

            else:
                instance_class.logger.info(
                    "[%s][COMPLETED] - No data impact by this payload", func.__name__
                )

            dict_payloads.append(dict_payload)
            instance_class.tasks.monitor(5)

        instance_class.logger.debug("[%s]%s[END]", func.__name__, indexes)
        if not is_generator:
            return dict_payloads[0]
        return dict_payloads

    return wrapper
