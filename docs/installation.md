# Installation

Requires Python 3.10 or newer.

=== "Windows"

    <p class="tab-h2">Python</p>

    Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). During setup, tick **Add python.exe to PATH**.

    Confirm the install in Command Prompt or PowerShell:

    ```powershell
    py -3 --version
    ```

    <p class="tab-h2">Install ifc2graph</p>

    In the folder where you want to work, create a virtual environment and install the package:

    ```powershell
    py -3 -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install ifc2graph
    ```

    If PowerShell blocks the activate script, run this once for your user account, then activate again:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    ```

    Alternatively, without a virtual environment:

    ```powershell
    pip install ifc2graph
    ```

    <p class="tab-h2">Neo4j</p>

    ifc2graph writes nodes and edges to a Neo4j database. You need a running instance that accepts Bolt connections (default `bolt://localhost:7687`).

    Download [Neo4j Desktop](https://neo4j.com/download/), create a local DBMS, set a password, and start it.

    !!! note    
        `uri`, `user`, and `password` can be omitted in the API if these environment variables are set instead:

        | Variable | Used for | Fallback |
        | --- | --- | --- |
        | `NEO4J_URI` | Bolt URI | `bolt://localhost:7687` |
        | `NEO4J_USER` | username | `neo4j` |
        | `NEO4J_PASSWORD` | password | none (required) |

        In PowerShell for the current session:

        ```powershell
        $env:NEO4J_URI = "bolt://localhost:7687"
        $env:NEO4J_USER = "neo4j"
        $env:NEO4J_PASSWORD = "password"
        ```

    !!! warning
        **The target Neo4j database is cleared on every run** (`MATCH (n) DETACH DELETE n`) before anything is written. Point this at an empty or disposable database.

=== "macOS"

    <p class="tab-h2">Python</p>

    Install Python 3.10 or newer with [Homebrew](https://brew.sh/):

    ```bash
    brew install python@3.12
    ```

    Or download an installer from [python.org](https://www.python.org/downloads/). Confirm:

    ```bash
    python3 --version
    ```

    <p class="tab-h2">Install ifc2graph</p>

    In the folder where you want to work, create a virtual environment and install the package:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install ifc2graph
    ```

    Alternatively, without a virtual environment:

    ```bash
    pip install ifc2graph
    ```

    <p class="tab-h2">Neo4j</p>

    ifc2graph writes nodes and edges to a Neo4j database. You need a running instance that accepts Bolt connections (default `bolt://localhost:7687`).

    Download [Neo4j Desktop](https://neo4j.com/download/), create a local DBMS, set a password, and start it.

    !!! note
        `uri`, `user`, and `password` can be omitted in the API if these environment variables are set instead:

        | Variable | Used for | Fallback |
        | --- | --- | --- |
        | `NEO4J_URI` | Bolt URI | `bolt://localhost:7687` |
        | `NEO4J_USER` | username | `neo4j` |
        | `NEO4J_PASSWORD` | password | none (required) |

        ```bash
        export NEO4J_URI="bolt://localhost:7687"
        export NEO4J_USER="neo4j"
        export NEO4J_PASSWORD="password"
        ```

    !!! warning
        **The target Neo4j database is cleared on every run** (`MATCH (n) DETACH DELETE n`) before anything is written. Point this at an empty or disposable database.

=== "Linux"

    <p class="tab-h2">Python</p>

    Install Python 3.10 or newer from your distribution.

    Debian and Ubuntu:

    ```bash
    sudo apt update
    sudo apt install python3 python3-venv python3-pip
    ```

    Confirm:

    ```bash
    python3 --version
    ```

    <p class="tab-h2">Install ifc2graph</p>

    In the folder where you want to work, create a virtual environment and install the package:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install ifc2graph
    ```

    On Debian and Ubuntu, `apt install python3-venv` is required before `python3 -m venv` will work.

    Alternatively, without a virtual environment:

    ```bash
    pip install ifc2graph
    ```

    <p class="tab-h2">Neo4j</p>

    ifc2graph writes nodes and edges to a Neo4j database. You need a running instance that accepts Bolt connections (default `bolt://localhost:7687`).

    Download [Neo4j Desktop](https://neo4j.com/download/), create a local DBMS, set a password, and start it.

    !!! note
        `uri`, `user`, and `password` can be omitted in the API if these environment variables are set instead:

        | Variable | Used for | Fallback |
        | --- | --- | --- |
        | `NEO4J_URI` | Bolt URI | `bolt://localhost:7687` |
        | `NEO4J_USER` | username | `neo4j` |
        | `NEO4J_PASSWORD` | password | none (required) |

        ```bash
        export NEO4J_URI="bolt://localhost:7687"
        export NEO4J_USER="neo4j"
        export NEO4J_PASSWORD="password"
        ```

    !!! warning
        **The target Neo4j database is cleared on every run** (`MATCH (n) DETACH DELETE n`) before anything is written. Point this at an empty or disposable database.

Now that the installation is finished, see [usage instructions](index.md#usage) to get started.
