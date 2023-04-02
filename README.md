# Email Forwarding Script

This Python script periodically checks an SQLite database for new contact form submissions and sends them to the site owner via email. This script is scheduled to run via a cron job, which is configured in the Ubuntu Server settings.

## Who it's for

Although it is possible to incorporate this script directly into the Flask app, which would enable immediate forwarding of form submissions, using a database offers several benefits. For example:

Separation of concerns: By separating the email forwarding functionality into a separate script, I am keeping the concerns of the Flask app separate from the concerns of sending email. This can make your Flask app easier to reason about, test, and maintain.

Scalability: If a lot of submissions are coming in, it may be more efficient to have a separate process that periodically checks for new submissions and sends emails, rather than having your Flask app handle this functionality directly. This can help to keep the Flask app responsive and avoid performance issues.

Flexibility: By using a separate script and cron job, there is more flexibility to customise the email forwarding process. For example, you could change the frequency of the cron job to check for new submissions more or less frequently, or you could modify the Python script to add additional functionality (e.g., filtering out submissions that meet certain criteria before sending the email).

By storing the form submissions in a database, future development opportunities arise, such as the creation of an admin panel. This panel would enable the user to view all submissions, delete entries, and reply to emails at their discretion.
