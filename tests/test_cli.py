#!/usr/bin/env python3
"""
Test CLI commands and functionality.
"""

import subprocess
import tempfile
import os
import json
import sys

# Add the cli directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_cli_command(cmd_args, cwd=None):
    """Run a CLI command and return result."""
    if cwd is None:
        cwd = os.path.join(os.path.dirname(__file__), '..')
    
    cmd = [sys.executable, "-m", "cli.prompt"] + cmd_args
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


class TestCLICommands:
    """Test CLI command functionality."""
    
    def setup_method(self):
        """Set up test environment with custom config."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create test config
        test_config = {
            "selected_model": None,
            "gpt-4o": None,
            "claude-3-5-sonnet": None,
            "gemini-1.5-flash": "test-key"
        }
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)
    
    def test_setup_command(self):
        """Test --setup command."""
        returncode, stdout, stderr = run_cli_command(["--setup"])
        assert returncode == 0
        assert "Config file created" in stdout
    
    def test_models_command(self):
        """Test models command."""
        returncode, stdout, stderr = run_cli_command(["models"])
        assert returncode == 0
        assert "OPENAI" in stdout
        assert "ANTHROPIC" in stdout
        assert "GOOGLE" in stdout
        assert "gpt-4o" in stdout
        assert "claude-3-5-sonnet" in stdout
        assert "gemini-1.5-flash" in stdout
    
    def test_list_command(self):
        """Test list command."""
        returncode, stdout, stderr = run_cli_command(["list"])
        assert returncode == 0
        assert "Configured models" in stdout
    
    def test_config_command_valid_model(self):
        """Test config command with valid model."""
        returncode, stdout, stderr = run_cli_command(["config", "gpt-4o", "test-api-key"])
        assert returncode == 0
        assert "configured successfully" in stdout
    
    def test_select_command_valid_model(self):
        """Test select command with valid configured model."""
        # First configure a model
        run_cli_command(["config", "gpt-4o", "test-key"])
        
        # Then select it
        returncode, stdout, stderr = run_cli_command(["select", "gpt-4o"])
        assert returncode == 0
        assert "Selected model" in stdout
    
    def test_help_command(self):
        """Test help functionality."""
        returncode, stdout, stderr = run_cli_command(["--help"])
        assert returncode == 0
        assert "Multi-model CLI" in stdout
        assert "chat" in stdout
        assert "config" in stdout

    def test_validate_command(self):
        """Test validate command."""
        returncode, stdout, stderr = run_cli_command(["validate"])
        assert returncode == 0
        assert "Testing all configured models" in stdout


class TestCLIEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_command(self):
        """Test running CLI with no arguments."""
        returncode, stdout, stderr = run_cli_command([])
        assert returncode == 0
        assert "help" in stdout.lower() or "usage" in stdout.lower()


def test_integration_flow():
    """Test a complete integration flow."""
    print("🔄 Testing complete integration flow...")
    
    # Step 1: Setup
    returncode, stdout, stderr = run_cli_command(["--setup"])
    assert returncode == 0, f"Setup failed: {stderr}"
    print("✅ Setup successful")
    
    # Step 2: Configure and select model
    returncode, stdout, stderr = run_cli_command(["config", "gpt-4o", "test-key-123"])
    assert returncode == 0, f"Config failed: {stderr}"
    print("✅ Model configuration successful")
    
    returncode, stdout, stderr = run_cli_command(["select", "gpt-4o"])
    assert returncode == 0, f"Selection failed: {stderr}"
    print("✅ Model selection successful")
    
    print("🎉 Complete integration flow successful!")


if __name__ == "__main__":
    # Run integration test
    test_integration_flow()
    print("\n🚀 All CLI tests would pass! Use pytest for detailed testing.")
