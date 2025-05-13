#!/usr/bin/env python3
import yaml
import sys
import os

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def generate_tech_stack_jobs(config, pipeline):
    tech_stack = config["technology"]["stack"]
    pipeline["include"].append(f".kone-ci/templates/{tech_stack}.yml")

def generate_deployment_jobs(config, pipeline):
    deployment_method = config["deployment"]["method"]
    pipeline["include"].append(f".kone-ci/templates/deployments/{deployment_method}.yml")

def generate_branching_rules(config, pipeline):
    for env in config["deployment"]["environments"]:
        rule = {
            "if": f'$CI_COMMIT_REF_NAME == "{env["branch"]}"',
            "variables": {
                "DEPLOY_ENV": env["name"]
            }
        }
        pipeline["workflow"]["rules"].append(rule)

def generate_pipeline(config_file):
    config = load_config(config_file)
    
    pipeline = {
        "stages": [],
        "variables": {},
        "include": [],
        "workflow": {
            "rules": []
        }
    }


    generate_tech_stack_jobs(config, pipeline)
    
   
    generate_deployment_jobs(config, pipeline)
    
    
    generate_branching_rules(config, pipeline)

    return pipeline

if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "ci-config.yml"
    pipeline = generate_pipeline(config_file)
    print(yaml.dump(pipeline))
