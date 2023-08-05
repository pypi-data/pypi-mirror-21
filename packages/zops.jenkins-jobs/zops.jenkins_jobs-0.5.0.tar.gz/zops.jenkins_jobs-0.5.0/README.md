# zops.jenkins_jobs

Manage the creation of jenkins jobs.

Organize your [Jenkins](jenkins.io) jobs right inside your code.

A typical projetct usinhg zops.jenkins_jobs directory would look like this:

```
/jenkins-jobs
  Jenkinsfile
  branch.yml
  jenkins-jobs.ini
```

### branch.yml

```YAML
- job:
    name: zops.jenkins_jobs__{branch}
    project-type: pipeline
    pipeline:
      script-path: jenkins-jobs/Jenkinsfile
      scm:
        - git:
            url: 'git@github.com:zerotk/zops.jenkins_jobs'
            credentials-id: 'XXX-YYY'
            skip-tag: true
            wipe-workspace: false
            branches:
              - '*/{branch}'
```

* The {setup.name} and {setup.url} variable are obtained from setup.py;
* The {git.branch} variable is obtained from the git repository;
```

With the following command line you can create the job in your Jenkins server:

```bash
$ zops jobs create
```
