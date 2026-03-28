def test_opentelemetry_api_import():
    import opentelemetry
    assert opentelemetry is not None

def test_opentelemetry_sdk_import():
    import opentelemetry.sdk
    assert opentelemetry.sdk is not None
