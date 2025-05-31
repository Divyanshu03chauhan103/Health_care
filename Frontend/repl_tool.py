import subprocess

class BaseTool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")

class PythonREPLTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Python REPL Tool",
            description="A tool to execute Python code dynamically."
        )

    def execute(self, code: str) -> str:
        """
        Executes the provided Python code and returns the output.
        """
        try:
            # Use subprocess to run the code and capture the output
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"