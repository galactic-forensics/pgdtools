"""Configuration file for testing the package with ``nox``."""

import nox


nox.options.sessions = "lint", "safety", "tests", "xdoctest"

package = "pgdtools"
locations = "pgdtools", "tests", "noxfile.py", "docs/conf.py"
python_suite = ["3.11", "3.10", "3.9", "3.8"]
python_main = "3.11"


@nox.session(python=python_main)
def docs(session):
    """Build the documentation."""
    session.install("sphinx", "sphinx_rtd_theme", ".[db_maintainer]")
    session.chdir("docs")
    session.run(
        "sphinx-build", "-b", "html", ".", "_build/html/"
    )  # as for readthedocs.io


@nox.session(python=python_main)
def lint(session):
    """Lint project using ``flake8``."""
    args = session.posargs or locations
    session.install(".[dev, db_maintainer]")
    session.run("flake8", *args)


@nox.session(python=python_suite)
def tests(session):
    """Test the project using ``pytest``."""
    session.install(".[dev, db_maintainer]")
    session.run("pytest")


@nox.session(python=python_main)
def safety(session):
    """Safety check for all dependencies."""
    session.install(".[dev, db_maintainer]", "safety")
    session.run(
        "safety",
        "check",
        "--full-report",
    )


@nox.session(python=python_main)
def xdoctest(session):
    """Test docstring examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install("xdoctest[all]", ".[db_maintainer]")
    session.run("python", "-m", "xdoctest", package, *args)
