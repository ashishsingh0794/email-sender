## Easy Email Sender with HTML payload

This repository provides a python wrapper scripts to send Emails with easily configurale payloads like Text/HTML.

#### Usage
1. Enter your SMTP config and credential to provided .env configuration file.
2. Setup [Email config file](config/email_params.yml) as per the required use-cas.
3. Look out for the below variables options defined in the main.py file:-

| Option              | Description                   | Type | Required  |
| --------------------|:------------------------------|---------|----------:|
| `mail_type`         | Type of the mail. Names the main categorization tag from step 2 config file. | String | yes |
| `redirect_url`      | Variable 1 to support given use-case (confirmation-email sending) | String | no |
| `customer_name`     | Variable 2 to support given use-case (confirmation-email sending) | String | no |
| `recipients_lst`    | Comma separated list of recipients of email | List | Yes |
| `email_data`        | Default value to set in case Email is type of plain text | String | no |

__Note__: 
1. If you want to use gmail credentials for email sending/testing, please follow [support.google](https://support.google.com/accounts/answer/185833?hl=en) for enabling 2 step verification and create your app password.
2. Logger is currently configured [Logger config file](config/logging.yml) to output on both std console and file output at .logs. 
Configure the setup as per the need or use self customized logger.
