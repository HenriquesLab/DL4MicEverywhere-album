# Introduction 

The deployment of album solutions is managed by GitHub actions. The workflows related with the deployment of solutions can be divided in two: the auxiliary workflows that do the backend of the deployment and the frontend workflows that are the ones launched.

The frontend workflows are: [`check_dl4mic_versions.yml`](../../../.github/workflows/check_dl4mic_versions.yml), [`deploy_solution_all.yml`](../../../.github/workflows/deploy_solution_all.yml) and [`deploy_solution_list.yml`](../../../.github/workflows/deploy_solution_list.yml).

The auxiliary workflows are: [`aux_deploy_solution.yml`](../../../.github/workflows/aux_deploy_solution.yml), [`aux_test_deploy_solution_list.yml`](../../../.github/workflows/aux_test_deploy_solution_list.yml) and [`aux_test_push_solution.yml`](../../../.github/workflows/aux_test_push_solution.yml).

# When is triggered?

These GitHub actions can be triggered by three different reasons:

1. **Automatically each day at 01:30 AM.** This will check if the version of any DL4MicEverywhere configuration has changed. If so, it will test and deploy all the solutions related with the updated DL4MicEverywhere configurations. This workflow is followed by [`check_dl4mic_versions.yml`](../../../.github/workflows/check_dl4mic_versions.yml).
2. **Manually giving a list of folders names from DL4MicEverywhere.** This will test and deploy all the solutions provided in the list of folders. This workflow is followed by [`deploy_solution_list.yml`](../../../.github/workflows/deploy_solution_list.yml).
3. **Manually triggered by the user.** Two different workflows can be manually triggered by clicking the `Run workflow` option. 

    First, [`Check and build updated DL4MicEverywhere`](../../../.github/workflows/check_dl4mic_versions.yml), which will do the same as **Automatically each day at 01:30 AM** This workflow is followed by [`check_dl4mic_versions.yml`](../../../.github/workflows/check_dl4mic_versions.yml). 
    
    Then, [`Check and build ALL DL4MicEverywhere`](../../../.github/workflows/deploy_solution_all.yml), will go through all the [source folders](../../../src) on the repository and test and deploy them. This workflow is followed by [`deploy_solution_all.yml`](../../../.github/workflows/deploy_solution_all.yml). 

# How does it work?

As many workflows are involved on the deployment of album solutions, this section will be divided on two. First the auxiliary/backend workflows and then the frontend workflows that rely on previous workflows.

## a) Auxiliary/Backend workflows 

### **(Aux) Test solution and push to source**

This workflow requires from a string as input, that string must be the 

## b) Frontend workflows

1. 