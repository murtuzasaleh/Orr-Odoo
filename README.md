# ORR - Odoo Project

# Table of Contents
* [Installing](#Installing)
* [Building and Testing](#Building-and-Testing)
* [Contributing](#Contributing)
	* [Private module](#Private-module)
	* [Public module](#Public-module)
		* [In the submodule](#In-the-submodule)
		* [In the main repo](#In-the-main-repo)
* [Deploying](#Deploying)


Repository for the Pavlov Media Odoo project.

# Installing

Look at the [INSTALL](./INSTALL.md) file.

# Building and Testing
Run
```shell script
./build.sh
```
Start Odoo
```shell script
. env/bin/activate
odoo -c odoo.conf
```
Go to https://localhost:8069

# Contributing

## Private module

* Create a new branch and add your module in src/custom-addons
* Update the file of the next release in `/ansible`
* Commit, push and create a pull request against the `develop` branch

## Public module

### In the submodule

* Create a new branch in src/<repo> and add your module
* Commit your changes and push your module to the public repo
* In Github (http://github.com/ursais/repo), create a pull request against the public repository
* Commit, push and create a pull request against `OCA/12.0`

### In the main repo

* Add your pull request in `/repos.yml`
* Update the file of the next release in `/ansible`
* Run
```shell script
gitaggregate -c repos.yml -p -j 5
```
* Commit, push and create a pull request against `develop`

# Deploying

Please refer to the [project documentation](https://wiki.opensourceintegrators.com/orr/index.php?title=Category:Releases).
