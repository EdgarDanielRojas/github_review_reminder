
# Deployment

To deploy the Github Review Reminder as a Google Cloud Function, follow these steps:

### Create a GitHub access token:

1. Go to your GitHub account settings and navigate to the Developer settings.
2. Select Personal access tokens and click on Generate new token.
3. Give your token a descriptive name.
4. Under the repo scope, select the following permissions:
   - **public_repo** (if your repositories are public)
   - **repo** (if your repositories are private)
5. Click on Generate token.
6. Copy the generated access token.

### Create a Slack webhook URL:

1. In your Slack workspace, go to Settings & administration and select Manage apps.
2. Search for "Incoming Webhooks" and click on Add to Slack to install the app.
3. Follow the instructions to create a new incoming webhook and copy the generated webhook URL.

### Set Secrets (Optional but strongly encouraged)

It is suggested to use this method to protect sensitive information within your organization, but the script will work with hard-coded values or plain text values when setting environment variables.

#### Option 1: Using Google Cloud Console:

1. Go to the Google Cloud Console.
2. Create a new project or select an existing project.
3. Open the Secret Manager page from the navigation menu.
4. Click on Create Secret.
5. Enter a name for the secret, such as `github-access-token` or `slack-webhook-url`.
6. Enter the respective value (GitHub access token or Slack webhook URL) in the Secret value field.
7. Click on Create Secret to store the secret securely.

#### Option 2: Using the Command-Line Interface (CLI):

1. Install and set up the Google Cloud SDK.
2. Open a terminal or command prompt.
3. Run the following commands to store your secrets in Google Secret Manager:

   ##### Create GitHub token secret
   ```
   echo "your-github-access-token" | gcloud secrets create github-access-token --data-file=-
   ```

   ##### Create Slack webhook secret
   ```
   echo "https://hooks.slack.com/services/your-slack-webhook-url" | gcloud secrets create slack-webhook-url --data-file=-
   ```

   Replace `your-github-access-token` and `your-slack-webhook-url` with the respective values.

### Deploy Cloud Function

1. Go to the Google Cloud Console.
2. Create a new project or select an existing project.
3. Open the Cloud Functions page from the navigation menu.
4. Click on Create Function.
5. In the General section:
   - Set **environment** to 1st gen.
   - Enter a name for the function, e.g., `github-pr-review-reminder`.
   - Choose the desired region or leave it as the default.
6. In the Trigger section (you can use Pub/Sub as a trigger as well):
   - Select **HTTP** as the trigger type.
   - Leave the **Authentication** option as **Allow unauthenticated invocations** (If you want to be secure, you can change this to **Authenticated only** and set up the necessary IAM permissions to invoke it).
7. In the Runtime, build, connections, and security settings section:
   - Under **Runtime** -> **Runtime environment variables**, click on **Add variable**.
   - Add the following environment variables and their corresponding values:
     - **GITHUB_TOKEN**: Your Token Value (Option 1)
     - **SLACK_WEBHOOK**: Your Slack Webhook (Option 1)
     - **GITHUB_ORGANIZATION**: your_organization (replace `your_organization` with your GitHub organization name)
     - **DURATION_THRESHOLD**: 3 (adjust the value if you want a different threshold)
   - You can also set **GITHUB_TOKEN** and **SLACK_WEBHOOK** via secrets if you set them up:
     - Go to **Security and Image Repo**.
     - Click on **Add a Secret Reference**.
     - Select your secret and version (latest works).
     - Select **reference method** as **exposed as environment variable**.
8. In the **Source code** section:
   - Select **Inline editor**.
   - Copy the code from `main.py` in this repository and paste it into the inline editor.
   - Copy the contents of the `requirements.txt` file in this repository and create a new file named `requirements.txt` in the inline editor. Paste the copied contents into the `requirements.txt` file.
9. Click on **Create** to deploy the Cloud Function.

### Schedule Function Trigger

To schedule the Cloud Function to execute at a specific hour each day, follow these steps:

1. Go to the Google Cloud Console.
2. Open your project and navigate to the **Cloud Scheduler** page.
3. Click on **Create Job**.
4. In the **Name** field, enter a name for the job, such as `github-pr-review-alert`.
5. In the **Frequency** section, select **Recurring**.
6. Set the desired schedule by specifying the **Hours**, **Minutes**, and **Timezone** (e.g., `0 9 * * *` to execute the job daily at 9 AM in the timezone).
7. In the **Target** section:
   - Select **HTTP** as the **URL** target type.
   - Enter the URL of your Cloud Function in the **URL** field. The URL should be in the format `https://REGION-PROJECT_ID.cloudfunctions.net/github-pr-review-alert`.
   - Choose the **HTTP Method** as **POST**.
8. In the **Auth header** section, you can optionally specify any required headers for your function.
9. Click on **Show more** to expand the **Advanced options** section.
10. In the **Retry strategy** section, you can configure the retry settings for failed invocations.
11. Click on **Create** to create the Cloud Scheduler job.

Following these steps, you should get a Cloud Function up and running that notifies your Slack channel as scheduled.