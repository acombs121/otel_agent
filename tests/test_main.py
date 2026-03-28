from otel_agent.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from otel-agent!" in captured.out