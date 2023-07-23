MullvadServerAlert
==================

MullvadServerAlert is a tool that uses GitHub Actions to monitor the status of Mullvad VPN servers. It sends alerts via multiple notification services when a server is detected as down. The tool uses the Mullvad API to fetch the status of each server, verifies their status, and sends notifications using [Apprise](https://github.com/caronc/apprise), a universal notification service.

Features
--------

-   Monitors the status of Mullvad VPN servers at specified intervals
-   Sends notifications via multiple services (Discord, Slack, etc.) when a server is detected as down
-   Uses GitHub Actions for scheduling and running the checks
-   Configurable list of servers to monitor
-   Configurable list of Apprise URLs for notifications

Setup
-----

1.  Click on the "Use this template" button to create a new repository from this template.

2.  Navigate to the 'Settings' tab of your new repository and click on 'Secrets' in the left sidebar.

3.  Click on the 'New repository secret' button.

4.  Create two new secrets:

    -   `HOSTNAMES`: A JSON-formatted string of the hostnames you want to monitor. For example: `["server1","server2","server3"]`.
    -   `APPRISE_URLS`: A JSON-formatted string of the Apprise URLs for the services where you want to receive notifications. For example: `["url1","url2","url3"]`.
5.  Save the secrets. GitHub Actions will now have access to these secrets and will use them when running the workflow.

6.  The GitHub Actions workflow is already set up in the `.github/workflows` directory in the file `hostname_check.yml`. By default, the workflow is scheduled to run every 5 minutes. If you want to change this, open `hostname_check.yml` and modify the `cron` line under `schedule`. The syntax for this line is the same as for cron jobs.

Usage
-----

After setting up, the GitHub Actions workflow will automatically run at the specified intervals. If a server is detected as down, the tool will send notifications to the configured services.

You can also run the tool locally by running `python main.py`. Make sure to set the `HOSTNAMES` and `APPRISE_URLS` environment variables if you are not using the `config.json` file.

Contributing
------------

Contributions are welcome! Please open an issue if you encounter any problems or have suggestions for improvements.