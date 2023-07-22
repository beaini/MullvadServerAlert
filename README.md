# MullvadServerAlert

MullvadServerAlert is a tool that uses GitHub Actions to monitor the status of Mullvad VPN servers and sends alerts to a specified Discord channel when a server is detected as down. It uses the OpenAPI endpoint to fetch the status of each server and verifies their status.

## Setup

1. **Clone this repository:** Use the "Use this template" button to create a new repository from this template.

2. **Modify the config file:** Edit the `config.json` file in your new repository to include the hostnames of the Mullvad servers you want to monitor.

3. **Set up the Discord webhook:** 
   - In your Discord server, create a new webhook (Server Settings > Integrations > New Webhook).
   - Copy the webhook URL.

4. **Add the Discord Webhook URL as a GitHub Secret:**
   - In your cloned GitHub repository, go to Settings > Secrets > New repository secret.
   - Create a new secret named `DISCORD_WEBHOOK` and paste the webhook URL as the value.

5. **Monitor your Mullvad servers:** The GitHub Action is scheduled to run once an hour and will send a message to your Discord server if any of the specified Mullvad servers are detected as down.

## License

MullvadServerAlert is released under the MIT License. See the LICENSE file for more details.

## Contributions

Contributions are welcome! Please feel free to submit a pull request.
