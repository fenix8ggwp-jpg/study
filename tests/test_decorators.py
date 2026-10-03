from pathlib import Path

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_success_console(self, capsys: pytest.CaptureFixture) -> None:
        """Успешное выполнение — лог в консоль."""

        @log()
        def add(x: int, y: int) -> int:
            return x + y

        result = add(1, 2)
        captured = capsys.readouterr()
        assert result == 3
        assert "add ok" in captured.out

    def test_log_success_file(self, tmp_path: Path) -> None:
        """Успешное выполнение — лог в файл."""
        log_file = tmp_path / "test.log"

        @log(filename=str(log_file))
        def multiply(x: int, y: int) -> int:
            return x * y

        result = multiply(3, 4)
        assert result == 12
        assert "multiply ok" in log_file.read_text(encoding="utf-8")

    def test_log_error_console(self, capsys: pytest.CaptureFixture) -> None:
        """Ошибка — лог в консоль."""

        @log()
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

        captured = capsys.readouterr()
        assert "divide error" in captured.out
        assert "ZeroDivisionError" in captured.out
        assert "(1, 0)" in captured.out

    def test_log_error_file(self, tmp_path: Path) -> None:
        """Ошибка — лог в файл."""
        log_file = tmp_path / "error.log"

        @log(filename=str(log_file))
        def failing_function(a: int) -> int:
            raise ValueError("test error")

        with pytest.raises(ValueError):
            failing_function(5)

        content = log_file.read_text(encoding="utf-8")
        assert "failing_function error" in content
        assert "ValueError" in content
        assert "(5,)" in content

    def test_log_with_kwargs(self, capsys: pytest.CaptureFixture) -> None:
        """Логирование kwargs при ошибке."""

        @log()
        def func_with_kwargs(a: int, b: int = 0) -> int:
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            func_with_kwargs(1, b=2)

        captured = capsys.readouterr()
        assert "'b': 2" in captured.out

    def test_log_preserves_metadata(self) -> None:
        """functools.wraps сохраняет имя и docstring."""

        @log()
        def my_func() -> None:
            """My docstring."""

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_log_file_append(self, tmp_path: Path) -> None:
        """Логи дописываются в файл, а не перезаписывают."""
        log_file = tmp_path / "append.log"

        @log(filename=str(log_file))
        def func() -> None:
            pass

        func()
        func()

        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2
        assert all("func ok" in line for line in lines)
