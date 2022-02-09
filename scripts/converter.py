#!/usr/bin/env python

import re

import yaml
import click

# https://stackoverflow.com/questions/51272814/python-yaml-dumping-pointer-references
yaml.Dumper.ignore_aliases = lambda *args: True

CONFIG_TEMPLATE = {
    "version": 2.1,
    "commands": {
        "prepare_python_env": {
            "description": "Common prepare steps for all jobs",
            "steps": [
                "checkout",
                {"run": {"name": "install dependencies", "command": "poetry install"}},
            ],
        }
    },
    "jobs": {},
    "workflows": {
        "version": 2,
    },
}

JOB_TEMPLATE = {
    "docker": [{"image": "cimg/python:3.10.2"}],
    "steps": [
        "prepare_python_env",
        {"run": {"name": "Run", "command": "poetry run python --version"}},
    ],
}

WORKFLOW_TEMPLATE = {
    "triggers": [
        {
            "schedule": {
                "cron": "10 8 * * *",
                "filters": {"branches": {"only": ["main"]}},
            }
        }
    ],
    "jobs": [],
}


def load_crontab():
    tab = []
    with open("crontab") as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            if line.strip() == "":
                continue
            tab.append(parse_cron(line))
    return tab


def parse_cron(line):
    parts = line.split()
    cron = " ".join(parts[:5])
    remaining = " ".join(parts[5:])

    m = re.match(r"(?P<command>.*)\s+@@(?P<name>\w+)@@", remaining)
    if m is None:
        raise ValueError(f"Line {line}v 不满足格式要求")

    return {
        "cron": cron,
        "command": m.group("command"),
        "name": m.group("name"),
    }


def generate_circle_ci_config(crons):
    jobs = {}
    workflows = {}
    for cron in crons:
        job_name = cron["name"] + "_job"
        job = JOB_TEMPLATE.copy()
        job["steps"][1]["run"]["command"] = cron["command"]
        jobs[job_name] = job

        workflow = WORKFLOW_TEMPLATE.copy()
        workflow["jobs"].append(job_name)
        workflow["triggers"][0]["schedule"]["cron"] = cron["cron"]
        workflow_name = cron["name"] + "_cron"
        workflows[workflow_name] = workflow

    config = CONFIG_TEMPLATE.copy()
    config["jobs"] = jobs
    config["workflows"] = workflows
    return yaml.dump(config, default_flow_style=False)


@click.command()
@click.option("-i", "--inplace", is_flag=True, help="update config.yml inplace")
def main(inplace):
    crons = load_crontab()
    config = generate_circle_ci_config(crons)
    if inplace:
        with open(".circleci/config.yml", "w") as f:
            f.write(config)
    else:
        print(config)


if __name__ == "__main__":
    main()
