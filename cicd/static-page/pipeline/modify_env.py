#!/usr/bin/env python3

###
# Script used to modify the footer website link and publish date in the quarto source files _quarto.yaml
# Usage: modify_env.py ../quarto-source-files/_quarto.yaml

from datetime import datetime
import yaml
import sys
import os


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print('Usage: python modify_env.py <env>')
        sys.exit(1)

    with open(args[1], 'r') as file:
        env = yaml.safe_load(file)
    
    # Get environment variables
    hosted_zone = os.getenv('HOSTED_ZONE', 'rasd.org.au')
    sub_domain = os.getenv('SUB_DOMAIN', 'www')

    # Change footer and navbar url to rasd
    url = f"{sub_domain}.{hosted_zone}"
    html_url = f"https://{url}/"
    env['book']['navbar']['href'] = html_url
    env['book']['page-footer']['center'][0]['text'] = url
    env['book']['page-footer']['center'][0]['href'] = html_url
    
    # Update publised date
    current_date = datetime.now().strftime('%m/%d/%Y')
    print(current_date)
    env['book']['date'] = current_date

    with open(args[1], 'w') as file:
        yaml.dump(env, file, sort_keys=False)
    
    print(env)
    print('Environment variables updated successfully')