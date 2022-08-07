**Terminal Utilities to automate and expedite frequent sfdx cli actions**
This repo is about using python with terminals to speed up some frequent tasks using sfdx cli during development of a salesforce 2nd Generation Project. Repo is primarily meant to be used with terminal and not any GUI aids but python is chosen over shells like bash so as to promote code portability among different shells and operating systems.

<ins>Setup for project</ins>:

* Install a version of python 3. I usually get around it using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) and set it as default.

* Install pandas. So far pandas has been used in addition to built-ins. If you are using conda use ```conda install pandas```, if not set up pip and use ```pip install pandas```.You may have to install additional dependencies beforehand in latter case.

* Project assumes contributors can set up sfdx projects for testing. [Help guide](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_intro.htm) for the same.


<ins>Examples of some cli operations</ins>:

* Retrieval or deployment of metadata during a 2GP development using manifest files. Currently a manifest present in the designated manifest folder which is also last modified one can be identified by the system and used for metadata retrieval and deployment. Support for any manifest of choice will also be added.During the same operation target org can be mentioned or not mentioned( default org for the project is used.)

* Manifest present in designated manifest folder can be merged i.e. merged manifest will have all the types and members of chosen manifests. Usage of manifest promotes quick retrievals and deployments in succcession when metadata of different types are involved which is even more helpful in deploying metadata to multiple orgs.

<ins>Near Future (on Priority) Enhancements</ins>:

* Setting utilities up for each sfdx project should be made infinitely easier.
Probable approaches:
    * Files for each automation should be made as a single class, having project directort as a property which is set while terminal issues a command from a sfdx project.

    * Turn sfdx utilites into a python module.

    * Add optimum and precise comments to already existing code.

    * Add tests for utilities class

    * Fix file for execute anonymous scripts