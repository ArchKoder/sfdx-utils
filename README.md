Terminal Utilities to automate and expedite frequent sfdx cli actions.

<ins>Examples of some cli operations</ins>:

* Retrieval or deployment of metadata during a 2GP development using manifest files. Currently a manifest present in the designated manifest folder and being last modified can be identified by the system and used for metadata retrieval and deployment. Support for any metadata will also be added.During the same operation target org can be mentioned or not mentioned( default org for the project is used.)

* Manifest present in designated manifest folder can be merged i.e. merged manifest will have all the types and members of chosen manifests. Usage of manifest promotes quick retrievals and deployments in succcession when metadata of different types are involved as well as when metadata has to be used for multiple target orgs, eg- deploying same ticket's fix onto multiple orgs.

<ins>Near Future (on Priority) Enhancements</ins>:

* Setting utilities up for each sfdx project should be made infinitely easier.
Probable approaches:
* * Files for each automation should be made as a single class, having project directort as a property which is set while terminal issues a command from a sfdx project.

* * Turn sfdx utilites into a python module.