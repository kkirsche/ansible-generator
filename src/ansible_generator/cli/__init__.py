from ansible_generator.cli.main import AnsibleGeneratorCLI


def main():
    """Entry point for the application script"""
    cli = AnsibleGeneratorCLI()
    cli.build()
    cli.run()
