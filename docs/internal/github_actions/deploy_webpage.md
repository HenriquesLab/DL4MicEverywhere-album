# Introduction 

The deployment of the webpage with the DL4MicEverwhere catalog ([https://henriqueslab.github.io/DL4MicEverywhere-album/](https://henriqueslab.github.io/DL4MicEverywhere-album/)) is automatically done using GitHub actions.

The main workflow responsible for that is [`deploy_page.yml`](../../../.github/workflows/deploy_page.yml), which can be also found as a GitHub action named as [GitHub page creation](https://github.com/HenriquesLab/DL4MicEverywhere-album/actions/workflows/deploy_page.yml).

# When is triggered?

This GitHub action can be triggered by three different reasons:

1. **When pushing a commit with a new tag.** On this repository, that will correspond with the deployment of a new solution.
2. **When a tag has been removed.** On this repository, that will correspond with the undeployment of a solution.
3. **Manually triggered by the user.** This can be done on the [GitHub page creation](https://github.com/HenriquesLab/DL4MicEverywhere-album/actions/workflows/deploy_page.yml) site, by clicking the `Run workflow` option. This is mostly meant for development and testing reasons.

# How does it work?

These are the steps followed by the workflow:

## 1. Building job

1. It initially waits 30 seconds in case a `git push` has been done before triggering this action. 
2. Clones `DL4MicEverywhere-album` repository.
3. Sets up Node.js version 20, this package is needed for the webpage creation.
4. Stores Gatsby dependencies at cache.
5. Using the Gatsby information located on [its folder](../../../gatsby), it installs all required dependencies and builds the webpage.
6. The created webpage is then uploaded as an [action artifact](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow).

## 2. Deploying job

1. Using the [actions/deploy-pages@v4](https://github.com/actions/deploy-pages/tree/v4/) GitHub action from the GitHub Marketplace, the webpage is deploy from the action artifact.