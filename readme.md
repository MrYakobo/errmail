# errmail

if you have services that run in systemd, you'll probably want to get an email when a service fails.

<img width="1015" alt="Screenshot 2024-08-18 at 22 33 19" src="https://github.com/user-attachments/assets/58d269bd-1fe8-415f-bb7b-ca524392bc55">

## Usage

1. Clone this repo to some place `/home/user/errmail/`
2. Add this service to `/etc/systemd/system/mail-notify@.service` (edit the environment variables)

```
[Unit]
Description=Send email

[Service]
Environment=SMTP_PASSWORD=your_password
Environment=SMTP_EMAIL=oops@mydomain.com
Environment=SENDER_NAME=oops systemd
Environment=SMTP_URL=smtp.domain.org
ExecStart=/bin/sh -c '/usr/bin/systemctl status %i | /home/user/errmail/ansi2html.sh | /home/user/errmail/errmail.py --subject "[systemd %i] Fail" --to my.personal@gmail.com'

[Install]
WantedBy=multi-user.target
```

3. Add `OnFailure=mail-notify@%i.service` to any .service you want to monitor.
4. Profit

## Credits where it's due

The script for converting terminal ansi codes (colors and such) to valid email HTML is done with the ansi2html script, [from here][1]

[1]: https://github.com/pixelb/scripts/blob/master/scripts/ansi2html.sh
