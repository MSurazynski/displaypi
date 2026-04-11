set shell := ["bash", "-c"]
venv_python := "venv/bin/python3"

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Running..."
    venv/bin/python3 main.py --type dashboard --daytime morning --day today
    @echo "Finished!"

display-evening-today:
    @echo "Running..."
    venv/bin/python3 main.py --type dashboard --daytime evening --day today
    @echo "Finished!"

display-nasa:
    @echo "Running..."
    venv/bin/python3 main.py --type nasa
    @echo "Finished!"

load-data:
    venv/bin/python3 -m utils.data

requirements-laptop:
    venv/bin/python3 -m pip freeze > requirements.laptop.txt
    @echo "Generated requirements.laptop.txt"

requirements-pi:
    venv/bin/python3 -m pip freeze --local > requirements.pi.txt
    @echo "Generated requirements.pi.txt"

apt-pi:
    dpkg-query -W -f='${binary:Package}\n' \
        python3-gpiozero \
        python3-lgpio \
        python3-rpi-lgpio \
        > apt-packages.pi.txt
    @echo "Generated apt-packages.pi.txt"

export-all-laptop:
    just requirements-laptop

export-all-pi:
    just requirements-pi
    just apt-pi