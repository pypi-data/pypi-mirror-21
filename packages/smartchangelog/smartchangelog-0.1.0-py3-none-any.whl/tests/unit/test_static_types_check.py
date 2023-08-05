import inspect

from smartchangelog import commitmsg
from mypy import api

from smartchangelog import changelog


def test_static_type_check_with_mypy():
    commitmsg_file = inspect.getfile(commitmsg)
    changelog_file = inspect.getfile(changelog)
    params = ['--ignore-missing-imports', commitmsg_file, changelog_file]
    result = api.run(params)
    if result[0]:
        # FIXME: begin: There are bugs in mypy
        #   * support iteration on enums see https://github.com/python/mypy/issues/2305
        #   * support NamedTuple
        # So, we have to remove irrelevant errors
        check_type_errors = "\n".join(
            (error for error in result[0].strip().split("\n") if error.split("error: ")[1] not in (
                '"CommitType" expects no type arguments, but 1 given',
                'Invalid type "commit_type_str"',
                'Iterable expected',
                '"CommitType" has no attribute "__iter__"',
                'Right hand side values are not supported in NamedTuple',
                'Invalid statement in NamedTuple definition; expected "field_name: field_type"'
            )))
        # FIXME: end
        if len(check_type_errors) > 0:
            raise (Exception(check_type_errors))
    if result[1]:
        raise (Exception(result[1]))
