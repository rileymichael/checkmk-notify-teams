# checkmk-notify-teams

Send alerts to Microsoft Teams from CheckMK 1.x and 2.x

![Example Alert](img/example-alert.png)

## setup

- clone / copy `teams` script & put in `/omd/sites/{your_site}/local/share/check_mk/notifications`
- ensure it's executable (`chmod +x teams`)
- setup notification. method = 'Notify via Microsoft Teams', param = teams channel webhook
![Example Config](img/example-config.png)
