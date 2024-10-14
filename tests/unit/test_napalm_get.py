import os

from nornir_napalm.plugins.tasks import napalm_get
from nornir_napalm.plugins.connections import CONNECTION_NAME


THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_get"


def connect(task, extras):
    if CONNECTION_NAME in task.host.connections:
        task.host.close_connection(CONNECTION_NAME)
    task.host.open_connection(
        CONNECTION_NAME,
        task.nornir.config,
        extras={"optional_args": extras},
        default_to_host_attributes=True,
    )


class Test(object):
    def test_napalm_getters(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(napalm_get, getters=["get_facts", "get_interfaces"])
        assert result
        for h, r in result.items():
            assert r.result["get_facts"]
            assert r.result["get_interfaces"]

    def test_napalm_getters_error(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_error"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)

        results = d.run(napalm_get, getters=["get_facts", "get_interfaces"])
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, KeyError)
        assert processed

    def test_napalm_getters_with_options_error(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_single_with_options"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(task=napalm_get, getters=["get_config"], nonexistent="asdsa")
        assert result
        assert result.failed
        for h, r in result.items():
            assert "unexpected keyword argument 'nonexistent'" in r.result

    def test_napalm_getters_with_options_error_optional_args(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_single_with_options"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(
            task=napalm_get,
            getters=["get_config"],
            getters_options={"get_config": {"nonexistent": "asdasd"}},
        )
        assert result
        assert result.failed
        for h, r in result.items():
            assert "unexpected keyword argument 'nonexistent'" in r.result

    def test_napalm_getters_single_with_options(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_single_with_options"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(task=napalm_get, getters=["get_config"], retrieve="candidate")
        assert result
        assert not result.failed
        for h, r in result.items():
            assert r.result["get_config"]

    def test_napalm_getters_multiple_with_options(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_multiple_with_options"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(
            task=napalm_get,
            getters=["get_config", "get_facts"],
            getters_options={"get_config": {"retrieve": "candidate"}},
        )
        assert result
        assert not result.failed
        for h, r in result.items():
            assert r.result["get_config"]
            assert r.result["get_facts"]

    def test_napalm_getters_without_prefix(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_getters_without_prefix"}
        d = nornir.filter(name="dev3.group_2")
        d.run(task=connect, extras=opt)
        result = d.run(napalm_get, getters=["is_alive"])
        assert result
        for h, r in result.items():
            assert r.result["is_alive"]
