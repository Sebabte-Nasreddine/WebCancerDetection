# Jenkins Setup Guide

This guide explains how to run Jenkins locally and configure the pipeline for this project.

## 1. Start Jenkins

We use a separate Docker Compose file to run Jenkins. This Jenkins instance has access to your host's Docker socket, allowing it to build Docker images.

1.  Start the Jenkins container:
    ```bash
    docker-compose -f docker-compose-jenkins.yml up -d
    ```

2.  Retrieve the initial admin password:
    ```bash
    docker exec jenkins_server cat /var/jenkins_home/secrets/initialAdminPassword
    ```

3.  Open Jenkins in your browser at [http://localhost:8080](http://localhost:8080).

## 2. Configure Jenkins

1.  **Unlock Jenkins**: Paste the password you retrieved in step 1.2.
2.  **Install Plugins**: Select "Install suggested plugins".
3.  **Create Admin User**: specificy your username and password.
4.  **Instance Configuration**: Default is fine.

## 3. Create the Pipeline Job

1.  On the Jenkins Dashboard, click **New Item**.
2.  Enter a name (e.g., `canc-pipeline`) and select **Pipeline**. Click **OK**.
3.  Scroll down to the **Pipeline** section.
4.  **Definition**: Select **Pipeline script from SCM**.
5.  **SCM**: Select **Git**.
6.  **Repository URL**:
    - If your project is on GitHub/GitLab, use that URL.
    - If testing locally with no remote, you can map the local directory.
    - We have mounted your project to `/var/jenkins_home/workspace/canc-pipeline`.
    - You can use this path as a "local" git repository or simply rely on the mount.
    - **Recommended for local dev**: In the **Pipeline** section, choose **Definition: Pipeline script from SCM**, **SCM: Git**.
    - **Repository URL**: `file:///var/jenkins_home/workspace/canc-pipeline`
    - NOTE: This requires your local directory to be a valid git repo (with compiled `.git`).

    - **Repositories**: Ensure you have committed your `Jenkinsfile` and other changes! Jenkins/Git only sees committed files.
    - **Branch Specifier**: Change `*/master` to `*/sebabte` (or your current branch name: run `git branch` to check).
7.  **Script Path**: `Jenkinsfile` (if using SCM).
8.  Click **Save**.

## 4. Run the Pipeline

1.  Click **Build Now** on the left sidebar.
2.  Click the build number (e.g., `#1`) under "Build History".
3.  Click **Console Output** to see the logs.

## 5. Troubleshooting

- **Docker Permission Denied**: If Jenkins fails to build with a permission error regarding `/var/run/docker.sock`, ensure the group permission on your host allows it, or use `privileged: true` (already included in compose file).
