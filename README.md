# Restricted Access Species Data

Welcome! This project contains the infrastructure, code and the deployment pipeline to launch and develop the RASD static site, RASD service site and automated user pool backups.

- [Static Page README](cicd/static-page/README.md)
- [Backend README](cicd/rasd-service/README.md)
- [Backups README](cicd/backups/README.md)

## Environments
There are 2 environments: testing, and production. the CICD framework also allows for development and staging environments, these are not currently used in this project. The environment is determined by the branch.

| git branch                                | environment              | Static Site Domain                                     | Service Site Domain                                            |
| ----------------------------------------- | ------------------------ | ------------------------------------------------------ | -------------------------------------------------------------- |
| main                                      | production               | https://rasd.org.au/                                   | https://service.rasd.org.au/                                   |
| main                                      | staging ( not used )     |                                                        |                                                                |
| testing                                   | testing                  | https://testing.rasd.org.au/                           | https://service.testing.rasd.org.au/                           |
| feature* (e.g. feature/service-migration) | development ( not used ) | https://feature-service-migration.testing.rasd.org.au/ | https://service.feature-service-migration.testing.rasd.org.au/ |

The production environment runs in our production AWS account, testing and development run in the test account.
## Configuration
There are different levels of configurations. Global configuration is handled in the [`cicd/config.ini`](cicd/config.ini) file, and applies to all three components. For each component, there's a component level config file, for example [`cicd/rasd-service/config.ini`](cicd/rasd-service/config.ini). The component level will override global project configuration.

The File format is of a standard ini file with different sections corresponding to the different environments. There is a [DEFAULT] section that includes values common to all environments such as the code repo details. Default values can be overridden in an environment section.

## Git branching and deployment
The branching model for this project is very similar to [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).
The `main` branch is a faithful representation of what is running in production, the `testing` branch represents what is deployed to the testing environment. Both of these branches are protected and can only be altered through PRs. 
The `main` and `testing` branches are CICD enabled, any commits to these will result in a deployment to the corresponding environment. This is controlled under `AUTO_DEPLOY`, if set to `False`, it requires a manual `release changes` in CodePipeline.

## Development workflow
The `main` and `testing` branches are protected and cant be committed to directly. To begin development on a feature or enhancement:
- Create a branch off `main` that includes a short description of the feature e.g. `feature/update-footer`
- Make all your changes and commit them to your branch. Test locally/deploy new development environment for testing.
- Once it's ready for deployment create a PR to merge your branch into `testing` Include at least one reviewer. It can be left up to the PR author if they want to wait for an approval, at the very least the reviewer receives a notification that we are getting ready for a testing deploy.
- Once the PR is merged it will be automatically deployed to the `testing` environment. Delete the feature branch. Tear down environment you deployed to AWS.
- Do any required UAT testing on the testing environment
- When UAT is passed create a PR to merge `testing` into `main` including at least one reviewer. Again it can be left up to the author if they want to wait for an approval
- When the PR is merged the changed will be automatically deployed to production


## Deployment to AWS

Deploy the CodePipeline is a one off step for each environment.

This is a one off step to create the CodePipeline for your feature branch, it should only need to be done once after you first create your feature branch. Run your AWS CLI authentication then then run the script `cicd/{COMPONENT}/pipeline/deploy_pipeline.sh` This will deploy or update the CodePipeline so that points to your newly created feature branch

Once the pipeline is deployed it will monitor itself for changes and redeploy itself if it's updated. Only the feature branch CodePipeline needs to be deployed manually. All other environments are already launched and will update themselves automatically when there are pipeline changes.

### Deployment of Service Website

As we stored `ABN_LOOKUP_GUID` key in AWS secrets, it will need a one off process to set the secret. The cloudformation will create an empty secret and you should be able to put values in it. Once it's done, it will need no further actions for that.

You might encounter error in building frontend phase since DNS might not be resolved in a short time. Wait a few minutes and try again, then error should disappear. Then you can use commands to setup the first time user and use the system.

## Rollback
To rollback to any previous revision go to CodePipeline and after selecting "Release Change" choose the commit to release. [Detailed instructions here](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-trigger-source-overrides.html#pipelines-trigger-source-overrides-console)



