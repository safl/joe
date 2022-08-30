import pytest

import cijoe.linux.kmemleak as kmemleak


def skip_config(cijoe):
    """Skip testing when configuration is missing or module not enabled"""

    kmemleak = cijoe.config.options.get("kmemleak", None)
    if not kmemleak:
        pytest.skip("missing: config['kmemleak'] configuration")

    enabled = kmemleak.get("enabled", False)
    if not enabled:
        pytest.skip("kmemleak is disabled: !config['kmemleak']['enabled']")


def test_clear(cijoe):
    skip_config(cijoe)

    rcode, state = kmemleak.clear(cijoe)
    assert not rcode, "Failed clearing kmemleak"


def test_scan(cijoe):
    skip_config(cijoe)

    rcode, state = kmemleak.scan(cijoe)
    assert not rcode, "Failed scanning kmemleak"


def test_cat(cijoe):
    skip_config(cijoe)

    rcode, state = kmemleak.cat(cijoe)
    assert not rcode, "Failed cat'ing kmemleak"
